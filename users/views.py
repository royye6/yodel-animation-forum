from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm, UserProfileUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from users.models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash 


def user_register(request):
    context = {'form': RegisterForm}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, 'Registered successfully')
            return redirect('/')
        else:
            messages.info(request, 'Please fill in all the required fields')
            return render(request, 'users/templates/users/register.html', context)
    else:
        return render(request, 'users/templates/users/register.html', context)


def user_login(request):
    context = {'form': LoginForm}
    next_url = request.META.get('HTTP_REFERER', '/')

    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Logged in successfully')
            # next_url = request.GET.get('next', '/')
            return redirect('/') 
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'users/templates/users/login.html', context)
    else:
        return render(request, 'users/templates/users/login.html', context)
    

@login_required
def user_logout(request):
    auth.logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('/')


@login_required
def profile(request):
    signed_in = request.user.is_authenticated
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        u_form = UserProfileUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.warning(request, 'Error updating profile')
            context = {
            "profile": profile,
            "signed_in": signed_in,
            "u_form": u_form,
            "p_form": p_form
            }
            return render(request, 'users/templates/users/profile.html', context)
       
    else:
        u_form = UserProfileUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            "profile": profile,
            "signed_in": signed_in,
            "u_form": u_form,
            "p_form": p_form
        }
        return render(request, 'users/templates/users/profile.html', context)


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


