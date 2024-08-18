import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import User
from .forms import StaffTopicForm, UserTopicForm, ReplyForm
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from .models import Topic, Reply
from .serializers import TopicSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404



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
                        uploaded_file = request.FILES['file']
                        topic.image = uploaded_file
                    else:
                        print("error uploading image file")
                    topic.save()
                    messages.success(request, "Topic created successfully!")
                    return redirect('/')
                
                except IntegrityError as e:
                    messages.error(request, "An error occurred. Please check your uploaded data")
                    print(e)
                    return render(request, 'content/new_topic.html', context)
        
    context = {
        "profile": profile,
        "signed_in": request.user.is_authenticated,
        "form": form
    }
    return render(request, 'content/new_topic.html', context)


def topic_detail(request, slug):
    profile = request.user.profile if request.user.is_authenticated else None
    topic = get_object_or_404(Topic, slug=slug)

    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')
    video_extensions = ('.mp4', '.webm')
    is_image = topic.file.name.endswith(image_extensions)
    is_video = topic.file.name.endswith(video_extensions)

    reply_form = ReplyForm(request.POST, request.FILES)
    replies = Reply.objects.filter(topic=topic)

    newest_member = User.objects.order_by('-date_joined').first()
    total_members = User.objects.count()
    total_topics = Topic.objects.count()
    total_replies = Reply.objects.count()
    total_posts = total_topics + total_replies

    if request.method == 'POST':
        if reply_form.is_valid():
            try:
                reply = reply_form.save(commit=False)
                reply.user = request.user
                reply.topic_id = topic.id
                if 'reply_file' in request.FILES:
                    uploaded_file = request.FILES['reply_file']
                    reply.reply_file = uploaded_file
                else:
                    None   
                reply.save()
                messages.success(request, "Reply sent successfully!")
            
            except IntegrityError as e:
                messages.error(request, "An error occurred. Please check your uploaded data")
                print(e)


    context = {
        "profile": profile,
        "signed_in": request.user.is_authenticated,
        "topic": topic,
        "is_image": is_image,
        "is_video": is_video,
        "reply_form": reply_form,
        "replies": replies,
        "newest_member": newest_member,
        "total_members": total_members,
        "total_topics": total_topics,
        "total_posts": total_posts
    }
    return render(request, 'content/topic.html', context)


def activity(request):
    profile = request.user.profile if request.user.is_authenticated else None

    replies = Reply.objects.order_by('-created_at').all()
    total_replies_per_post = Reply.objects.select_related('topic').order_by('created_at').all()
    context = {
        "profile": profile,
        "signed_in": request.user.is_authenticated,
        "replies": replies,
        "total_replies_per_post": total_replies_per_post
    }
    return render(request, 'content/activity.html', context)


def gallery(request):
    profile = request.user.profile if request.user.is_authenticated else None
    topics = Topic.objects.order_by('-created_at').all()

    context = {
        "profile": profile,
        "signed_in": request.user.is_authenticated,
        "topics": topics
    }
    return render(request, 'content/gallery.html', context)


def topic_paginated_api(request):
    page = request.GET.get('page', 1)
    page_size = 6

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