#!/usr/bin/python2

from store import Store

class Controller:

    def __init__(self, store, server):
        self.principal = ""
        self.store = store
        self.server = server

    def apply_permissions(self, access_criterion, success_criterion, action):
        if access_criterion:
            if success_criterion:
                action(self)
            else:
                raise RuntimeError("FAILED")
        else:
            raise RuntimeError("DENIED")

    def begin_transaction(self, principal, password):
        if not self.store.user_exists(principal):
            raise RuntimeError("FAILED")

        if not self.store.check_password(principal, password):
            raise RuntimeError("DENIED")

        self.principal = principal
        self.store.begin_transaction()

    def end_transaction(self):
        # apply changes
        pass

    def end_transaction_exit(self):
        # apply changes, check for permission and end program
        self.server.run = False # Stops server
        pass

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

    def get_value(self, token):
        # evaluate token value and return that
        if type(token) is dict:
            return token
        else:
            #todo: parse ID_GROUP STRING
            pass
        pass

    def set(self, field, expression):
        value = self._parse_expression(expression)
        self.apply_permissions(
            self.store.has_permission(self.principal, field, "write"),
            True,
            lambda self: self.store.set_field(field, value)
            )


    def append_to(self, field, expression):
        value = self._parse_expression(expression)
        self.apply_permissions(
            self.store.has_permission(self.principal, field, "append"),
            self.store.field_exists(field) and
            self.store.field_type(field) == list,
            lambda self: self.store.append_to(field, value)
            )

    def local(self, field, expression):
        value = self._parse_expression(expression)
        self.apply_permissions(
            True,
            not self.store.field_exists(field),
            lambda self: self.store.set_local(field, value)
            )

    def for_each(self, iterator, field, expression):
        def action(self):
            l = self.store.get_field(field)
            newValue = []
            for element in l:
                self.store.set_local(iterator, element)
                value = self._parse_expression(expression)
                newValue.append(value)
            self.store.remove_local(iterator)
            self.set(field, newValue)

        self.apply_permissions(
            self.store.has_permission(self.principal, field, "read") and
            self.store.has_permission(self.principal, field, "write"),

            self.store.field_exists(field) and
            self.store.field_type(field) == list and
            not self.store.field_exists(iterator),

            action
            )


    # TODO: figure out conditions for anyone and all
    def set_delegation(self, field, authority, permission, user):
        self.apply_permissions(
            (self.principal == "admin" or self.principal == authority) and
            self.store.has_permission(authority, field, "delegate") and
            self.store.has_permission(authority, field, permission),

            self.store.field_exists(field) and
            self.store.user_exists(user) and
            self.store.user_exists(authority),

            lambda self: self.store.set_delegation(field, authority, permission, user)
            )

    def delete_delegation(self, field, authority, permission, user):
        self.apply_permission(


    def default_delegator(self, user):
        pass

    def _parse_expression(self, expression):
        pass

# has_permission should return true if the field doesn't exist
