from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from main.models import LoginForm


def index(request):
    return render(request, 'index.html', {})


def login(request):
    print(request.body)
    token = '';

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)

        if loginForm.is_valid():
            token = loginForm.login()

            if token:
                return redirect('/dashboard')
            else:
                return HttpResponse('Error')