import json

import requests

import daftar
from daftar.models import User, StorageDocument, Application, Authority, Workflow, Form


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


def get_applications(filter=None, limit=None):
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
    print(data)

    url = daftar.settings.DAFTAR_HOST + "/form"

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.post(url, json=data, headers=hed)
    if response.status_code == requests.codes.ok:
        return True
    else:
        return False


def add_workflows(form):
    stages = []
    for i in range(1, int(form.get('totalStages')) + 1):
        id_name = form.get(str(i)).split('_')
        stage = {'authId': id_name[0], 'authName': id_name[1]}
        stages.append(stage)

    data = {
        "name": form.get('name'),
        "creatorId": User().id,
        "totalStages": form.get('totalStages'),
        "stages": stages
    }

    url = daftar.settings.DAFTAR_HOST + "/workflow"

    hed = {'Authorization': 'Bearer ' + User().token}
    response = requests.post(url, json=data, headers=hed)
    if response.status_code == requests.codes.ok:
        return True
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
