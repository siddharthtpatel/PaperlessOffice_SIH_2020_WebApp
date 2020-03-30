from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from main.models import LoginForm


def index(request):
    return render(request, 'index.html', {})


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            token = login_form.login()

            if token:
                request.session['token'] = token;
                return redirect('/dashboard')
            else:
                return render(request, 'index.html', {'login_error': True})
