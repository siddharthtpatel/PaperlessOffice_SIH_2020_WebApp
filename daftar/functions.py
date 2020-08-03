import json

import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, FileResponse

import daftar
from daftar.models import User, StorageDocument, Application, Authority, Workflow, Form, ApplicationTemplates
from daftar.views import verify_token


def get_storage_documents(limit=None):
    url = daftar.settings.DAFTAR_HOST + "/storage"
    if limit is not None:
        url += '?limit=' + str(limit)

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.get(url, headers=hed)

    if response.status_code != 200:
        return False

    docs = []
    for doc in response.json():
        docs.append(StorageDocument(doc))

    return docs


def get_applications(user_id=None, filter=None, limit=None):
    url = daftar.settings.DAFTAR_HOST + "/applications"

    if filter is not None:
        url += '?filter=' + str(filter) + '&'

    if limit is not None:
        url += '?limit=' + str(limit)

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.get(url, headers=hed)

    if response.status_code != 200:
        return False

    docs = []
    if user_id is not None:
        for doc in response.json():
            application = Application(doc)
            print(application.authorities)
            if User().id in application.authorities:
                docs.append(application)
    else:
        for doc in response.json():
            docs.append(Application(doc))

    return docs


def get_authorities(filter=None, limit=None):
    url = daftar.settings.DAFTAR_HOST + "/users"

    if filter is not None:
        url += '?filter=' + str(filter) + '&'

    if limit is not None:
        url += '?limit=' + str(limit)

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.get(url, headers=hed)

    auth_list = []
    for auth in response.json():
        auth_list.append(Authority(auth))

    return auth_list


def get_workflows(filter=None, limit=None):
    url = daftar.settings.DAFTAR_HOST + "/workflow"

    if filter is not None:
        url += '?filter=' + str(filter) + '&'

    if limit is not None:
        url += '?limit=' + str(limit)

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.get(url, headers=hed)

    if response.status_code != 200:
        return False

    workflows = []
    for workflow in response.json():
        workflows.append(Workflow(workflow))

    return workflows


def add_forms(form):
    fields = []
    for i in range(1, int(form.get('totalFields')) + 1):
        question = {'type': form.get(f'{i}_type'),
                    'question': form.get(f'{i}_question')}
        options = {}
        if question['type'] in ['radio', 'checkbox']:
            for j in range(1, int(form.get(f"{i}_total_options")) + 1):
                options[f'{j}'] = form.get(f"{i}_{j}_option")
            question['options'] = options
        fields.append(question)

    data = {'creator': User().first_name + " " + User().last_name,
            'title': form.get('formName'),
            'description': form.get('formDesc'),
            'fields': fields}

    url = daftar.settings.DAFTAR_HOST + "/form"

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.post(url, json=data, headers=hed)
    if response.status_code == requests.codes.ok:
        form = json.loads(response.text)
        return form['id']
    else:
        return False


def add_workflows(form):
    stages = []
    for i in range(1, int(form.get('totalStages')) + 1):
        id_name = form.get(f'{i}_name').split('_')
        stage = {'authId': id_name[0], 'authRole': form.get(f'{i}_role'), 'authName': id_name[1]}
        stages.append(stage)

    data = {
        "name": form.get('workflowName'),
        "creatorId": User().id,
        "totalStages": form.get('totalStages'),
        "stages": stages
    }

    url = daftar.settings.DAFTAR_HOST + "/workflow"

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.post(url, json=data, headers=hed)
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)
    else:
        return False


def get_forms(filter=None, limit=None):
    url = daftar.settings.DAFTAR_HOST + "/form"

    if filter is not None:
        url += '?filter=' + str(filter) + '&'

    if limit is not None:
        url += '?limit=' + str(limit)

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.get(url, headers=hed)

    if response.status_code != 200:
        return False

    forms = []
    for form in response.json():
        forms.append(Form(form))

    return forms


def add_application_templates(form):
    data = {
        "name": form.get('name'),
        "workflowId": form.get('workflow_id'),
        "formId": form.get('form_id')
    }
    url = daftar.settings.DAFTAR_HOST + "/applications/templates"

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.post(url, json=data, headers=hed)
    if response.status_code == requests.codes.ok:
        return True
    else:
        return False


def get_application_templates(filter=None, limit=None):
    url = daftar.settings.DAFTAR_HOST + "/applications/templates"

    if filter is not None:
        url += '?filter=' + str(filter) + '&'

    if limit is not None:
        url += '?limit=' + str(limit)

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.get(url, headers=hed)

    if response.status_code != 200:
        return False

    application_templates = []
    for application_template in response.json():
        application_templates.append(ApplicationTemplates(application_template))

    return application_templates


def fetch_application(request):
    if verify_token(request):
        if request.method == "POST":
            url = daftar.settings.DAFTAR_HOST + "/applications/" + str(request.POST.get('id'))
            hed = {'Authorization': 'Bearer ' + User().token}
            response = requests.get(url, headers=hed)
            return HttpResponse(response, content_type=json)


def get_application_template(application_template_id):
    url = daftar.settings.DAFTAR_HOST + "/applications/templates/" + application_template_id

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.get(url, headers=hed)

    if response.status_code != 200:
        return False

    application_template = ApplicationTemplates(response.json())

    return application_template


def get_form(form_id):
    url = daftar.settings.DAFTAR_HOST + "/form/" + form_id

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.get(url, headers=hed)

    if response.status_code != 200:
        return False

    form = Form(response.json())

    return form


def get_workflow(workflow_id):
    url = daftar.settings.DAFTAR_HOST + "/workflow/" + workflow_id

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.get(url, headers=hed)

    if response.status_code != 200:
        return False

    workflow = Workflow(response.json())

    return workflow


def submit_applications(form):
    form_details = {}
    i = 1
    for i in range(1, int(form.get('fields_count')) + 1):
        if form.get(f'{i}_type') == "checkbox":
            answers = []
            for j in range(1, int(form.get(f'{i}_answer_count')) + 1):
                if form.get(f'{i}_answer_{j}') is not None:
                    answers.append(form.get(f'{i}_answer_{j}'))
            form_details[form.get(f'{i}_question')] = answers
        else:
            form_details[form.get(f'{i}_question')] = form.get(f'{i}_answer')

    data = {
        "name": form.get('name'),
        "templateId": form.get('id'),
        "form": form_details
    }
    print(data)
    url = daftar.settings.DAFTAR_HOST + "/applications"

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.post(url, json=data, headers=hed)
    if response.status_code == requests.codes.ok:
        # if False:
        return True
    else:
        return False


def save_changes(form):
    url = daftar.settings.DAFTAR_HOST + "/settings/costOfPaper/" + form.get("costOfPaper")

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.post(url, {}, headers=hed)
    if response.status_code == requests.codes.ok:
        return True
    else:
        return False


class FileLimiter(object):
    def __init__(self, file_obj, read_limit):
        self.read_limit = read_limit
        self.amount_seen = 0
        self.file_obj = file_obj

        # So that requests doesn't try to chunk the upload but will instead stream it:
        self.len = read_limit

    def read(self, amount=-1):
        if self.amount_seen >= self.read_limit:
            return b''
        remaining_amount = self.read_limit - self.amount_seen
        data = self.file_obj.read(min(amount, remaining_amount))
        self.amount_seen += len(data)
        return data


def upload_new_document(fileName, fileDesc, file, fileExt):
    url = daftar.settings.DAFTAR_HOST + "/storage"

    hed = {'Authorization': 'Bearer ' + User().token}

    data = {
        "fileName": fileName,
        "fileDescription": fileDesc,
        "fileExt": fileExt
    }
    response = requests.post(url, data, headers=hed,
                             files=dict(file=file))
    if response.status_code == requests.codes.ok:
        return True
    else:
        print(response.json())
        return False


def sign_applications(form):
    url = daftar.settings.DAFTAR_HOST + "/applications/" + form.get('id')
    if form.get('action') == "Sign":
        url += "/sign"
    else:
        url += "/reject"

    data = {
        "message": form.get('message')
    }

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.post(url, json=data, headers=hed)
    print(response.text)
    print(response.status_code)
    if response.status_code == requests.codes.ok:
        # if True:
        return True
    else:
        return False


def fetch_workflow(request):
    if verify_token(request):
        if request.method == "POST":
            url = daftar.settings.DAFTAR_HOST + "/workflow/" + str(request.POST.get('id'))
            hed = {'Authorization': 'Bearer ' + User().token}
            response = requests.get(url, headers=hed)
            return HttpResponse(response, content_type=json)


def export(request):
    if verify_token(request):
        if request.method == "POST":
            url = daftar.settings.DAFTAR_HOST + "/" + request.POST.get('name') + "?excel"
            hed = {'Authorization': 'Bearer ' + User().token}
            response = requests.get(url, headers=hed)

            file_name = default_storage.save('excel', ContentFile(response.content))
            file_url = default_storage.url(file_name)

            f = open("media/" + file_name + ".xls", 'x')
            f.close()
            f = open("media/" + file_name + ".xls", 'wb+')
            f.write(response.content)
            f.close()
            return HttpResponse(file_url + ".xls")
