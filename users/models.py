from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.utils.text import slugify


STATUS = {
    ('Novice', 'Novice'),
    ('Intermediate', 'Intermediate'),
    ('Legend', 'Legend'),
}


def user_directory_path(instance, filename):
    ext =filename.split('.')[-1].lower()
    filename_without_ext = filename.split('.')[0]
    slug = slugify(filename_without_ext)
    return f'user_{instance.user.id}/{slug}.{ext}'


class User(AbstractUser):
    full_name = models.CharField(max_length=300, null=True, blank=True)
    username = models.CharField(max_length=300, unique=True)
    email = models.EmailField(unique=True)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(default='default.png', upload_to=user_directory_path, null=True, blank=True)
    full_name = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    posts = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    posts_liked = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']


    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"
    

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)