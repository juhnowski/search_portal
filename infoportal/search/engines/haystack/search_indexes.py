# nstall the package:
# #
# #     Latest stable (2.6.0) off PyPI: pip install django-haystack
# #     Latest dev off GitHub: pip install -e git+https://github.com/django-haystack/django-haystack.git@master#egg=django-haystack
# #
# # Add haystack to your INSTALLED_APPS.
# # Create search_indexes.py files for your models.
# # Setup the main SearchIndex via autodiscover.
# # Include haystack.urls to your URLconf.

# TODO: Download and copy jdbc driver jar for postgres to “contrib/dataimporthandler/lib” folder
#
#           https://jdbc.postgresql.org/download.html
#
#           https://jdbc.postgresql.org/download/postgresql-42.2.2.jar

# 0 - Установка
# скачать и распаковать solr  https://www.apache.org/dyn/closer.lua/lucene/solr/8.3.1/solr-8.3.1.tgz
# добавить в path

# 1 - Запуск
# solr start
# htp://localhost:8983/solr - запустился

# 2 - Создание ядра
# cd backend/infoportal/search/engines/haystack
# cp solrconfig.xml /home/ilya/solr-8.3.1/server/solr/infoportal/conf/solrconfig.xml
#

# solr create -c infoportal -d solr

# <field name="doc_kind" type="string" indexed="true" stored="true"/>
# <field name="doc_mark" type="string" indexed="true" stored="true"/>
# <field name="doc_name_ru" type="string" indexed="true" stored="true"/>
# <field name="doc_name_en" type="string" indexed="true" stored="true"/>
# <field name="doc_annotation" type="string" indexed="true" stored="true"/>
# <field name="doc_comment" type="string" indexed="true" stored="true"/>
# <field name="doc_full_mark" type="string" indexed="true" stored="true"/>
# <field name="tk_rus" type="string" indexed="true" stored="true"/>
# <field name="mtk_dev" type="string" indexed="true" stored="true"/>
# <field name="keywords" type="string" indexed="true" stored="true"/>
# <field name="doc_assign_date" type="pdate" indexed="true" stored="true"/>
# <field name="doc_effective_date" type="pdate" indexed="true" stored="true"/>
# <field name="doc_restoration_date" type="pdate" indexed="true" stored="true"/>
# <field name="doc_restoration_date" type="pdate" indexed="true" stored="true"/>
# <field name="search_text" type="string" indexed="true" stored="true"/>


from haystack import indexes

from infoportal.documents.models import Documents
from infoportal.search.models import AutoCompletion


class DocumentsIndex(indexes.SearchIndex, indexes.Indexable):
    doc_kind = indexes.CharField(model_attr='doc_kind')
    doc_mark = indexes.CharField(model_attr='doc_mark')
    doc_name_ru = indexes.CharField(model_attr='doc_name_ru')
    doc_name_en = indexes.CharField(model_attr='doc_name_en')
    doc_annotation = indexes.CharField(model_attr='doc_annotation')
    doc_comment = indexes.CharField(model_attr='doc_comment')
    doc_full_mark = indexes.CharField(model_attr='doc_full_mark')
    tk_rus = indexes.CharField(model_attr='tk_rus')
    mtk_dev = indexes.CharField(model_attr='mtk_dev')
    keywords = indexes.CharField(model_attr='keywords')
    doc_assign_date = indexes.DateField(model_attr='doc_assign_date')
    doc_effective_date = indexes.DateField(model_attr='doc_effective_date')
    doc_restoration_date = indexes.DateField(model_attr='doc_restoration_date')

    def prepare(self, obj):
        self.prepared_data = super(DocumentsIndex, self).prepare(obj)
        return self.prepared_data

    def get_model(self):
        return Documents

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class AutoCompletionIndex(indexes.SearchIndex, indexes.Indexable):
    search_text = indexes.CharField(model_attr='search_text')

    def prepare(self, obj):
        self.prepared_data = super(AutoCompletionIndex, self).prepare(obj)
        return self.prepared_data

    def get_model(self):
        return AutoCompletion

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
