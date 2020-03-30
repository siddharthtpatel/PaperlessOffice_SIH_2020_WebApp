import requests
from django import forms

import daftar


class LoginForm(forms.Form):
    email = forms.CharField(max_length= 100)
    password = forms.CharField(widget=forms.PasswordInput())

    def login(self):
        data = {
            'email': self.cleaned_data['email'],
            'password': self.cleaned_data['password']
        }

        r = requests.post(daftar.settings.DAFTAR_HOST + "/auth/login", json=data)
        if r.status_code == requests.codes.ok:
            return r.json()['token']
        else:
            return None;