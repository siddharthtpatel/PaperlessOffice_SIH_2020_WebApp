import requests
from django import forms

import daftar


class User(object):
    class __User:
        def __init__(self):
            self.data = None

        def __str__(self):
            return self + self.data
    instance = None

    def __new__(cls): # __new__ always a classmethod
        if not User.instance:
            User.instance = User.__User()
        return User.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)