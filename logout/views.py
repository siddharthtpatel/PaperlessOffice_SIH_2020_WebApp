import requests
from django.http import HttpResponse
from django.shortcuts import redirect

import daftar
from daftar.models import User


def logout(request):
    hed = {'Authorization': 'Bearer ' + User().token}

    r = requests.delete(daftar.settings.DAFTAR_HOST + "/auth/logout", headers=hed)

    if r.status_code == requests.codes.ok:
        request.session.flush()
        return redirect('/')
    else:
        return HttpResponse("Error: Logging out!")
