from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import username_value_not_me

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
ROLES = [
    (ADMIN, 'admin'),
    (MODERATOR, 'moderator'),
    (USER, 'user'),
]

class User(AbstractUser):

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator, username_value_not_me],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Биография',
        null=True,
        blank=True
    )
    confirmation_code = models.CharField(
        verbose_name='код подтверждения',
        max_length=255,
        blank=False,
    )
    
    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
