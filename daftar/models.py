import tempfile

import requests

from django.db import models
from django.core import files


class User(object):
    class __User:
        def __init__(self):
            self.id = None
            self.first_name = None
            self.last_name = None
            self.dob = None
            self.isUser = None
            self.token = None

        def __str__(self):
            return self + self.id
    instance = None

    def __new__(cls): # __new__ always a classmethod
        if not User.instance:
            User.instance = User.__User()
        return User.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


class StorageDocument(models.Model):
    # ImageField not sure :/
    img = models.ImageField(upload_to='images/', blank=True, null=True)

    def __init__(self, json, url):
        self.id = json['_id']['$oid']
        self.fileName = json['fileName']
        self.fileDesc = json['fileDescription']
        self.file = json['file']
        self.fileExt = json['fileExtension']
        self.visibility = json['visibility']
        self.timestamp = json['timestamp']

        if self.fileExt == 'jpg' or self.fileExt == 'png' or self.fileExt == 'jpeg':
            print('JPG/PNG/JPEG image detected')
            # TODO: Fix this
            #self.load_img(url)

    # This is not working :/
    def load_img(self, url):
        hed = {'Authorization': 'Bearer ' + User().token}
        request = requests.get(url, stream=True, headers=hed)

        if request.status_code != requests.codes.ok:
            return

        lf = tempfile.NamedTemporaryFile()

        for block in request.iter_content(1024 * 8):
            if not block:
                break

            lf.write(block)

        self.img.save(self.file, files.File(lf))
