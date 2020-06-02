import daftar
import json
import requests
from django.shortcuts import render
from daftar.models import User


def index(request):
    user = User()
    return render(request, 'dashboard.html', {'user': user.data})
