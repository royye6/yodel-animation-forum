import requests
from django.shortcuts import render, redirect
from users.models import Profile, User
from content.models import Topic, Reply
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages


def home(request):
    signed_in = request.user.is_authenticated
    profile = None

    if signed_in:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect('/')

    pinned_topics = Topic.objects.filter(is_pinned=True)
    regular_topics = Topic.objects.filter(is_pinned=False).order_by('-created_at')
    all_topics = list(pinned_topics) + list(regular_topics)
  

    paginator = Paginator(all_topics, settings.PAGE_SIZE)
    topics_pages = paginator.page(1)

    context = {
        "profile": profile,
        "signed_in": signed_in,
        "topics": all_topics,
        "topics_page": topics_pages,
    }

    if request.htmx:
        topics_list()

    return render(request, 'core/templates/home/home.html', context)


def topics_list(request):
    page = request.GET.get('page', 1)

    pinned_topics = Topic.objects.filter(is_pinned=True)
    regular_topics = Topic.objects.filter(is_pinned=False).order_by('-created_at')
    all_topics = list(pinned_topics) + list(regular_topics)

    paginator = Paginator(all_topics, settings.PAGE_SIZE)
    topics_pages = paginator.page(1)

    context = {
        "topics_page": paginator.page(page)
    }
    print('Pagination is working')
    return render(request, 'core/templates/home/home.html#topics_partial', context)


def members(request):
    profile = request.user.profile if request.user.is_authenticated else None
    users = User.objects.order_by('-date_joined').all()

    context = {
        "profile": profile,
        "signed_in": request.user.is_authenticated,
        "users": users
    }
    return render(request, 'members/members.html', context)
    

def staff(request):
    profile = request.user.profile if request.user.is_authenticated else None
    users = User.objects.order_by('-date_joined').all()

    context = {
        "profile": profile,
        "signed_in": request.user.is_authenticated,
        "users": users
    }
    return render(request, 'members/staff.html', context)


def support(request):
    profile = request.user.profile if request.user.is_authenticated else None
    users = User.objects.order_by('-date_joined').all()

    if not request.user.is_authenticated:
        messages.info(request, "Login to access this page")
        return redirect('login')
    
    context = {
        "profile": profile,
        "signed_in": request.user.is_authenticated,
        "users": users
    }
    return render(request, 'members/support.html', context)