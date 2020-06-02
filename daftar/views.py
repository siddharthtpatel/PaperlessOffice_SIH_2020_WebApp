import requests
import daftar
from daftar.models import User


# Global Function for all applications
def verify_token(request):
    if 'token' in request.session:
        token = request.session['token']
        hed = {'Authorization': 'Bearer ' + token}

        r = requests.get(daftar.settings.DAFTAR_HOST + "/user", headers=hed)
        print(r)
        if r.status_code == requests.codes.ok:
            user = User()
            user.data = r.json()
            return True
        else:
            return False
    else:
        return False
