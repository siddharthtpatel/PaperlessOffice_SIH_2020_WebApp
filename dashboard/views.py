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
            return

        return render(request, 'dashboard.html', {'title': 'Daftar | Dashboard',
                                                  'isUser': User().isUser,
                                                  'first_name': User().first_name,
                                                  'docs': docs, 'applications': applications})
    else:
        return redirect('/')


def application(request):
    if verify_token(request):
        applications = get_applications()
        if applications is False:
            # TODO: Error handling
            print('Error Loading Documents')
            return

        return render(request, 'application.html', {'title': 'Daftar | Applications',
                                                    'isUser': User().isUser,
                                                    'first_name': User().first_name,
                                                    'applications': applications})
    else:
        return redirect('/')


def storage(request):
    if verify_token(request):
        docs = get_storage_documents()

        if docs is False:
            # TODO: Error handling
            print('Error Loading Documents')
            return

        return render(request, 'storage.html', {'title': 'Daftar | Storage',
                                                'isUser': User().isUser,
                                                'first_name': User().first_name,
                                                'docs': docs})
    else:
        return redirect('/')
