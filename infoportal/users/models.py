from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
#from django.contrib.auth.models import UserManager

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class Company(models.Model):
    company_name = models.CharField('Название', max_length=100)
    position_сompany = models.CharField('Должность', max_length=100, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'компания'
        verbose_name_plural = 'Компании'


ROLE_CHOICES = (
    ('GA', 'Админ группы'),
    ('BL', 'Библиотека'),
    ('RD', 'Читатель'),
    ('UR', 'Пользователь'),
    ('EX', 'Эксперт'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Электронная почта', unique=True)
    #username = models.CharField('Имя пользователя', max_length=50)
    first_name = models.CharField('Имя', max_length=30, blank=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True)
    patronymic = models.CharField('Отчество', max_length=30, blank=True)
    # TODO: сделать валидацию phone
    phone = models.CharField('Телефон', max_length=30, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True) # NoQa
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    is_active = models.BooleanField('Активный', default=True, 
                                    help_text='Если пользователь активный')
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now) # NoQa

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
