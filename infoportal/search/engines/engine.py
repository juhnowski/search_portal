from django.conf import settings
from django.http import JsonResponse

from .simple.engine import simple_search_text, simple_search_auto_completions
from .solr.engine import solr_search_text, solr_search_auto_completions
from .sphinx.engine import sphinx_search_text, sphinx_search_auto_completions
from .whoosh.engine import whoosh_search_text, whoosh_search_auto_completions


def engine_search_text(search_serializer, page, page_size, user_id):
    if settings.SEARCH_ENGINE.get('name') == 'simple':
        return simple_search_text(search_serializer, page, page_size, user_id)
    elif settings.SEARCH_ENGINE.get('name') == 'sphinx':
        return sphinx_search_text(search_serializer, page, page_size, user_id)
    elif settings.SEARCH_ENGINE.get('name') == 'solr':
        return solr_search_text(search_serializer, page, page_size, user_id)
    elif settings.SEARCH_ENGINE.get('name') == 'whoosh':
        return whoosh_search_text(search_serializer, page, page_size, user_id)
    else:
        return JsonResponse({'documents': [], 'count': 0})


def engine_search_auto_completions(search_serializer):
    if settings.SEARCH_ENGINE.get('name') == 'simple':
        return simple_search_auto_completions(search_serializer)
    elif settings.SEARCH_ENGINE.get('name') == 'sphinx':
        return sphinx_search_auto_completions(search_serializer)
    elif settings.SEARCH_ENGINE.get('name') == 'solr':
        return solr_search_auto_completions(search_serializer)
    elif settings.SEARCH_ENGINE.get('name') == 'whoosh':
        return whoosh_search_auto_completions(search_serializer)
    else:
        return JsonResponse({'auto_completions': []})
