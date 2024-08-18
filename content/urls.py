from django.urls import path
from . import views


urlpatterns = [
    path('new-topic', views.new_topic, name='newtopic'),
    path('topic/<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('api/topics/', views.topic_paginated_api, name='topic_api'),
    path('activity', views.activity, name='activity'),
    path('gallery', views.gallery, name='gallery'),
]