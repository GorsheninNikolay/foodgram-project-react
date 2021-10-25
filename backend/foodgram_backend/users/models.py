from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    is_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='block_for_yourself'
            ),
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            ),
        ]
