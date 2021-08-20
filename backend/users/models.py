from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=200
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=200
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=200
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Пользователь подписчик')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь на которого подписываемся')
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name='Время создания'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
