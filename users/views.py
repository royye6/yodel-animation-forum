from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm



def user_register(request):
    context = {'form': RegisterForm}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
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