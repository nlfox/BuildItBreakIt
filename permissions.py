from copy import deepcopy

class SecurityState:
    def __init__(self):
        self.permissions = ["delegate", "read", "write", "append"]
        self.delegations = {"anyone": [], "admin": []}
        self.default = "anyone"
        self.identifiers = []

        self.delegationsPatch = {}
        self.defaultPatch = ""
        self.identifiersPatch = []

    def __str__(self):
        s = ""
        s += "delegations:\n"
        s += str(self.delegations)
        s += "\nidentifiers:\n"
        s += str(self.identifiers)
        s += "\ndelegationsPatch:\n"
        s += str(self.delegationsPatch)
        s += "\nidentifiersPatch:\n"
        s += str(self.identifiersPatch)
        return s

    def begin_transaction(self):
        self.delegationsPatch = deepcopy(self.delegations)
        self.defaultPatch = self.default
        self.identifiersPatch = []

    def complete_transaction(self):
        self.delegations = deepcopy(self.delegationsPatch)
        self.default = self.defaultPatch
        self.default = ""
        self.identifiers = list(set().union(self.identifiers, self.identifiersPatch))
        self.identifiersPatch = []

    def discard_transaction(self):
        self.delegationsPatch = deepcopy(self.delegations)
        self.default = ""
        self.identifiersPatch = []

    def add_user(self, user):
        if user not in self.delegations and user not in self.delegationsPatch:
            self.delegationsPatch[user] = []
            for p in self.permissions:
                self.set_delegation("all", self.default, p, user)

    def own(self, user, field):
        if field not in self.identifiers and field not in self.identifiersPatch:
            self.identifiersPatch.append(field)
            
        for p in self.permissions:
            self.set_delegation(field, "admin", p, user)

    def set_default(self, user):
        self.defaultPatch = user

    def set_delegation(self, field, authority, permission, user):
        if field == "all":
            for field in self.identifiers:
                if self.has_permission(authority, field, "delegate"):
                    self.set_delegation(field, authority, permission, user)

            for field in self.identifiersPatch:
                if self.has_permission(authority, field, "delegate"):
                    self.set_delegation(field, authority, permission, user)
        else:
            delegation = Delegation(field, authority, permission, user)
            if delegation not in self.delegationsPatch[user]:
                self.delegationsPatch[user].append(delegation)

    def delete_delegation(self, field, authority, permission, user):
        if field == "all":
            for field in self.identifiers:
                if self.has_permission(authority, field, "delegate"):
                    self.delete_delegation(field, authority, permission, user)

            for field in self.identifiersPatch:
                if self.has_permission(authority, field, "delegate"):
                    self.delete_delegation(field, authority, permission, user)
        else:
            delegation = Delegation(field, authority, permission, user)
            if delegation in self.delegationsPatch[user]:
                self.delegationsPatch[user].remove(delegation)

    def has_permission(self, user, field, permission):
        if user == "admin":
            return True
        
        tbs = []
        for d in self.delegationsPatch[user]:
            if d.field == field and d.permission == permission:
                tbs.append(d)
        for d in self.delegationsPatch["anyone"]:
            if d.field == field and d.permission == permission:
                tbs.append(d)
                
        foundPermission = False
        while len(tbs) > 0:
            d = tbs.pop(0)
            if d.authority == "admin":
                foundPermission = True
                break

            for d in self.delegationsPatch[d.authority]:
                if (d.field == field or d.field == "all")  and d.permission == permission:
                    tbs.append(d)

        return foundPermission

class Delegation:
    def __init__(self, field, authority, permission, user):
        self.field = field
        self.authority = authority
        self.permission = permission
        self.user = user

    def __str__(self):
        return "(" + self.field + ", " + self.authority + ", " + self.permission + ", " + self.user + ")"

    def __eq__(self, other):
        return self.field == other.field and self.authority == other.authority and self.permission == other.permission and self.user == other.user
