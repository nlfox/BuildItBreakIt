#!/usr/bin/python2

class Store:
    def __init__(self):
        self.fields = {}
        self.users = []

    def has_permission(self, username, label, transactionType):
        label = label.split()[0]
        userId = -1
        for index, user in enumerate(self.users):
            if user.name == username:
                userId = index
                break

        return userId in self.fields[label][transactionType]

    def apply_transaction(self, transaction):
        return

    def check_password(self, username, password):
        for user in self.users:
            if user.name == username and user.password == password:
                return True
        return False

    def user_exists(self, username):
        for user in self.users:
            if user.name == username:
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
