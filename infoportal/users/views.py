from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from .serializers import UserSerializer, UserLoginSerializer, \
    UserCreateSerializer, UserSearchSerializer, UserAdvancedSearchSerializer
from users.utils.authentication import token_expire_handler, expires_in, \
    get_token
from users.utils.permissions import *

CustomUserModel = get_user_model()


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """Авторизация пользователя
    необходимо отправить json в Body вида:

    { "email": "example@example.com",
      "password": "123456"
    }"""

    login_serializer = UserLoginSerializer(data=request.data)
    if not login_serializer.is_valid():
        return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST) # NoQa

    user = authenticate(
            username=login_serializer.data['email'],
            password=login_serializer.data['password']
        )
    if not user:
        return Response({'detail': 'Неправильные данные для создания аккаунта'}, # NoQa
                        status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)

    is_expired, token = token_expire_handler(token)
    user_serialized = UserSerializer(user)

    return Response({
        'user': user_serialized.data,
        'expires_in': expires_in(token),
        'token': token.key
    }, status=status.HTTP_200_OK)


class UserListAPIView(generics.ListAPIView):
    """Получение списка пользователей"""
    permission_classes = (IsAdmin, )
    serializer_class = UserSerializer
    queryset = CustomUserModel.objects.filter(is_active=True, is_superuser=False)


class UserRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение, изменение, удаление отдельного пользователя по pk"""
    lookup_field = 'pk'
    permission_classes = (IsAdmin|GetAndUpdateOwnerOnly, )
    serializer_class = UserSerializer
    queryset = CustomUserModel.objects.filter(is_active=True)


class UserCreateAPIView(generics.CreateAPIView):
    """Создание пользователя"""
    permission_classes = (IsAdmin, )
    serializer_class = UserCreateSerializer
    queryset = CustomUserModel.objects.all()


@api_view(["GET"])
def check_token(request):
    """Проверка токена"""
    key = get_token(request)
    try:
        token = Token.objects.get(key=key)
        user = CustomUserModel.objects.get(id=token.user_id)
        user_serialized = UserSerializer(user)
        return Response({
            'user': user_serialized.data,
            }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class UserSearchAPIView(generics.ListAPIView):
    """
    поиск пользователя по его email
    """
    serializer_class = UserSearchSerializer
    permission_classes = (IsRoleUR|IsAdmin, )
    pagination_class = None

    def get_queryset(self):
        email = self.request.query_params.get('search', None)
        queryset = CustomUserModel.objects.filter(email=email)
        return queryset


class UserAdvancedSearchAPIView(generics.ListAPIView):
    """
    расширеный поиск пользователя
    """
    serializer_class = UserAdvancedSearchSerializer
    permission_classes = (IsRoleUR|IsAdmin, )

    
    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        queryset = CustomUserModel.objects.filter(Q(email=search_query) |
                       Q(first_name__trigram_similar=search_query) |
                       Q(last_name__trigram_similar=search_query) |
                       Q(patronymic__trigram_similar=search_query) |
                       Q(company__company_name__trigram_similar=search_query))
        return queryset
