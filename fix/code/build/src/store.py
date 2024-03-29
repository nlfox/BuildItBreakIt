#!/usr/bin/python2
from cpp.pypermissions import PySecurityState

class Store:
    def __init__(self, admin_password):
        self.fields = {}
        self.users = {"admin": admin_password, "anyone": None}

        self.fieldsPatch = {}
        self.usersPatch = {}
        self.local = {}

        self.S = PySecurityState()
        self.principal = ""

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

    def begin_transaction(self, principal):
        self.fieldsPatch = {}
        self.usersPatch = {}
        self.local = {}
        self.principal = principal
        self.S.begin_transaction()

    def discard_transaction(self):
        self.fieldsPatch = {}
        self.usersPatch = {}
        self.local = {}
        self.S.discard_transaction()

    def complete_transaction(self):
        self.users.update(self.usersPatch)
        self.fields.update(self.fieldsPatch)
        self.S.complete_transaction()

    def modify_principal(self, username, password):
        if username not in self.users and username not in self.usersPatch:
            self.S.add_user(username)
            
        self.usersPatch[username] = password

    def has_permission(self, username, label, transactionType):
        if not self.field_exists(label):
            return True

        labellist = label.split('.')
        var = labellist[0]
        if var in self.local:
            return True

        return self.S.has_permission(username, label, transactionType)
    
    def check_password(self, username, password):
        return username in self.users and password == self.users[username]

    def get_field(self, label, reference=False):
        if not self.field_exists(label):
            return ""

        val = None

        labellist = label.split('.')
        if len(labellist) == 1:
            if labellist[0] in self.local:
                val = self.local[labellist[0]]
            elif labellist[0] in self.fieldsPatch:
                val = self.fieldsPatch[labellist[0]]
            else:
                val = self.fields[labellist[0]]
            
        elif len(labellist) == 2:
            if labellist[0] in self.local:
                val = self.local[labellist[0]][labellist[1]]
            elif labellist[0] in self.fieldsPatch:
                val = self.fieldsPatch[labellist[0]][labellist[1]]
            else:
                val = self.fields[labellist[0]][labellist[1]]

        if type(val) == dict:
            if reference:
                return val
            else:
                return dict(val)
        elif type(val) == list:
            if reference:
                return val
            else:
                return list(val)
        else:
            return val

    def user_exists(self, username):
        if username in self.usersPatch:
            return True
        
        if username in self.users:
            return True

        return False

    def field_exists(self, label, local=True):
        tags = label.split('.')

        if len(tags) == 1:
            return (local and tags[0] in self.local) or tags[0] in self.fields or tags[0] in self.fieldsPatch
        else:
            if local and tags[0] in self.local:
                return type(self.local[tags[0]]) == dict and tags[1] in self.local[tags[0]]
            elif tags[0] in self.fieldsPatch:
                return type(self.fieldsPatch[tags[0]]) == dict and tags[1] in self.fieldsPatch[tags[0]]
            elif tags[0] in self.fields:
                return type(self.fields[tags[0]]) == dict and tags[1] in self.fields[tags[0]]
            else:
                return False

    def field_type(self, field):
        if not self.field_exists(field):
            return None
        
        tags = field.split(".")
        if tags[0] in self.local:
            if len(tags) == 1:
                return type(self.local[tags[0]])
            else:
                return type(self.local[tags[0]][tags[1]])
        elif tags[0] in self.fieldsPatch:
            if len(tags) == 1:
                return type(self.fieldsPatch[tags[0]])
            else:
                return type(self.fieldsPatch[tags[0]][tags[1]])
        elif tags[0] in self.fields:
            if len(tags) == 1:
                return type(self.fields[tags[0]])
            else:
                return type(self.fieldsPatch[tags[0]][tags[1]])

    def set_field(self, field, value):
        if not self.field_exists(field):
            self.S.own(self.principal, field)
            self.fieldsPatch[field] = value
        elif not self.field_exists(field, local=False):
            self.set_local(field, value)
        else:
            self.fieldsPatch[field] = value
            

    def set_local(self, field, value):
        self.local[field] = value

    def remove_local(self, field):
        if field in self.local:
            del self.local[field]

    def global_field_exists(self, field):
        return self.field_exists(field.split('.')[0], local=False)

    def set_delegation(self, field, authority, permission, user):
        self.S.set_delegation(field, authority, permission, user)

    def delete_delegation(self, field, authority, permission, user):
        self.S.delete_delegation(field, authority, permission, user)

    def set_default(self, user):
        self.S.set_default(user)

    def append_to(self, field, expr):
        l = self.get_field(field, reference=True)
        if type(expr) == list:
            l.extend(expr)
        else:
            l.append(expr)
#        self.set_field(field, l)
