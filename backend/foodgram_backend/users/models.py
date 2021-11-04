from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='Email'
        )
    username = models.CharField(
        max_length=150, unique=True, verbose_name='Логин'
        )
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    password = models.CharField(max_length=150, verbose_name='Пароль')
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписан')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='followers', verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='followings', verbose_name='Подписка на пользователя'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='block_for_yourself'
            ),
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            ),
        ]
