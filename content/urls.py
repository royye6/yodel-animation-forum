from django.urls import path
from . import views


urlpatterns = [
    path('topic', views.new_topic, name='topic'),
    path('new-topic', views.new_topic, name='newtopic'),
    path('topic/<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('api/topics/', views.topic_paginated_api, name='topic_api'),
]