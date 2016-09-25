#!/usr/bin/python2

class Store:
    def __init__(self):
        self.fields = {}
        self.users = {}

        self.fieldsPatch = {}
        self.usersPatch = {}
        self.local = {}

    def __str__(self):
        s = ""
        s += "Local:\n"
        s += str(self.local)
        s += "\nusersPatch:\n"
        s += str(self.usersPatch)
        s += "\nfieldsPatch:\n"
        s += str(self.fieldsPatch)
        s += "\nusers:\n"
        s += str(self.users)
        s += "\nfields:\n"
        s += str(self.fields)
        s += "\n"
        return s

    def begin_transaction(self):
        self.fieldsPatch = {}
        self.usersPatch = {}
        self.local = {}

    def discard_transaction(self):
        self.begin_transaction()

    def complete_transaction(self):
        self.users.update(self.usersPatch)
        self.fields.update(self.fieldsPatch)

    def modify_principal(self, username, password):
        self.usersPatch[username] = password

    # TODO: all of this needs to be reworked
    def has_permission(self, username, label, transactionType):
        if not self.field_exists(label):
            return True
        pass
    
    def check_password(self, username, password):
        for user in self.users:
            if user.name == username and user.password == password:
                return True
            
        return False

    def get_field(self, label):
        if not self.field_exists(label):
            return ""
        
        labellist = label.split('.')
        if len(labellist) == 1:
            if labellist[0] in self.local.keys():
                return self.local[labellist[0]]
            elif labellist[0] in self.fieldsPatch.keys():
                return self.fieldsPatch[labellist[0]]
            else:
                return self.fields[labellist[0]]
            
        elif len(labellist) == 2:
            if labellist[0] in self.local.keys():
                return self.local[labellist[0]][labellist[1]]
            elif labellist[0] in self.fieldsPatch.keys():
                return self.fieldsPatch[labellist[0]][labellist[1]]
            else:
                return self.fields[labellist[0]][labellist[1]]

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
            return tags[0] in self.local.keys() or tags[0] in self.fields.keys() or tags[0] in self.fieldsPatch.keys()
        else:
            if tags[0] in self.local.keys():
                return type(self.local[tags[0]]) == dict and tags[1] in self.local[tags[0]]
            elif tags[0] in self.fieldsPatch.keys():
                return type(self.fieldsPatch[tags[0]]) == dict and tags[1] in self.fieldsPatch[tags[0]]
            elif tags[0] in self.fields.keys():
                return type(self.fields[tags[0]]) == dict and tags[1] in self.fields[tags[0]]
            else:
                return False

    def field_type(self, field):
        if not self.field_exists(field):
            return None
        
        tags = field.split(".")
        if tags[0] in self.local.keys():
            if len(tags) == 1:
                return type(self.local[tags[0]])
            else:
                return type(self.local[tags[0]][tags[1]])
        elif tags[0] in self.fieldsPatch.keys():
            if len(tags) == 1:
                return type(self.fieldsPatch[tags[0]])
            else:
                return type(self.fieldsPatch[tags[0]][tags[1]])
        elif tags[0] in self.fields.keys():
            if len(tags) == 1:
                return type(self.fields[tags[0]])
            else:
                return type(self.fieldsPatch[tags[0]][tags[1]])

    def set_field(self, field, value):
        self.fieldsPatch[field] = value

    def set_local(self, field, value):
        self.local[field] = value

    def remove_local(self, field):
        if field in self.local:
            del self.local[field]

    def shallow_field_exists(self, field):
        return self.field_exists(field.split('.')[0])

    def set_delegation(self, field, authority, permission, user):
        pass

    def delete_delegation(self, field, authority, permission, user):
        pass

    
