import requests
from django.shortcuts import render, redirect

import daftar
from main.models import LoginForm, SignupForm


def index(request):
    if verify_token(request):
        return redirect('/dashboard')
    else:
        return render(request, 'index.html', {})

# TODO: Make this function global to all templates
def verify_token(request):
    if 'token' in request.session:
        token = request.session['token']
        hed = {'Authorization': 'Bearer ' + token}

        r = requests.get(daftar.settings.DAFTAR_HOST + "/user", headers=hed)
        if r.status_code == requests.codes.ok:
            return True
        else:
            return False
    else:
        return False


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            token = login_form.login()

            if token:
                request.session['token'] = token
                return redirect('/dashboard')
            else:
                return render(request, 'index.html', {'login_error': True})


def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            if signup_form.signup():
                return render(request, 'index.html', {'signup_success': True})
            else:
                return render(request, 'index.html', {'signup_error': True})
