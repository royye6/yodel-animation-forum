import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .forms import StaffTopicForm, UserTopicForm
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Topic
from .serializers import TopicSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# def topic(request):
#     return render(request, 'topic.html')


@login_required
def new_topic(request):
    profile = request.user.profile if request.user.is_authenticated else None
    
    if request.user.is_staff:
        form = StaffTopicForm(request.POST or None)
    else:
        form = UserTopicForm(request.POST or None)

    if request.method == 'POST':
       
            if form.is_valid():
                try:
                    topic = form.save(commit=False)
                    topic.user = request.user
                    topic.save()
                    messages.success(request, "Topic created successfully!")
                    return redirect('/')
                
                except IntegrityError as e:
                    messages.error(request, "An error occurred. Please check your uploaded data")
                    print(e)
                    return render(request, 'content/newtopic.html', context)
        
    context = {
        "profile": profile,
        "signed_in": request.user.is_authenticated,
        "form": form
    }
    return render(request, 'content/newtopic.html', context)


def topic_detail(request, slug):
    return render(request, '/')

def topic_paginated_api(request):
    page = request.GET.get('page', 1)
    page_size = 14

    paginator = Paginator(Topic.objects.all(), page_size)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        messages.error(request, 'Page number is not an integer')
        topics = paginator.page(1)
    except EmptyPage:
        messages.error(request, 'Page out of range')
        topics = paginator.page(paginator.num_pages)

    serializer_class = TopicSerializer
    serializer = serializer_class(topics, many=True)
    return JsonResponse({'topics': serializer.data, 'next': topics.next_page_number()})