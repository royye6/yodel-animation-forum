from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='users/default.png', upload_to='media/users/profile')

    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"