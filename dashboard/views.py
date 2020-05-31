import daftar
import json
import requests
from django.shortcuts import render


def index(request):
    head = {'Authorization': 'Bearer '+request.session['token']}
    user = requests.get(daftar.settings.DAFTAR_HOST+"/user", headers=head)
    user = json.loads(user.text)
    return render(request, 'dashboard.html', {'user': user})
