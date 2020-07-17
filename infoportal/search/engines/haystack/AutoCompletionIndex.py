from haystack import indexes

from .search.models import AutoCompletion


class AutoCompletionIndex(indexes.SearchIndex, indexes.Indexable):
    search_text = indexes.CharField(document=True, model_attr='search_text')

    def get_model(self):
        return AutoCompletion

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
