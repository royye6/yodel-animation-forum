from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('t/list/', views.topics_list, name='topics_list'),
]