from django.shortcuts import render, redirect

from daftar.functions import get_storage_documents, get_applications
from daftar.models import User
from daftar.views import verify_token


def index(request):
    if verify_token(request):
        docs = get_storage_documents(limit=4)
        applications = get_applications(limit=3)

        if docs is False:
            # TODO: Error handling
            print('Error Loading Documents')
            return

        if applications is False:
            # TODO: Error handling
            print('Error Loading Applications')

        return render(request, 'dashboard.html', {'title': 'Daftar | Dashboard',
                                                  'first_name': User().first_name,
                                                  'docs': docs, 'applications': applications})
    else:
        return redirect('/')
