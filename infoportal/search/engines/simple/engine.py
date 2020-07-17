import datetime
import logging
import time

from django.conf import settings
from django.http import JsonResponse
from documents.models import CodeOKVED, CodeOKS
from documents.models import Documents
from documents.serializers import DocumentsSerializer
from search.models import Search, AutoCompletion, SearchHistory
from search.serializers import SearchOptionsSerializer

from .querytexts import Query

LOGGER = logging.getLogger('django')

if settings.SEARCH_ENGINE.get('name') == 'simple':
    SEARCH_QUERY = Query()

    with open('stopwords.txt', "r") as f:
        stopwords = f.read()


def simple_search_auto_completions(search_serializer):
    s_text = search_serializer.data['search_text']

    str_page_size = search_serializer.data['page_size']
    if str_page_size:
        page_size = int(str_page_size)
        if page_size:
            if page_size < 1 or page_size > 10:
                page_size = 10
    else:
        page_size = 10

    doc = set()

    try:
        auto_comp = AutoCompletion.objects.filter(
            search_text__contains=s_text
        )
        for au in auto_comp:
            doc.add(au.search_text)
    except Exception as ex:
        LOGGER.error(ex)

    words = s_text.split()
    for a in words:
        try:
            auto_comp = AutoCompletion.objects.filter(
                search_text__contains=a
            )
            for au in auto_comp:
                doc.add(au.search_text)
        except Exception as ex:
            LOGGER.error(ex)

    try:
        print(AutoCompletion.objects.get(search_text__contains=s_text))
    except:
        if not AutoCompletion.objects.filter(search_text=s_text[:-1]).update(search_text=s_text):
            auto_completion = AutoCompletion()
            auto_completion.search_text = s_text
            auto_completion.page_size = page_size
            auto_completion.save()

    paginated_result = list(doc)
    paginated_result.sort()

    filtered_paginated_result = []
    flen = len(s_text)
    for phrase in paginated_result:
        if len(phrase) > flen:
            filtered_paginated_result.append(phrase)
    paginated_result = filtered_paginated_result[:page_size]

    search_limit = page_size - len(paginated_result)

    if search_limit > 0:
        search_doc = set()
        if s_text:
            if SEARCH_QUERY:
                serched = SEARCH_QUERY.phrase_query(s_text.lower())
                for doc_id in serched:
                    search_doc.add(doc_id)
        filtered_search_doc = list(search_doc)[:search_limit]
        try:
            for docId in filtered_search_doc:
                docs = Documents.objects.filter(pk=docId)
                for d in docs:
                    paginated_result.append(d.doc_name_ru)

        except Exception as ex:
            LOGGER.error(ex)

    return JsonResponse({'auto_completions': paginated_result})


def in_document(text, param):
    lst1 = param.lower().split()
    lst2 = text.lower().split()
    lst3 = [value for value in lst1 if value in lst2]
    return len(lst3) > 0


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} время выполнения {:.3f} ms'.format(f.__name__, (time2 - time1) * 1000.0))

        return ret

    return wrap


@timing
def simple_search_text(search_serializer, page, page_size, user_id):
    s_text = search_serializer.data['search_text']
    if s_text in stopwords:
        return JsonResponse({'documents': [], 'count': 0})

    if page_size == -1:
        str_page_size = search_serializer.data['page_size']
        if str_page_size:
            page_size = int(str_page_size)
            if page_size:
                if page_size < 1 or page_size > 10:
                    page_size = 10
        else:
            page_size = 10

    top_limit = page_size * page

    search = Search()
    search.search_text = s_text
    search.save()

    search_history = SearchHistory()
    search_history.userid = user_id
    search_history.search = search
    search_history.save()

    doc_set = set()
    doc = []

    str_s_options = search_serializer.data['search_options']
    search_options_serializer = SearchOptionsSerializer(data=str_s_options)

    search_options_serializer.is_valid()

    s_options = search_options_serializer.data

    result = []

    if s_options:
        if s_options.get('name_ru'):
            if s_text:
                if s_text != s_options.get('name_ru'):
                    s_text = s_text + " " + s_options.get('name_ru')
            else:
                s_text = s_options.get('name_ru')

    if s_text:
        if SEARCH_QUERY:
            serched = SEARCH_QUERY.phrase_query(s_text.lower())
            for doc_id in serched:
                doc_set.add(doc_id)

            for docId in doc_set:
                document = Documents.objects.get(pk=docId)
                if s_options:
                    if s_options.get('document_status'):
                        if not in_document(document.doc_status, s_options.get('document_status')):
                            continue
                    if s_options.get('document_type'):
                        if not in_document(document.doc_kind, s_options.get('document_type')):
                            continue
                    if s_options.get('brief_document_description'):
                        if not in_document(s_options.get('brief_document_description'),
                                           document.doc_mark):
                            continue
                    if s_options.get('name_en'):
                        if not in_document(s_options.get('name_en'), document.doc_name_en):
                            continue
                    if s_options.get('abstract'):
                        if not in_document(s_options.get('abstract'), document.doc_annotation):
                            continue
                    if s_options.get('note'):
                        if not in_document(s_options.get('note'), document.doc_comment):
                            continue
                    if s_options.get('full_designation_of_the_document'):
                        if not in_document(s_options.get('full_designation_of_the_document'),
                                           document.doc_full_mark):
                            continue
                    if s_options.get('okved'):
                        try:
                            code = CodeOKVED.objects.filter(title=s_options.get('okved'))
                            if document.classifier_okved != code:
                                continue
                        except Exception as ex:
                            LOGGER.error(ex)
                            continue
                    if s_options.get('oks'):
                        try:
                            code = CodeOKS.objects.filter(title=s_options.get('oks'))
                            if document.classifier_oks != code:
                                continue
                        except Exception as ex:
                            LOGGER.error(ex)
                            continue
                    if s_options.get('tk'):
                        if not in_document(s_options.get('tk'), document.tk_rus):
                            continue
                    if s_options.get('mtk'):
                        if not in_document(s_options.get('mtk'), document.mtk_dev):
                            continue
                    if s_options.get('keywords'):
                        if not in_document(s_options.get('keywords'), document.keywords):
                            continue
                    if s_options.get('date_of_adoption'):
                        if str(document.doc_assign_date) != s_options.get('date_of_adoption'):
                            continue
                    if s_options.get('effective_date'):
                        if str(document.doc_effective_date) != s_options.get('effective_date'):
                            continue
                    if s_options.get('recover_date'):
                        if str(document.doc_restoration_date) != s_options.get('recover_date'):
                            continue

                    ds = DocumentsSerializer(document)
                    result.append(ds.data)
                else:
                    if document.doc_status == 'actual':
                        ds = DocumentsSerializer(document)
                        result.append(ds.data)

                if len(result) == top_limit:
                    return JsonResponse({'documents': result[(page - 1) * page_size:], 'count': len(result)})

            count = len(result)
            limit_for_free_search = top_limit - len(result)
            doc_set = set()
            if limit_for_free_search > 0:
                free_serched = SEARCH_QUERY.free_text_query(s_text.lower())
                count = count + len(free_serched)
                free_serched = free_serched[:limit_for_free_search]
                for free_doc_id in free_serched:
                    doc_set.add(free_doc_id)

            result_advanced = []
            for docId in doc_set:
                document = Documents.objects.get(pk=docId)
                if s_options:
                    if s_options.get('document_status'):
                        if not in_document(document.doc_status, s_options.get('document_status')):
                            continue
                    if s_options.get('document_type'):
                        if not in_document(document.doc_kind, s_options.get('document_type')):
                            continue
                    if s_options.get('brief_document_description'):
                        if not in_document(s_options.get('brief_document_description'),
                                           document.doc_mark):
                            continue
                    if s_options.get('name_en'):
                        if not in_document(s_options.get('name_en'), document.doc_name_en):
                            continue
                    if s_options.get('abstract'):
                        if not in_document(s_options.get('abstract'), document.doc_annotation):
                            continue
                    if s_options.get('note'):
                        if not in_document(s_options.get('note'), document.doc_comment):
                            continue
                    if s_options.get('full_designation_of_the_document'):
                        if not in_document(s_options.get('full_designation_of_the_document'),
                                           document.doc_full_mark):
                            continue
                    if s_options.get('okved'):
                        try:
                            code = CodeOKVED.objects.filter(title=s_options.get('okved'))
                            if document.classifier_okved != code:
                                continue
                        except Exception as ex:
                            LOGGER.error(ex)
                            continue
                    if s_options.get('oks'):
                        try:
                            code = CodeOKS.objects.filter(title=s_options.get('oks'))
                            if document.classifier_oks != code:
                                continue
                        except Exception as ex:
                            LOGGER.error(ex)
                            continue
                    if s_options.get('tk'):
                        if not in_document(s_options.get('tk'), document.tk_rus):
                            continue
                    if s_options.get('mtk'):
                        if not in_document(s_options.get('mtk'), document.mtk_dev):
                            continue
                    if s_options.get('keywords'):
                        if not in_document(s_options.get('keywords'), document.keywords):
                            continue
                    if s_options.get('date_of_adoption'):
                        if str(document.doc_assign_date) != s_options.get('date_of_adoption'):
                            continue
                    if s_options.get('effective_date'):
                        if str(document.doc_effective_date) != s_options.get('effective_date'):
                            continue
                    if s_options.get('recover_date'):
                        if str(document.doc_restoration_date) != s_options.get('recover_date'):
                            continue

                    ds = DocumentsSerializer(document)
                    result_advanced.append(ds.data)
                else:
                    if document.doc_status == 'actual':
                        ds = DocumentsSerializer(document)
                        result_advanced.append(ds.data)

            result = result + result_advanced

            if len(result) < (page - 1) * page_size:
                return JsonResponse({'documents': [], 'count': 0})
            else:
                return JsonResponse({'documents': result[(page - 1) * page_size:], 'count': count})
    else:
        if s_options:
            if s_options.get('document_status'):
                try:
                    doc.append(
                        Documents.objects.filter(
                            doc_kind__contains=s_options.get('document_status')
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('document_type') and len(doc) < top_limit:
                try:
                    doc.append(
                        Documents.objects.filter(
                            doc_kind__contains=s_options.get('document_type')
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('brief_document_description') and len(doc) < top_limit:
                try:
                    doc.append(
                        Documents.objects.filter(
                            doc_mark__contains=s_options.get(
                                'brief_document_description')
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('name_en') and len(doc) < top_limit:
                try:
                    doc.append(
                        Documents.objects.filter(
                            doc_name_en__contains=s_options.get('name_en')
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('abstract') and len(doc) < top_limit:
                try:
                    doc.append(
                        Documents.objects.filter(
                            doc_annotation__contains=s_options.get('abstract')
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('note') and len(doc) < top_limit:
                try:
                    doc.append(
                        Documents.objects.filter(
                            doc_comment__contains=s_options.get('note')
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('full_designation_of_the_document') and len(doc) < top_limit:
                try:
                    doc.append(
                        Documents.objects.filter(
                            doc_full_mark__contains=s_options.get(
                                'full_designation_of_the_document'
                            )
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('okved') and len(doc) < top_limit:
                try:
                    code = CodeOKVED.objects.filter(title=s_options.get('okved'))

                    for c in code:
                        doc.append(Documents.objects.filter(classifier_okved=c))
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('oks') and len(doc) < top_limit:
                try:
                    code = CodeOKS.objects.filter(
                        code__contains=s_options.get('oks')
                    )
                    for c in code:
                        doc.append(Documents.objects.filter(classifier_oks=c))
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('tk') and len(doc) < top_limit:
                try:
                    doc.append(
                        Documents.objects.filter(
                            tk_rus__contains=s_options.get('tk')
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('mtk') and len(doc) < top_limit:
                try:
                    doc.append(
                        Documents.objects.filter(
                            mtk_dev__contains=s_options.get('mtk')
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('keywords') and len(doc) < top_limit:
                try:
                    doc.append(
                        Documents.objects.filter(
                            keywords__contains=s_options.get('keywords')
                        )
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('date_of_adoption') and len(doc) < top_limit:
                try:
                    search_date = datetime.strptime(
                        s_options.get('date_of_adoption'),
                        '%Y-%m-%d'
                    )
                    doc.append(
                        Documents.objects.filter(doc_assign_date=search_date)
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('effective_date') and len(doc) < top_limit:
                try:
                    search_date = datetime.strptime(
                        s_options.get('effective_date'),
                        '%Y-%m-%d'
                    )
                    doc.append(
                        Documents.objects.filter(doc_effective_date=search_date)
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if s_options.get('recover_date') and len(doc) < top_limit:
                try:
                    search_date = datetime.strptime(
                        s_options.data['recover_date'],
                        '%Y-%m-%d'
                    )
                    doc.append(
                        Documents.objects.filter(doc_restoration_date=search_date)
                    )
                except Exception as ex:
                    LOGGER.error(ex)

            if len(doc) < page * page_size:
                return JsonResponse({'documents': []})

            doc_list = doc[(page - 1) * page_size: page * page_size]
            for d in doc_list:
                for i in range(len(d)):
                    doc_set.add(d[i].pk)

            for docId in doc_set:
                ds = DocumentsSerializer(Documents.objects.get(pk=docId))
                result.append(ds.data)

            return JsonResponse({'documents': result, 'count': len(doc)})
    return JsonResponse({'documents': [], 'count': 0})
