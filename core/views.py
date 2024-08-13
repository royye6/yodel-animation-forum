import requests
from django.shortcuts import render, redirect
from users.models import Profile, User
from content.models import Topic


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

    context = {
        "profile": profile,
        "signed_in": signed_in,
        "topics": all_topics
    }
    return render(request, 'core/templates/home/home.html', context)


