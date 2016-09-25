class SecurityState:
    def __init__(self):
        self.permissions = ["delegate", "read", "write", "append"]
        self.delegations = {"anyone": []}
        self.default = "anyone"
        self.identifiers = []

    def add_user(self, user):
        self.delegations[user] = []

    def own(self, user, field):
        if field not in self.identifiers:
            self.identifiers.append(field)
            
        for p in self.permissions:
            self.set_delegation(field, "admin", p, user)

    def set_delegation(self, field, authority, permission, user):
        if field == "all":
            for field in self.identifiers:
                if self.has_permission(authority, field, "delegate"):
                    self.set_delegation(field, authority, permission, user)
        else:
            delegation = Delegation(field, authority, permission, user)
            if delegation not in self.delegations[user]:
                self.delegations[user].append(delegation)

    def delete_delegation(self, field, authority, permission, user):
        if field == "all":
            for field in self.identifiers:
                if self.has_permission(authority, field, "delegate"):
                    self.delete_delegation(field, authority, permission, user)
        else:
            delegation = Delegation(field, authority, permission, user)
            if delegation in self.delegations[user]:
                self.delegations[user].remove(delegation)

    def has_permission(self, user, field, permission):
        if user == "admin":
            return True
        
        tbs = []
        for d in self.delegations[user]:
            if d.field == field and d.permission == permission:
                tbs.append(d)
        for d in self.delegations["anyone"]:
            if d.field == field and d.permission == permission:
                tbs.append(d)
                
        foundPermission = False
        while len(tbs) > 0:
            d = tbs.pop(0)
            if d.authority == "admin":
                foundPermission = True
                break

            for d in self.delegations[d.authority]:
                if (d.field == field or d.field == "all")  and d.permission == permission:
                    tbs.append(d)

        return foundPermission

class Delegation:
    def __init__(self, field, authority, permission, user):
        self.field = field
        self.authority = authority
        self.permission = permission
        self.user = user

    def __eq__(self, other):
        return self.field == other.field and self.authority == other.authority and self.permission == other.permission and self.user == other.user
