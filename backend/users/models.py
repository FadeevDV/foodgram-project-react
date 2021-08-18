from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    """Расширение стандартной модели пользователя Django"""
    bio = models.TextField(
        blank=True,
    )
    email = models.EmailField(
        blank=False,
        unique=True,
        validators=[validate_email],
    )
    role = models.CharField(
        max_length=150,
        blank=False,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    secret = models.CharField(
        max_length=200,
    )
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )

    @property
    def is_admin(self):
        if self.role == UserRole.ADMIN or self.is_superuser:
            return True

    @property
    def is_moderator(self):
        if self.role == UserRole.MODERATOR or self.is_superuser:
            return True

    class Meta:
        ordering = (
            '-username',
        )
