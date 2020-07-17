from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token

CustomUserModel = get_user_model()

def check_permissions(key, user_permissions):
    token = Token.objects.get(key=key)
    user = CustomUserModel.objects.get(id=token.user_id)
    if user.role in user_permissions:
        return True
    elif user.is_superuser == 1:
        return True
    else:
        return 'Данный пользователь не имеет доступа'
