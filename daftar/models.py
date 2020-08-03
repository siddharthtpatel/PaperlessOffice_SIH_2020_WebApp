import os
import tempfile
import datetime
import json as js
import requests
from django.core.files.base import ContentFile

from django.db import models
from django.core import files
from django.core.files.storage import FileSystemStorage, default_storage
from django import forms

import daftar
from daftar import settings


class User(object):
    class __User:
        def __init__(self):
            self.id = None
            self.first_name = None
            self.last_name = None
            self.dob = None
            self.public_key = None
            self.private_key = None
            self.role = None
            self.type = None
            self.token = None
            self.email = None
            self.costOfPaper = None

        def __str__(self):
            return self + self.id

    instance = None

    def __new__(cls):  # __new__ always a classmethod
        if not User.instance:
            User.instance = User.__User()
        return User.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class StorageDocument(models.Model):
    image = models.ImageField(
        upload_to='media',
    )

    def __init__(self, json):
        self.id = json['_id']['$oid']
        self.fileName = json['fileName']
        self.fileDesc = json['fileDescription']
        self.file = json['file']
        self.fileExt = json['fileExtension']
        self.visibility = json['visibility']
        self.timestamp = datetime.datetime.fromtimestamp(float(json['timestamp']['$date']) / 1000)

        if self.fileExt == 'jpg' or self.fileExt == 'png' or self.fileExt == 'jpeg':
            print('JPG/PNG/JPEG image detected')
        self.load_img()

        url = daftar.settings.DAFTAR_HOST + "/users"
        hed = {'Authorization': 'Bearer ' + User().token}
        request = requests.get(url, stream=True, headers=hed)
        users = js.loads(request.text)
        for user in users:
            if json['creator'] == user['_id']['$oid']:
                self.creatorName = user['first_name'] + " " + user['last_name']

    def load_img(self):
        url = daftar.settings.DAFTAR_HOST + "/storage/" + self.id + "?download"
        hed = {'Authorization': 'Bearer ' + User().token}
        request = requests.get(url, stream=True, headers=hed)

        if request.status_code != requests.codes.ok:
            return

        print(self.fileName)
        print(daftar.settings.MEDIA_ROOT)

        file_name = default_storage.save(self.file, ContentFile(request.content))
        self.file_url = default_storage.url(file_name)
        print(self.file_url)


class Application(object):

    def __init__(self, json):
        self.id = json['_id']['$oid']
        self.name = json['name']
        self.description = json['description']
        self.creatorId = json['creatorId']
        self.creatorName = json['creatorName']
        self.status = int(json['status'])
        self.stage = int(json['stage'])
        self.stages = int(json['stages'])
        self.assignedName = json['assignedName']
        self.assignedId = json['assignedId']
        self.timestamp = datetime.datetime.fromtimestamp(float(json['timestamp']['$date']) / 1000)
        self.progress = int(self.stage / self.stages * 100)

        if User().token == json['creatorId']:
            self.isCreator = True
        else:
            self.isCreator = False


class Authority(object):

    def __init__(self, json):
        self.id = json['_id']['$oid']
        self.name = json['first_name'] + ' ' + json['last_name']
        self.role = json['role']


class Workflow(object):

    def __init__(self, json):
        self.id = json['_id']['$oid']
        self.name = json['name']
        self.creatorId = json['creatorId']
        self.totalStages = int(json['totalStages'])
        self.stages = json['stages']
        self.timestamp = datetime.datetime.fromtimestamp(float(json['timestamp']['$date']) / 1000)

        if User().id == json['creatorId']:
            self.isCreator = True
        else:
            self.isCreator = False


class Form(object):

    def __init__(self, json):
        self.id = json['_id']['$oid']
        self.title = json['title']
        self.description = json['description']
        self.creatorId = json['creator']
        self.fields = []
        i = 1
        for field in json['fields']:
            self.fields.append(Field(field, i))
            i = i + 1

        if User().id == json['creator']:
            self.isCreator = True
        else:
            self.isCreator = False


class ApplicationTemplates(object):

    def __init__(self, json):
        self.id = json['_id']['$oid']
        self.name = json['name']
        self.creatorName = json['creatorName']
        self.stages = json['stages']
        self.workflowId = json['workflowId']
        self.formId = json['formId']

        if User().id == json['creatorId']:
            self.isCreator = True
        else:
            self.isCreator = False

        url = daftar.settings.DAFTAR_HOST
        hed = {'Authorization': 'Bearer ' + User().token}

        request = requests.get(url + "/workflow", stream=True, headers=hed)
        workflows = js.loads(request.text)
        for workflow in workflows:
            if json['workflowId'] == workflow['_id']['$oid']:
                self.workflowName = workflow['name']

        request = requests.get(url + "/form", stream=True, headers=hed)
        forms = js.loads(request.text)
        for form in forms:
            if json['formId'] == form['_id']['$oid']:
                self.formName = form['title']


class Field(object):

    def __init__(self, json, field_id):
        self.id = field_id
        self.type = json['type']
        self.question = json['question']

        if json['type'] in ('radio', 'checkbox'):
            self.options = []
            i = 1
            for option in json['options'].values():
                self.options.append(Option(option, i))
                i = i + 1


class Option(object):

    def __init__(self, value, option_id):
        self.id = option_id
        self.value = value


class UploadFileForm(forms.Form):
    fileName = forms.CharField(max_length=50)
    fileDescription = forms.CharField(max_length=50)
    file = forms.FileField()
