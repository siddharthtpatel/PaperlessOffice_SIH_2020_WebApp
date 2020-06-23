import requests

import daftar
from daftar.models import User, StorageDocument, Application


def get_storage_documents(limit = None):
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
