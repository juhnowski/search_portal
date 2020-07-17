from rest_framework.authtoken.models import Token
from users.utils.authentication import token_expire_handler


def authenticate_credentials(key):
    try:
        token = Token.objects.get(key=key)
    except Token.DoesNotExist:
        return 'Неверный токен'

    if not token.user.is_active:
        return 'Пользователь не активный'

    is_expired, token = token_expire_handler(token)
    if is_expired:
        return 'Время токена истекло'

    return True
