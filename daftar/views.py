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
            user.email = data['email']
            user.public_key = data['public_key']
            user.private_key = data['private_key']
            user.costOfPaper = data['costOfPaper']
            user.dob = data['dob']
            user.role = data['role']
            user.token = token
            if user.role == 'user':
                user.type = 'user'
            elif user.role == 'admin':
                user.type = 'admin'
            else:
                user.type = 'authority'

            return True
        else:
            return False
    else:
        return False
