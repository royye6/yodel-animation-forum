from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('t/list/', views.topics_list, name='topics_list'),
    path('members/', views.members, name='members'),
    path('staff/', views.staff, name='staff'),
    path('support/', views.support, name='support'),
]