from django.db import models
from users.models import User, Profile
from django.utils.text import slugify
from django.db.models.signals import pre_save


def user_directory_path(instance, filename): 
    ext = filename.split('.')[-1].lower()
    filename_without_ext = filename.split('.')[0]
    slug = slugify(filename_without_ext)
    return f'user_{instance.user.id}/content/{slug}.{ext}'

    
class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    content = models.TextField(max_length=50000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.title} By {self.user}, {self.created_at}"


def slugify_instance_title(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
pre_save.connect(slugify_instance_title, sender=Topic)


class Reply(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_image = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    content = models.TextField(max_length=50000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user}'s reply to {self.topic}"