

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