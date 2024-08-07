from django import forms
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django_recaptcha.fields import ReCaptchaField
    

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    captcha = ReCaptchaField()


class LoginForm(AuthenticationForm):
    captcha =ReCaptchaField()


class ProfileUpdateForm(forms.ModelForm):
    model = Profile
    fields = ['image']