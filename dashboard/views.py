from django.shortcuts import render
from daftar.models import User
from daftar.views import verify_token


def index(request):
    if verify_token(request):
        return render(request, 'dashboard.html', {'first_name': User().first_name})
    else:
        return render(request, 'index.html', {})
