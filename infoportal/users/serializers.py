from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from .models import Company

CustomUserModel = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    """сериализация компании"""
    company_name = serializers.CharField(max_length=100)
    position_сompany = serializers.CharField(max_length=100)

    class Meta:
        model = Company
        exclude = ('id', )


class UserCreateSerializer(WritableNestedModelSerializer):
    """создание пользователя"""
    company = CompanySerializer(required=False)

    def create(self, validated_data):
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = CustomUserModel
        fields = ('email', 'first_name', 'last_name', 'patronymic',
                  'phone', 'password', 'role', 'company', 'is_superuser')


class UserSerializer(WritableNestedModelSerializer):
    """update пользователя"""
    company = CompanySerializer(required=False)
    
    class Meta:
        model = CustomUserModel
        fields = ('id', 'email', 'first_name', 'last_name',
                  'patronymic', 'phone', 'company', 'role', 'is_superuser')


class UserLoginSerializer(serializers.Serializer):
    """авторизация"""
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSearchSerializer(serializers.ModelSerializer):
    """
    сериализация поиска пользователя
    """
    class Meta:
        model = CustomUserModel
        exclude = ('password',
                   'last_login',
                   'is_superuser',
                   'phone',
                   'role',
                   'is_active',
                   'is_staff',
                   'date_joined',
                   'company',
                   'groups',
                   'user_permissions')


class UserAdvancedSearchSerializer(serializers.ModelSerializer):
    """
    сериализация особого поиска пользователя
    """
    role = serializers.CharField(source='get_role_display')
    class Meta:
        model = CustomUserModel
        exclude = ('password',
                   'last_login',
                   'is_superuser',
                   'is_active',
                   'is_staff',
                   'date_joined',
                   'company',
                   'groups',
                   'user_permissions')
