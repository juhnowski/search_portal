from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from users.utils.permissions import *
from users.utils.authentication import get_token

from .models import Documents, DocumentsNotice, TextSetings, Comments
from .serializers import DocumentsSerializer, DocumentsListSerializer, \
    ShortDocumentsSerializer, DocumentsNoticeSerializer, \
    TextSettingsSerializer, CommentsSerializer, \
    RateDocumentsSerializer
from .utils.token_authentication import authenticate_credentials
from .utils.user_permission import check_permissions


class DocumentForm(forms.ModelForm):
    """
    Форма загрузки документа
    В дальнейшем вероятно удалить
    """
    doc_image_content = forms.FileField(required=False)
    doc_pdf_content = forms.FileField(required=False)
    related_documents = forms.ModelMultipleChoiceField(
                            queryset=Documents.objects.all(),
                            widget=CheckboxSelectMultiple(),
                            required=False,
                        )

    class Meta:
        model = Documents
        fields = ('doc_kind',
                  'doc_mark',
                  'doc_name_ru',
                  'doc_name_en',
                  'doc_annotation',
                  'doc_comment',
                  'doc_sys_number',
                  'doc_full_mark',
                  'doc_status',
                  'application_status',
                  'doc_reg_date',
                  'doc_limit_date',
                  'doc_on_rf_use',
                  'classifier_pns',
                  'doc_assign_org',
                  'doc_assign_date',
                  'classifier_enterd_countries',
                  'doc_reg_text',
                  'doc_effective_date',
                  'doc_restoration_date',
                  'doc_enter_org',
                  'classifier_okved',
                  'classifier_oks',
                  'classifier_okp',
                  'tk_rus',
                  'org_author_name',
                  'mtk_dev',
                  'keywords',
                  'doc_annotation_ru',
                  'doc_origin_language',
                  'contains_in_npa_links',
                  'cancel_in_part',
                  'doc_o_zsh',
                  'doc_o_zgo_vch',
                  'doc_o_zgo',
                  'doc_o_zsh_vch',
                  'doc_supplemented',
                  'doc_supplementing',
                  'doc_outside_system',
                  'doc_html_content',

                  'doc_changes',
                  'has_document_case',
                 )


def documents(request):
    """
    Станица с формой для загрузки документа
    Удалить после того, как будет определено как
    документ буде загружаться
    """
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES or None)
        if form.is_valid():
            doc_kind = form.cleaned_data['doc_kind']
            doc_mark = form.cleaned_data['doc_mark']
            doc_name_ru = form.cleaned_data['doc_name_ru']
            doc_name_en = form.cleaned_data['doc_name_en']
            doc_annotation = form.cleaned_data['doc_annotation']
            doc_comment = form.cleaned_data['doc_comment']
            doc_sys_number = form.cleaned_data['doc_sys_number']
            doc_full_mark = form.cleaned_data['doc_full_mark']
            doc_status = form.cleaned_data['doc_status']
            application_status = form.cleaned_data['application_status']
            doc_reg_date = form.cleaned_data['doc_reg_date']
            doc_limit_date = form.cleaned_data['doc_limit_date']
            doc_on_rf_use = form.cleaned_data['doc_on_rf_use']
            classifier_pns = form.cleaned_data['classifier_pns']
            doc_assign_org = form.cleaned_data['classifier_pns']
            doc_assign_date = form.cleaned_data['doc_assign_date']
            classifier_enterd_countries = form.cleaned_data['classifier_enterd_countries']
            doc_reg_text = form.cleaned_data['doc_reg_text']
            doc_effective_date = form.cleaned_data['doc_effective_date']
            doc_restoration_date = form.cleaned_data['doc_restoration_date']
            doc_enter_org = form.cleaned_data['doc_enter_org']
            classifier_okved = form.cleaned_data['classifier_okved']
            classifier_oks = form.cleaned_data['classifier_oks']
            classifier_okp = form.cleaned_data['classifier_okp']
            tk_rus = form.cleaned_data['tk_rus']
            org_author_name = form.cleaned_data['org_author_name']
            mtk_dev = form.cleaned_data['mtk_dev']
            keywords = form.cleaned_data['keywords']
            doc_annotation_ru = form.cleaned_data['doc_annotation_ru']
            doc_origin_language = form.cleaned_data['doc_origin_language']
            contains_in_npa_links = form.cleaned_data['contains_in_npa_links']
            cancel_in_part = form.cleaned_data['cancel_in_part']
            doc_o_zsh = form.cleaned_data['doc_o_zsh']
            doc_o_zgo_vch = form.cleaned_data['doc_o_zgo_vch']
            doc_o_zgo = form.cleaned_data['doc_o_zgo']
            doc_o_zsh_vch = form.cleaned_data['doc_o_zsh_vch']
            doc_supplemented = form.cleaned_data['doc_supplemented']
            doc_supplementing = form.cleaned_data['doc_supplementing']
            doc_outside_system = form.cleaned_data['doc_outside_system']
            doc_html_content = form.cleaned_data['doc_html_content']
            doc_changes = form.cleaned_data['doc_changes']
            has_document_case = form.cleaned_data['has_document_case']
            related_documents = form.cleaned_data['related_documents']

            try:
                doc_image_content = request.FILES['doc_image_content'].file.read()
                image_contemt_name = request.FILES['doc_image_content'].name
            except MultiValueDictKeyError:
                doc_image_content = None
            try:
                doc_pdf_content = request.FILES['doc_pdf_content'].file.read()
                pdf_content_name = request.FILES['doc_pdf_content'].name
            except MultiValueDictKeyError:
                doc_pdf_content = None

            document = Documents.objects.create(
                               doc_kind=doc_kind,
                               doc_mark=doc_mark,
                               doc_name_ru=doc_name_ru,
                               doc_name_en=doc_name_en,
                               doc_annotation=doc_annotation,
                               doc_comment=doc_comment,
                               doc_sys_number=doc_sys_number,
                               doc_full_mark=doc_full_mark,
                               doc_status=doc_status,
                               application_status=application_status,
                               doc_reg_date=doc_reg_date,
                               doc_limit_date=doc_limit_date,
                               doc_on_rf_use=doc_on_rf_use,
                               classifier_pns=classifier_pns,
                               doc_assign_org=doc_assign_org,
                               doc_assign_date=doc_assign_date,
                               doc_reg_text=doc_reg_text,
                               doc_effective_date=doc_effective_date,
                               doc_restoration_date=doc_restoration_date,
                               doc_enter_org=doc_enter_org,
                               tk_rus=tk_rus,
                               org_author_name=org_author_name,
                               mtk_dev=mtk_dev,
                               keywords=keywords,
                               doc_annotation_ru=doc_annotation_ru,
                               contains_in_npa_links=contains_in_npa_links,
                               cancel_in_part=cancel_in_part,
                               doc_o_zsh=doc_o_zsh,
                               doc_o_zgo_vch=doc_o_zgo_vch,
                               doc_o_zgo=doc_o_zgo,
                               doc_o_zsh_vch=doc_o_zsh_vch,
                               doc_supplemented=doc_supplemented,
                               doc_supplementing=doc_supplementing,
                               doc_outside_system=doc_outside_system,
                               doc_html_content=doc_html_content,
                               doc_changes=doc_changes,
                               has_document_case=has_document_case
                       )
            if doc_image_content is not None:
                document.doc_image_content = doc_image_content
                document.image_contemt_name = image_contemt_name

            if doc_pdf_content is not None:
                document.doc_pdf_content = doc_pdf_content
                document.pdf_content_name = pdf_content_name
            document.save()
            document.classifier_enterd_countries.set(classifier_enterd_countries)
            document.classifier_okved.set(classifier_okved)
            document.classifier_oks.set(classifier_oks)
            document.classifier_okp.set(classifier_okp)
            document.doc_origin_language.set(doc_origin_language)
            document.related_documents.set(related_documents)
            return redirect('documents')
    else:
        form = DocumentForm()
    return render(request, 'documents/load-document.html', {'form': form})


def content(request, id):
    """
        Возвращает контент документа в зависимости от пришедшего
        HTTP_ACCEPT в header
    """
    user_permissions = ['GA', 'UR']
    is_allowed = authenticate_credentials(get_token(request))
    if is_allowed is True:
        is_permission = check_permissions(get_token(request), user_permissions)
        if is_permission is True:
            accept_header = request.META.get('HTTP_ACCEPT')
            if accept_header is None:
                return HttpResponse(status=406)
            document = get_object_or_404(Documents, id=id)
            if accept_header == 'application/pdf':
                content_name = document.pdf_content_name
                if content_name:
                    response = HttpResponse(bytes(document.doc_pdf_content))
                    response['Content-Length'] = len(bytes(document.doc_pdf_content))
                    response['Content-Type'] = 'application/pdf'
                    response['Content-Disposition'] = 'attachment; filename="' + document.pdf_content_name + '"' # NoQa
                    return response
                else:
                    return HttpResponse(status=204)
            elif accept_header == 'image/jpg':
                content_name = document.image_contemt_name
                if content_name:
                    response = HttpResponse(bytes(document.doc_image_content))
                    response['Content-Length'] = len(bytes(document.doc_image_content))
                    response['Content-Type'] = 'image/jpg'
                    response['Content-Disposition'] = 'attachment; filename="' + document.image_contemt_name + '"' # NoQa
                    return response
                else:
                    return HttpResponse(status=204)
            elif accept_header == 'text/html':
                doc_html_content = document.doc_html_content
                if doc_html_content:
                    response = HttpResponse(doc_html_content)
                    response['Content-Type'] = 'text/html'
                    return response
                else:
                    return HttpResponse(status=204)
        else:
            return JsonResponse({'response': is_permission})
    else:
        return JsonResponse({'response': is_allowed})


class DocumentAPIView(generics.RetrieveAPIView):
    """
    Возвращает полный список полей документа
    """
    permission_classes = (IsRoleUR|IsRoleRD|IsRoleBL|IsRoleEX|IsAdmin, )
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer


class ShortDocumentAPIView(generics.RetrieveAPIView):
    """
    Возвращает краткий список полей документа
    """
    permission_classes = (IsRoleUR|IsRoleRD|IsRoleBL|IsRoleEX|IsAdmin, )
    queryset = Documents.objects.all()
    serializer_class = ShortDocumentsSerializer


class DocumentsListAPIView(generics.ListAPIView):
    """
    Возвращает список всех документов
    """
    permission_classes = (IsRoleUR|IsRoleRD|IsRoleBL|IsRoleEX|IsAdmin, )
    queryset = Documents.objects.all()
    serializer_class = DocumentsListSerializer


class NoticeDocumentAPIView(generics.RetrieveAPIView):
    """
    Возвращает данные о заметках в документе
    """
    serializer_class = DocumentsNoticeSerializer
    queryset = DocumentsNotice.objects.all()

    def get_object(self):
        user = self.request.user
        document_id = self.kwargs['pk']
        queryset = get_object_or_404(DocumentsNotice, user=user, document=document_id)
        return queryset


class NoticeCreateDocumentAPIView(generics.CreateAPIView):
    """
    создание сущности данные о заметках в документе
    """
    serializer_class = DocumentsNoticeSerializer
    queryset = DocumentsNotice.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = DocumentsNoticeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            document = get_object_or_404(Documents, id=self.kwargs['pk'])
            try:
                serializer.save(user=self.request.user, document=document)
            except IntegrityError:
                raise ValidationError({'unique': 'Not a unique combination user and document.'})
        return Response(serializer.data)


class TextSettingsAPIView(generics.UpdateAPIView,
                          generics.DestroyAPIView):
    """
    Работа с настройками закладок
    """
    permission_classes = (HandleOwnerOnlyDocumentsNotice|IsAdmin, )
    serializer_class = TextSettingsSerializer
    queryset = TextSetings.objects.all()


class CreateTextSettingsAPIView(generics.CreateAPIView):
    """
    Создание закладки
    """
    serializer_class = TextSettingsSerializer
    queryset = TextSetings.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = TextSettingsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            document_notice_id = self.kwargs['pk']
            notice_document = get_object_or_404(DocumentsNotice,
                                                id=document_notice_id,
                                                user=self.request.user)
            serializer.save()
        text_setting = TextSetings.objects.get(id=serializer.data['id'])
        notice_document.text_settings.add(text_setting)
        return Response(serializer.data)


class CommentsAPIView(generics.UpdateAPIView,
                      generics.DestroyAPIView):
    """
    Работа с комментариями в документе
    """
    permission_classes = (HandleOwnerOnlyDocumentsNotice|IsAdmin, )
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()


class CreateCommentsAPIView(generics.CreateAPIView):
    """
    Создание комментария в документе
    """
    serializer_class = CommentsSerializer
    queryset = Comments.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            document_notice_id = self.kwargs['pk']
            notice_document = get_object_or_404(DocumentsNotice,
                                                id=document_notice_id,
                                                user=self.request.user)
            serializer.save()
        comment = Comments.objects.get(id=serializer.data['id'])
        notice_document.comments.add(comment)
        return Response(serializer.data)


class RateDocumentAPIView(generics.CreateAPIView):
    """
    Оставить оценку на документ
    """
    permission_classes = (IsRoleUR | IsRoleRD | IsRoleBL | IsRoleEX | IsAdmin,)
    serializer_class = RateDocumentsSerializer

    def create(self, request, *args, **kwargs):
        data = {
            'value': request.data['value'],
            'user': request.user.id,
            'document': self.kwargs['pk']
        }

        if 1 > int(request.data['value']) or int(request.data['value']) > 5:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)
        # если пользователь уже ставил оценку на документ вернуть 400
        if serializer.is_valid(raise_exception=True) \
                and not serializer.validated_data['document'].ratings.filter(user=serializer.validated_data['user']):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
