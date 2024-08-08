from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm, UserProfileUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth

from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash 


def user_register(request):
    context = {'form': RegisterForm}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Please fill in all the required fields')
            return render(request, 'users/templates/users/register.html', context)
    else:
        return render(request, 'users/templates/users/register.html', context)


def user_login(request):
    context = {'form': LoginForm}
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/') 
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'users/templates/users/login.html', context)
    else:
        return render(request, 'users/templates/users/login.html', context)
    

@login_required
def user_logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def profile(request):
    signed_in = request.user.is_authenticated
    return render(request, 'users/templates/users/profile.html', {'signed_in': signed_in})


@login_required
def settings(request):
    return render(request, 'users/templates/users/_partials/settings.html')


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid() and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            update_session_auth_hash(request, user_form.instance)
            return redirect('/')
        else:
            print(user_form.errors, profile_form.errors)
            print("error updating profile")
            return redirect('profile')
    else:
        user_form = UserProfileUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)
    context = {'user_form': user_form, 'profile_form': profile_form, 'password_form': password_form}
    return render(request, 'users/templates/users/_partials/edit.html', context)


