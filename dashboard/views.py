import json

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

import daftar
from daftar.functions import get_storage_documents, get_applications, get_authorities, get_workflows, add_forms, \
    add_workflows, get_forms, add_application_templates, get_application_templates, get_application_template, get_form, \
    get_workflow, submit_applications, save_changes, upload_new_document
from daftar.models import User, UploadFileForm
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
        cost_per_paper = User().costOfPaper
        money_saved = cost_per_paper*len(all_applications)
        trees_saved = len(all_applications)/8333
        trees_saved =round(trees_saved, 5)
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
                                                    'rejected_applications': rejected_applications,
                                                    'cost_per_paper': cost_per_paper,
                                                    'money_saved': money_saved,
                                                    'trees_saved': trees_saved})
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
                return HttpResponseRedirect(reverse('form'))
            else:
                return HttpResponseRedirect(reverse('new_form'))
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
        return render(request, 'new_document.html', {'title': 'Daftar | New Document',
                                                     'isUser': User().isUser,
                                                     'first_name': User().first_name
                                                     })
    else:
        return redirect('/')


def add_new_dcoument(request):
    if verify_token(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                io_file = request.FILES['file'].file
                file_value = io_file.getvalue()

                upload_new_document(data['fileName'], data['fileDescription'], file_value, str(data['file']).split('.')[-1])
                return HttpResponseRedirect(reverse('storage'))
            else:
                return HttpResponseRedirect(reverse('new_document'))
    else:
        return redirect('/')


def new_application_template(request):
    if verify_token(request):
        forms = get_forms()
        if forms is False:
            # TODO: Error handling
            print('Error Loading Forms')

        workflows = get_workflows()
        if workflows is False:
            # TODO: Error handling
            print('Error Loading Workflows')

        return render(request, 'new_application_template.html', {'title': 'Daftar | New Application Template',
                                                                 'isUser': User().isUser,
                                                                 'first_name': User().first_name,
                                                                 'forms': forms,
                                                                 'workflows': workflows})
    else:
        return redirect('/')


def add_application_template(request):
    if verify_token(request):
        if request.method == 'POST':
            response = add_application_templates(request.POST)
            if response:
                return HttpResponseRedirect(reverse('application_template'))
            else:
                return HttpResponseRedirect(reverse('new_application_template'))
    else:
        return redirect('/')


def application_template(request):
    if verify_token(request):
        application_templates = get_application_templates()
        if application_templates is False:
            # TODO: Error handling
            print('Error Loading Documents')

        return render(request, 'application_template.html', {'title': 'Daftar | Application Templates',
                                                             'isUser': User().isUser,
                                                             'first_name': User().first_name,
                                                             'application_templates': application_templates})
    else:
        return redirect('/')


def fill_application(request):
    if verify_token(request):

        if request.method == 'GET':
            applications = get_application_templates()
            if applications is False:
                # TODO: Error handling
                print('Error Loading Documents')
            return render(request, 'fill_application.html', {'title': 'Daftar | Fill Applications',
                                                             'isUser': User().isUser,
                                                             'first_name': User().first_name,
                                                             'applications': applications,
                                                             'isApplicationNotSelected': True})
        else:
            application_template_id = request.POST.get('application_template_id')
            application_template = get_application_template(application_template_id)
            form = get_form(application_template.formId)
            workflow = get_workflow(application_template.workflowId)

            return render(request, 'fill_application.html', {'title': 'Daftar | Fill Applications',
                                                             'isUser': User().isUser,
                                                             'first_name': User().first_name,
                                                             'application_template': application_template,
                                                             'form': form,
                                                             'workflow': workflow,
                                                             'fields': form.fields,
                                                             'isApplicationNotSelected': False})
    else:
        return redirect('/')


def submit_application(request):
    if verify_token(request):
        if request.method == 'POST':
            response = submit_applications(request.POST)
            if response:
                return HttpResponseRedirect(reverse('application'))
            else:
                return HttpResponseRedirect(reverse('fill_application'))

    else:
        return redirect('/')


def my_account(request):
    if verify_token(request):

        return render(request, 'account.html', {'title': 'Daftar | My Account',
                                                'user': User()})
    else:
        return redirect('/')


def save_cost_changes(request):
    if verify_token(request):
        if request.method == 'POST':
            response = save_changes(request.POST)
            print(response)
            return redirect('/')
    else:
        return redirect('/')