import json

import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt

import daftar
from daftar.functions import get_storage_documents, get_applications, get_authorities, get_workflows, add_forms, \
    add_workflows, get_forms, add_application_templates, get_application_templates, get_application_template, get_form, \
    get_workflow, submit_applications, save_changes, upload_new_document, sign_applications
from daftar.models import User, UploadFileForm

from daftar.views import verify_token


def index(request):
    if verify_token(request):
        docs = get_storage_documents(limit=4)
        applications = get_applications(limit=3)
        cost_per_paper = User().costOfPaper
        all_applications = get_applications()
        money_saved = cost_per_paper * len(all_applications)
        money_saved = round(money_saved, 5)
        trees_saved = len(all_applications) / 8333
        trees_saved = round(trees_saved, 5)
        pending_applications = len(get_applications(filter='pending'))
        signed_applications = len(get_applications(filter='signed'))
        rejected_applications = len(get_applications(filter='rejected'))

        if docs is False:
            # TODO: Error handling
            print('Error Loading Documents')
            return

        if applications is False:
            # TODO: Error handling
            print('Error Loading Applications')
            return

        return render(request, 'dashboard.html', {'title': 'Daftar | Dashboard',
                                                  'user_type': User().type,
                                                  'first_name': User().first_name,
                                                  'docs': docs,
                                                  'applications': applications,
                                                  'money_saved': money_saved,
                                                  'trees_saved': trees_saved,
                                                  'pending_applications': pending_applications,
                                                  'signed_applications': signed_applications,
                                                  'rejected_applications': rejected_applications})
    else:
        return redirect('/')


def application(request):
    if verify_token(request):
        applications = get_applications()
        pending_applications = []
        rejected_applications = []
        approved_applications = []
        all_applications = []
        for application in applications:
            if application.creatorId == User().id:
                if application.status == 0:
                    pending_applications.append(application)
                elif application.status == 1:
                    approved_applications.append(application)
                else:
                    rejected_applications.append(application)
                all_applications.append(application)
        cost_per_paper = User().costOfPaper
        money_saved = cost_per_paper * len(all_applications)
        trees_saved = len(all_applications) / 8333
        trees_saved = round(trees_saved, 5)

        if all_applications is False:
            # TODO: Error handling
            print('Error Loading Documents')
            return

        return render(request, 'application.html', {'title': 'Daftar | Applications',
                                                    'user_type': User().type,
                                                    'first_name': User().first_name,
                                                    'user_id': User().id,
                                                    'all_applications': all_applications,
                                                    'pending_applications': pending_applications,
                                                    'approved_applications': approved_applications,
                                                    'rejected_applications': rejected_applications,
                                                    'cost_per_paper': cost_per_paper,
                                                    'money_saved': money_saved,
                                                    'trees_saved': trees_saved})
    else:
        return redirect('/')


def review_application(request):
    if verify_token(request):
        all_applications = get_applications(filter=User().id)
        pending_applications = []
        reviewed_applications = []
        for application in all_applications:
            if application.status == 0:
                pending_applications.append(application)
            else:
                reviewed_applications.append(application)

        cost_per_paper = User().costOfPaper
        money_saved = cost_per_paper * len(all_applications)
        trees_saved = len(all_applications) / 8333
        trees_saved = round(trees_saved, 5)

        if all_applications is False:
            # TODO: Error handling
            print('Error Loading Documents')
            return

        return render(request, 'review_application.html', {'title': 'Daftar | Review Applications',
                                                           'user_type': User().type,
                                                           'first_name': User().first_name,
                                                           'user_id': User().id,
                                                           'all_applications': all_applications,
                                                           'pending_applications': pending_applications,
                                                           'reviewed_applications': reviewed_applications,
                                                           'cost_per_paper': cost_per_paper,
                                                           'money_saved': money_saved,
                                                           'trees_saved': trees_saved})
    else:
        return redirect('/')


@xframe_options_exempt
def storage(request):
    if verify_token(request):
        docs = get_storage_documents()

        if docs is False:
            # TODO: Error handling
            print('Error Loading Documents')
            return

        return render(request, 'storage.html', {'title': 'Daftar | Storage',
                                                'user_type': User().type,
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
                                                     'user_type': User().type,
                                                     'first_name': User().first_name,
                                                     'authorities': auth_list})
    else:
        return redirect('/')


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
                                                 'user_type': User().type,
                                                 'first_name': User().first_name,
                                                 'workflows': workflows})
    else:
        return redirect('/')


def new_form(request):
    if verify_token(request):
        return render(request, 'new_form.html', {'title': 'Daftar | New Form',
                                                 'user_type': User().type,
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
                                             'user_type': User().type,
                                             'first_name': User().first_name,
                                             'forms': forms})
    else:
        return redirect('/')


def new_document(request):
    if verify_token(request):
        return render(request, 'new_document.html', {'title': 'Daftar | New Document',
                                                     'user_type': User().type,
                                                     'first_name': User().first_name
                                                     })
    else:
        return redirect('/')


def add_new_document(request):
    if verify_token(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                io_file = request.FILES['file'].file
                file_value = io_file.getvalue()

                upload_new_document(data['fileName'], data['fileDescription'], file_value,
                                    str(data['file']).split('.')[-1])
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
                                                                 'user_type': User().type,
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
                return HttpResponseRedirect(reverse('application_templates'))
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
                                                             'user_type': User().type,
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
                                                             'user_type': User().type,
                                                             'first_name': User().first_name,
                                                             'applications': applications,
                                                             'isApplicationNotSelected': True})
        else:
            application_template_id = request.POST.get('application_template_id')
            application_template = get_application_template(application_template_id)
            form = get_form(application_template.formId)
            workflow = get_workflow(application_template.workflowId)

            return render(request, 'fill_application.html', {'title': 'Daftar | Fill Applications',
                                                             'user_type': User().type,
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


def sign_application(request):
    if verify_token(request):
        if request.method == 'POST':
            response = sign_applications(request.POST)
            print(response)
            if response:
                return HttpResponseRedirect(reverse('application'))
            else:
                return HttpResponseRedirect(reverse('application'))
    else:
        return redirect('/')


def new_application_step1(request):
    if verify_token(request):
        if request.method == "GET":
            forms = get_forms()
            if forms is False:
                # TODO: Error handling
                print('Error Loading Forms')

            return render(request, 'new_application_step1.html', {'title': 'Daftar | New Application Step 1',
                                                                    'isUser': User().isUser,
                                                                    'first_name': User().first_name,
                                                                    'forms': forms})
        elif request.method == "POST":
            application_name = request.POST.get('name')
            if request.POST.get('form_id') is None:
                form_id = add_forms(request.POST)
                print (form_id)
                form_name = get_form(form_id).title
            else:
                form_id = request.POST.get('form_id')
                form_name = get_form(form_id).title
            
            workflows = get_workflows()
            if workflows is False:
                # TODO: Error handling
                print('Error Loading Workflows')
            
            auth_list = get_authorities()
            if auth_list is False:
            # TODO: Error handling
                print('Error Loading Documents')
                return

            return render(request, 'new_application_step2.html', {'title': 'Daftar | New Application Step 2',
                                                                 'isUser': User().isUser,
                                                                 'first_name': User().first_name,
                                                                 'workflows': workflows,
                                                                 'application_name': application_name,
                                                                 'form_id': form_id,
                                                                 'form_name': form_name,
                                                                 'authorities': auth_list
                                                                 })
    else:
        return redirect('/')


def add_application(request):
    if verify_token(request):
        if request.method == 'POST':
            if request.POST.get('workflow_id') is None:
                workflow = add_workflows(request.POST)
                workflow_id = workflow['id']
            else:
                workflow_id = request.POST.get('workflow_id')

            data = {
                'name': request.POST.get('name'),
                'formId': request.POST.get('form_id'),
                'workflowId': workflow_id
            }
            url = daftar.settings.DAFTAR_HOST + "/applications/templates"

            hed = {'Authorization': 'Bearer ' + User().token}
            response = requests.post(url, json=data, headers=hed)
            print(response.text)
            if response.status_code == requests.codes.ok:
                return HttpResponseRedirect(reverse('application_templates'))
            else:
                return HttpResponseRedirect(reverse('new_application_step1'))
    else:
        return redirect('/')
    


