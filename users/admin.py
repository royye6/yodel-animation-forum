from django.contrib import admin
from users.models import User, Profile
from content.models import Topic, Reply


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'full_name']
    list_display = ['id', 'username', 'full_name', 'email', 'last_login', 'date_joined', 'is_superuser', 'is_staff',]


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display =['id', 'image', 'status', 'followers', 'following', 'posts', 'likes', 'posts_liked']


class TopicAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'id']
    list_display = ['id', 'user', 'slug', 'title', 'image', 'content', 'created_at']


class ReplyAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'id']
    list_display = ['id', 'topic', 'reply_image', 'content', 'created_at']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Reply, ReplyAdmin)