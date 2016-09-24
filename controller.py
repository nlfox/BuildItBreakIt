#!/usr/bin/python2
from store import Store

class Controller:
    
    def __init__(self):
        self.principal = ""
        self.store = Store()

    def apply_permissions(self, access_criterion, success_criterion, action):
        if access_criterion:
            if success_criterion:
                action(self)
            else:
                raise RuntimeError("FAILED")
        else:
            raise RuntimeError("DENIED")

    def begin_transaction(self, principal):
        self.principal = principal
        self.store.begin_transaction()

    def create_principal(self, username, password):
        self.apply_permissions(
            self.principal == "admin",
            not self.store.user_exists(username),
            lambda self: self.store.modify_principal(username, password)
            )

    def change_password(self, username, password):
        self.apply_permissions(
            self.principal == "admin" or self.principal == username,
            self.store.user_exists(username),
            lambda self: self.store.modify_principal(username, password)
            )

    def set(self, field, expression):
        pass

    def append_to(self, field, expression):
        pass

    def local(self, field, expression):
        pass

    def for_each(self, iterator, field, expression):
        pass

    def set_delegation(self, field, authority, permission, user):
        pass

    def delete_delegation(self, field, authority, permission, user):
        pass

    def default_delegator(self, user):
        pass
