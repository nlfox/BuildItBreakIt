#!/usr/bin/python2

class Store:
    def __init__(self):
        self.fields = {}
        self.users = {}

        self.fieldsPatch = {}
        self.usersPatch = {}

    def begin_transaction(self):
        self.fieldsPatch = {}
        self.usersPatch = {}

    def modify_principal(self, username, password):
        self.usersPatch[username] = password

    def has_permission(self, username, label, transactionType):
        label = label.split()[0]

        if label in self.fields.keys():
            return username in self.fields[label][transactionType]
        elif label in self.fieldsPatch.keys():
            return username in self.fieldsPatch[label][transactionType]

    def check_password(self, username, password):
        for user in self.users:
            if user.name == username and user.password == password:
                return True

        for user in self.usersPatch:
            if user.name == username and user.password == password:
                return True
            
        return False

    def get_field(self, label):
        labellist = label.split('.')
        if len(labellist) == 1:
            return self.fields[labellist[0]]["value"]
        elif len(labellist) == 2:
            return self.fields[labellist[0]]["value"][labellist[1]]

    def user_exists(self, username):
        for user in self.usersPatch:
            if user.name == username:
                return True
        
        for user in self.users:
            if user.name == username:
                return True

        return False

    def field_exists(self, label):
        tags = label.split('.')

        if len(tags) == 1:
            return tags[0] in this.fields.keys() or tags[0] in this.fieldsPatch.keys()
        else:
            return tags[1] in this.fields[tags[0]]["value"].keys() or tags[1] in this.fieldsPatch[tags[0]]["value"].keys()
