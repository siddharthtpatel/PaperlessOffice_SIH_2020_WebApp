from django.shortcuts import render

from daftar.functions import get_storage_documents
from daftar.models import User
from daftar.views import verify_token


def index(request):
    if verify_token(request):
        docs = get_storage_documents(limit=4)

        if docs is False:
            # TODO: Error handling
            print('Error Loading Documents')
            return

        print(docs)
        return render(request, 'dashboard.html', {'title': 'Daftar | Dashboard',
                                                  'first_name': User().first_name,
                                                  'docs': docs})
    else:
        return render(request, 'index.html', {})
