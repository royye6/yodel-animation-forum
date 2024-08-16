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
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# def topic(request):
#     return render(request, 'topic.html')


@login_required
def new_topic(request):
    profile = request.user.profile if request.user.is_authenticated else None
    
    if request.user.is_staff:
        form = StaffTopicForm(request.POST, request.FILES)
    else:
        form = UserTopicForm(request.POST, request.FILES)

    if request.method == 'POST':
            if form.is_valid():
                try:
                    topic = form.save(commit=False)
                    topic.user = request.user
                    if 'file' in request.FILES:
                        uploaded_file = request.FILES['image']
                        topic.image = uploaded_file
                    else:
                        print("error uploading image file")
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
    profile = request.user.profile if request.user.is_authenticated else None
    topic = get_object_or_404(Topic, slug=slug)
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
    video_extensions = ('.mp4', '.webm')
    is_image = topic.file.name.endswith(image_extensions)
    is_video = topic.file.name.endswith(video_extensions)

    context = {
        "profile": profile,
        "signed_in": request.user.is_authenticated,
        "topic": topic,
        "is_image": is_image,
        "is_video": is_video
    }
    return render(request, 'content/topic.html', context)


def topic_paginated_api(request):
    page = request.GET.get('page', 1)
    page_size = 5

    pinned_topics = Topic.objects.filter(is_pinned=True)
    pinned_serializer = TopicSerializer(pinned_topics, many=True)

    paginator = Paginator(Topic.objects.filter(is_pinned=False), page_size)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        return Response({'error': 'Page number is not an integer'}, status=status.HTTP_400_BAD_REQUEST)
    except EmptyPage:
        return Response({'error': 'No more topics'}, status=status.HTTP_404_NOT_FOUND)

    serializer_class = TopicSerializer
    serializer = serializer_class(topics, many=True)
    return JsonResponse({
        'pinned_topics': pinned_serializer.data,
        'topics': serializer.data, 
        'next': topics.next_page_number() if topics.has_next() else None
        })