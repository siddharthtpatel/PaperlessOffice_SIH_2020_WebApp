import json

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

import daftar
from daftar.functions import get_storage_documents, get_applications, get_authorities, get_workflows, add_forms, \
    add_workflows, get_forms
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
    if verify_token(request):
        if request.method == 'POST':
            response = add_workflows(request.POST)

            if response:
                return HttpResponseRedirect(reverse('new_workflow'))
            else:
                return HttpResponseRedirect(reverse('index'))
    else:
        return redirect('/')


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


def new_form(request):
    if verify_token(request):
        return render(request, 'new_form.html', {'title': 'Daftar | New Form',
                                                 'isUser': User().isUser,
                                                 'first_name': User().first_name})
    else:
        return redirect('/')


def add_form(request):
    if verify_token(request):
        if request.method == 'POST':
            response = add_forms(request.POST)
            if response:
                return HttpResponseRedirect(reverse('workflow'))
            else:
                return HttpResponseRedirect(reverse('add_form'))
    else:
        return redirect('/')


def form(request):
    if verify_token(request):
        forms = get_forms()
        if forms is False:
            # TODO: Error handling
            print('Error Loading Documents')

        return render(request, 'form.html', {'title': 'Daftar | Forms',
                                             'isUser': User().isUser,
                                             'first_name': User().first_name,
                                             'forms': forms})
    else:
        return redirect('/')


def new_document(request):
    if verify_token(request):
        # TODO

        return render(request, 'new_document.html', {'title': 'Daftar | New Document'})
    else:
        return redirect('/')
