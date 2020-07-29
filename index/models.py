import requests
from django import forms

import daftar
from daftar.models import User


class LoginForm(forms.Form):
    email = forms.CharField(max_length= 100)
    password = forms.CharField(widget=forms.PasswordInput())

    def login(self, verify_pin=None):
        data = {
            'email': self.cleaned_data['email'],
            'password': self.cleaned_data['password']
        }

        if verify_pin is not None:
            data['pin'] = verify_pin

        r = requests.post(daftar.settings.DAFTAR_HOST + "/auth/login", json=data)
        if r.status_code == requests.codes.ok:
            return r.json()['token']
        else:
            print(r.json())
            return None


class SignupForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    dob = forms.CharField(max_length=10)
    role = forms.CharField(max_length=10)

    def signup(self):
        data = {
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'email': self.cleaned_data['email'],
            'password': self.cleaned_data['password'],
            'dob': self.cleaned_data['dob'],
            'role': self.cleaned_data['role']
        }

        r = requests.post(daftar.settings.DAFTAR_HOST + "/auth/signup", json=data)
        if r.status_code == requests.codes.ok:
            return True
        else:
            return False
