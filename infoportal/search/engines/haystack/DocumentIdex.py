from haystack import indexes

from .documents.models import Documents


class DocumentsIndex(indexes.SearchIndex, indexes.Indexable):
    doc_kind = indexes.CharField(model_attr='doc_kind')
    doc_mark = indexes.CharField(model_attr='doc_mark')
    doc_name_ru = indexes.CharField(document=True, model_attr='doc_name_ru')
    doc_name_en = indexes.CharField(model_attr='doc_name_en')
    doc_annotation = indexes.CharField(model_attr='doc_annotation')
    doc_comment = indexes.CharField(model_attr='doc_comment')
    doc_full_mark = indexes.CharField(model_attr='doc_full_mark')
    tk_rus = indexes.CharField(model_attr='tk_rus')
    mtk_dev = indexes.CharField(model_attr='mtk_dev')
    keywords = indexes.CharField(model_attr='keywords')
    doc_assign_date = indexes.DateTimeField(model_attr='doc_assign_date')
    doc_effective_date = indexes.DateTimeField(model_attr='doc_effective_date')
    doc_restoration_date = indexes.DateTimeField(model_attr='doc_restoration_date')

    def get_model(self):
        return Documents

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
