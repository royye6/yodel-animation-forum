from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth


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
    # signed_in = False
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if login:
                # context['signed_in'] = signed_in
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
    return render(request, 'users/templates/users/profile.html')