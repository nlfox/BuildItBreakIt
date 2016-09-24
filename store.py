#!/usr/bin/python2

class Store:
    def __init__(self):
        self.fields = {}
        self.users = []

    def has_permission(self, username, label, transactionType):
        userId = -1
        for index, user in enumerate(self.users):
            if user.name == username:
                userId = index
                break

        return userId in self.fields[label][transactionType]

    def apply_transaction(self, transaction):
        return

    def check_password(self, user, password):
        for password, user in enumerate(self.users):
            if user.password == password:
                return True
        return False

    def user_exists(self, username):
        for user in self.users:
            if user.name == username:
                return True

        return False

    def field_exists(self, field):
        tags = field.split('.')
        field = self.fields
        for tag in tags:
            if tag not in field.keys():
                return False

        return True

    def get_field(self, label):
        def get_field(label):
            labellist = label.split('.')
            if len(labellist == 1):
                return self.fields[labellist[0]]["value"]
            elif len(labellist == 2):
                return self.fields[labellist[0]]["value"][labellist[1]]
