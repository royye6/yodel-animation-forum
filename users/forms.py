from django import forms
from .models import Profile
from users.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django_recaptcha.fields import ReCaptchaField
from django.forms import FileInput


class RegisterForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'captcha']




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
        fields = ['image', 'full_name', 'status']
        
        # def save(self, commit=True):
        #     user = self.instance.user
        #     user.email = self.cleaned_data.get('email', user.username)
        #     user.email = self.cleaned_data.get('email', user.email)
        #     user.save()
        #     profile = super().save(commit=False)
        #     profile.save()
        #     return profile
          