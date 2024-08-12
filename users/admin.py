from django.contrib import admin
from users.models import User, Profile


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'full_name']
    list_display = ['id', 'username', 'full_name', 'email', 'last_login', 'date_joined', 'is_superuser', 'is_staff',]


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display =['id', 'image', 'status', 'followers', 'following', 'posts', 'likes', 'posts_liked']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)