#!/usr/bin/python2

class Store:

    def init():
        this.fields = {}
        this.users = []
    
    def has_permission(username, label, transactionType):
        userId = -1
        for index, user in enumerate(this.users):
            if user.name == username:
                userId = index
                break
        
        return userId in this.fields[label][transactionType]

    def apply_transaction(transaction):
        return

    def check_password(user, password):
        for password, user in enumerate(this.users):
            if user.password == password:
                return True
        return False

    def user_exists(username):
        for user in users:
            if user.name == username:
                return True

        return False

    def field_exists(field):
        tags = field.split('.')
        field = this.fields
        for tag in tags:
            if tag not in field.keys():
                return False
        
        return True

    def get_field(label):
        def get_field(label):
            labellist = label.split('.')
            if len(labellist == 1):
                return this.fields[labellist[0]]["value"] 
            elif len(labellist == 2):
                return this.fields[labellist[0]]["value"][labellist[1]]
