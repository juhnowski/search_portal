import logging

from django.http import JsonResponse
from documents.utils.token_authentication import authenticate_credentials
from documents.utils.user_permission import check_permissions
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.utils.authentication import get_token
from users.utils.permissions import IsAdmin

from .engines.engine import engine_search_text, engine_search_auto_completions
from .engines.simple.querytexts import Query
from .models import Search, AutoCompletion, SearchHistory
from .serializers import SearchSerializer, AutoCompletionSerializer, SearchHistorySerializer

LOGGER = logging.getLogger('django')
SEARCH_QUERY = Query()


class SearchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows searches to be viewed or edited.
    """
    permission_classes = (IsAdmin,)
    queryset = Search.objects.all()
    serializer_class = SearchSerializer


class SearchHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows searche history to be viewed or edited.
    """
    permission_classes = (IsAdmin,)
    queryset = Search.objects.all()
    serializer_class = SearchHistorySerializer


class AutoCompletionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows auto completions to be viewed or edited.
    """
    permission_classes = (IsAdmin,)
    queryset = AutoCompletion.objects.all()
    serializer_class = AutoCompletionSerializer


with open('stopwords.txt', "r") as f:
    stopwords = f.read()


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def search_auto_completions(request):
    """ Автодополнение поиска необходимо отправить json в Body вида:

    { "search_text": "ВНИИПО",
      "page_size":"10"
    }"""
    user_permissions = ['GA', 'UR']
    is_allowed = authenticate_credentials(get_token(request))
    if is_allowed is True:
        is_permission = check_permissions(get_token(request), user_permissions)
        if is_permission is False:
            return JsonResponse({'response': is_permission})
    else:
        return JsonResponse({'response': is_allowed})

    search_serializer = AutoCompletionSerializer(data=request.data)

    search_serializer.is_valid()

    return engine_search_auto_completions(search_serializer)


@api_view(['POST'])
@permission_classes((AllowAny,))
def search_text(request):
    """
    Поисковый запрос необходимо отправить json в Body вида:

    { "search_text": "ВНИИПО",
      "search_options": "{'':''}",
      "page_size":"10"
    }
    """

    user_permissions = ['GA', 'UR']
    key = get_token(request)
    is_allowed = authenticate_credentials(key)
    if is_allowed is True:
        is_permission = check_permissions(get_token(request), user_permissions)
        if is_permission is False:
            return JsonResponse({'response': is_permission})
    else:
        return JsonResponse({'response': is_allowed})

    try:
        limit = int(request.GET["limit"])
        offset = int(request.GET["offset"])
        page_size = limit
        page = int(offset / limit) + 1
    except Exception as ex:
        page_size = -1
        page = 1
        LOGGER.error(f"{ex}")

    search_serializer = SearchSerializer(data=request.data)

    search_serializer.is_valid()

    try:
        token = Token.objects.get(key=key)
    except Exception as e:
        return JsonResponse(
            {"response": "user not found - internal server  error"}
        )

    return engine_search_text(search_serializer, page, page_size, token.user_id)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def search_history(request):
    user_permissions = ['GA', 'UR']
    key = get_token(request)
    is_allowed = authenticate_credentials(key)
    if is_allowed is True:
        is_permission = check_permissions(get_token(request), user_permissions)
        if is_permission is False:
            return JsonResponse({'response': is_permission})
    else:
        return JsonResponse({'response': is_allowed})

    try:
        token = Token.objects.get(key=key)
    except Exception:
        return JsonResponse({"auto_completions": []})

    result = []
    try:
        hist = SearchHistory.objects.filter(userid=token.user_id)
        for h in hist:
            result.append(hist.search.search_text)
    except Exception:
        return JsonResponse({"auto_completions": result})

    return Response({"auto_completions": result})
