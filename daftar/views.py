import requests
import daftar
from daftar.models import User


# Global Function for all applications
def verify_token(request):
    if 'token' in request.session:
        token = request.session['token']
        hed = {'Authorization': 'Bearer ' + token}

        r = requests.get(daftar.settings.DAFTAR_HOST + "/user", headers=hed)
        data = r.json()
        if r.status_code == requests.codes.ok:
            user = User()
            user.id = data['_id']['$oid']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.dob = data['dob']
            user.isUser = data['role'] == 'user'
            user.token = token
            return True
        else:
            return False
    else:
        return False
