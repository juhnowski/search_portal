from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from datetime import timedelta
from django.utils import timezone
from django.conf import settings


def expires_in(token):
    """сколько осталось времени жизни токена"""
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed # NoQa
    return left_time


def is_token_expired(token):
    """проверка окончилось ли время токена или нет"""
    return expires_in(token) < timedelta(seconds=0)


def token_expire_handler(token):
    """если время токена прошло, то удаляем старый и создаем новый"""
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token


class ExpiringTokenAuthentication(TokenAuthentication):
    """Переопределение стандартного TokenAuthentication"""
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Неверный токен')

        if not token.user.is_active:
            raise AuthenticationFailed('Пользователь не активный')

        is_expired, token = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed('Время токена истекло')

        return (token.user, token)


def get_token(request):
    """Получить значение токена из request"""
    token = request.META.get('HTTP_AUTHORIZATION')
    if token is not None:
        key = token.split()[1]
        return key
    else:
        return None
