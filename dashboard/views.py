import json

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

import daftar
from daftar.functions import get_storage_documents, get_applications, get_authorities, get_workflows
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
        all_applications = get_applications()
        pending_applications = get_applications(filter='pending')
        approved_applications = get_applications(filter='signed')
        rejected_applications = get_applications(filter='rejected')
        if all_applications is False:
            # TODO: Error handling
            print('Error Loading Documents')
            return

        return render(request, 'application.html', {'title': 'Daftar | Applications',
                                                    'isUser': User().isUser,
                                                    'first_name': User().first_name,
                                                    'all_applications': all_applications,
                                                    'pending_applications': pending_applications,
                                                    'approved_applications': approved_applications,
                                                    'rejected_applications': rejected_applications})
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


def new_workflow(request):
    if verify_token(request):
        auth_list = get_authorities()

    if auth_list is False:
        # TODO: Error handling
        print('Error Loading Documents')
        return

    return render(request, 'new_workflow.html', {'title': 'Daftar | Workflow',
                                                 'isUser': User().isUser,
                                                 'first_name': User().first_name,
                                                 'authorities': auth_list})


def add_workflow(request):
    if request.method == 'POST':
        stages = []
        for i in range(1, int(request.POST.get('totalStages')) + 1):
            id_name = request.POST.get(str(i)).split('_')
            stage = {'authId': id_name[0], 'authName': id_name[1]}
            stages.append(stage)

        data = {
            "name": request.POST.get('name'),
            "creatorId": User().id,
            "totalStages": request.POST.get('totalStages'),
            "stages": stages
        }

        hed = {'Authorization': 'Bearer ' + User().token}
        r = requests.post(daftar.settings.DAFTAR_HOST + "/workflow", json=data, headers=hed)

        if r.status_code == requests.codes.ok:
            return HttpResponseRedirect(reverse('new_workflow'))
        else:
            return HttpResponseRedirect(reverse('index'))


def workflow(request):
    if verify_token(request):
        workflows = get_workflows()
        if workflows is False:
            # TODO: Error handling
            print('Error Loading Documents')


        return render(request, 'workflow.html', {'title': 'Daftar | Workflows',
                                                 'isUser': User().isUser,
                                                 'first_name': User().first_name,
                                                 'workflows': workflows})
    else:
        return redirect('/')


def new_document(request):
    if verify_token(request):
        # TODO

        return render(request, 'new_document.html', {'title': 'Daftar | New Document'})
    else:
        return redirect('/')

