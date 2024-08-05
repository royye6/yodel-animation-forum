from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django_recaptcha.fields import ReCaptchaField

# class RegisterForm(forms.Form):
#     username = forms.CharField(label='Your Name', max_length=100, required=True)
#     email = forms.EmailField(label='Your Email', required=True)
#     password = forms.CharField(label='Your Password', required=True, widget=forms.PasswordInput())
#     password2 = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput())
#     captcha = ReCaptchaField()


# class LoginForm(forms.Form):
#     username = username = forms.CharField(label='Your Name', max_length=100, required=True)
#     email = forms.EmailField(label='Your Email', required=True)
#     password = forms.CharField(label='Your Password', required=True, widget=forms.PasswordInput())
#     captcha = ReCaptchaField()
    

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    captcha = ReCaptchaField()


class LoginForm(AuthenticationForm):
    captcha =ReCaptchaField()