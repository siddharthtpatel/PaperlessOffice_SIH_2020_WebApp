from django.shortcuts import render, redirect

from daftar.views import verify_token
from index.models import LoginForm, SignupForm


def index(request, verify_pin=None):
    if verify_pin is not None:
        request.session['pin'] = verify_pin

    if verify_token(request):
        return redirect('/dashboard')
    else:
        return render(request, 'index.html', {})


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            if 'pin' in request.session:
                token = login_form.login(request.session['pin'])
                del request.session['pin']
                request.session.modified = True
            else:
                token = login_form.login()

            if token is not None:
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
        else:
            return render(request, 'index.html', {'signup_error': True})