from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username', 'email', 'first_name', 'last_name', 'password']}), # noqa
    ]
    list_display = ('id', 'username', 'email', )
    list_filter = ('email', 'username', )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'following', )
