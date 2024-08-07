import requests
from django.shortcuts import render

def home(request):
    signed_in = request.user.is_authenticated
    return render(request, 'core/templates/home/home.html', {'signed_in': signed_in})


