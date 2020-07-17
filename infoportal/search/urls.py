from django.urls import path

from .views import search_auto_completions, search_history, search_text, \
    SearchViewSet, AutoCompletionViewSet, SearchHistoryViewSet

urlpatterns = [
    path('auto_completions', search_auto_completions),
    path('text', search_text),
    path('history', search_history),

    path('search', SearchViewSet),
    path('auto_completion', AutoCompletionViewSet),
    path('search_history', SearchHistoryViewSet)

]
