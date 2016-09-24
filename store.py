#!/usr/bin/python2

class Store:
    def __init__(self):
        self.fields = {}
        self.users = {}

        self.fieldsPatch = {}
        self.usersPatch = {}

        self.principal = ""

    def begin_transaction(self):
        self.fieldsPatch = {}
        self.usersPatch = []

    def set_principal(self, username):
        self.principal = username

    def create_principal(self, username, password):
        if this.principal == "admin":
            if !self._user_exists(username):
                self.usersPatch[username] = password
            else:
                raise RuntimeError("FAILED")
        else:
            raise RuntimeError("DENIED")

    def change_password(self, username, password):
        if self.principal == "admin" or self.principal == username:
            if self._user_exists(username):
                self.usersPatch[username] = password
            else:
                raise RuntimeError("FAILED")
        else:
            raise RuntimeError("DENIED")

    def has_permission(self, username, label, transactionType):
        label = label.split()[0]

        return username in self.fields[label][transactionType]

    def check_password(self, username, password):
        for user in self.users:
            if user.name == username and user.password == password:
                return True

        for user in self.usersPatch:
            if user.name == username and user.password == password:
                return True
            
        return False

    def field_exists(self, field):
        tags = field.split('.')
        if len(tags) == 1:
            return tags[0] in self.fields.keys()
        else:
            return tags[0] in self.fields.keys() and tags[1] in self.fields[tags[0]]["value"]

    def get_field(self, label):
        labellist = label.split('.')
        if len(labellist) == 1:
            return self.fields[labellist[0]]["value"]
        elif len(labellist) == 2:
            return self.fields[labellist[0]]["value"][labellist[1]]

    def _user_exists(self, username):
        for user in this.usersPatch:
            if user.name == username:
                return True
        
        for user in this.users:
            if user.name == username:
                return True

        return False

    def _field_exists(self, label):
        tags = label.split('.')

        if len(tags) == 1:
            return tags[0] in this.fields.keys() or tags[0] in this.fieldsPatch.keys()
        else:
            return tags[1] in this.fields[tags[0]]["value"].keys() or tags[1] in this.fieldsPatch[tags[0]]["value"].keys()
