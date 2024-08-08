from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth import get_user_model

# User = get_user_model


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    captcha = ReCaptchaField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValueError('Email already exists')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = Profile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    captcha =ReCaptchaField()


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        
        # def save(self, commit=True):
        #     user = self.instance.user
        #     user.email = self.cleaned_data.get('email', user.username)
        #     user.email = self.cleaned_data.get('email', user.email)
        #     user.save()
        #     profile = super().save(commit=False)
        #     profile.save()
        #     return profile
          