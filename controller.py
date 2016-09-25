#!/usr/bin/python2

from store import Store
import ply.lex as lex
from ply.lex import LexToken

class Controller:

    def __init__(self, store, server):
        self.principal = ""
        self.store = store
        self.server = server

    def _assert_access(self, condition):
        if not condition:
            raise RuntimeError("DENIED")
        self.store.discard_transaction()

    def _assert_success(self, condition):
        if not condition:
            raise RuntimeError("FAILED")
        self.store.discard_transaction()

    def begin_transaction(self, principal, password):
        self._assert_access(self.store.user_exists(principal))
        self._assert_success(self.store.check_password(principal, password))
        self.principal = principal
        self.store.begin_transaction(principal)

    def end_transaction(self):
        self.store.complete_transaction()

    def end_transaction_exit(self):
        # apply changes, check for permission and end program
        self.server.run = False # Stops server
        pass

    def create_principal(self, username, password):
        self._assert_access(self.principal == "admin")
        self._assert_success(not self.store.user_exists(username))
        self.store.modify_principal(username, password)

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
            self._parse_value(token)

    def set(self, field, expression):
        value = self._parse_expression(expression)
        self.apply_permissions(
            self.store.has_permission(self.principal, field, "write"),
            self._is_field(field),
            lambda self: self.store.set_field(field, value)
            )


    def append_to(self, field, expression):
        value = self._parse_expression(expression)
        self.apply_permissions(
            self.store.has_permission(self.principal, field, "append"),

            self.store.field_exists(field) and
            self.store.field_type(field) == list and
            self._is_field(field),

            lambda self: self.store.append_to(field, value)
            )

    def local(self, field, expression):
        value = self._parse_expression(expression)
        self.apply_permissions(
            True,

            not self.store.field_exists(field) and
            self._is_field(field),

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
            not self.store.field_exists(iterator) and
            self._is_field(iterator) and
            self._is_field(field),

            action
            )

    def set_delegation(self, field, authority, permission, user):
        self.apply_permissions(
            (self.principal == "admin" or self.principal == authority) and
            (self.store.has_permission(authority, field, "delegate") or
             field == "all"),

            (self.store.global_field_exists(field) or field == "all") and
            self.store.user_exists(user) and
            self.store.user_exists(authority) and
            self._is_field(field),

            lambda self: self.store.set_delegation(field, authority, permission, user)
            )

    def delete_delegation(self, field, authority, permission, user):
        self.apply_permissions(
            ((self.principal == "admin" or self.principal == authority) and
             (self.store.has_permission(authority, field, "delegate") or field == "all")) or
            (self.principal == user and field != "all"),

            self.store.shallow_field_exists(field) and
            self.store.user_exists(user) and
            self.store.user_exists(authority) and
            self._is_field(field),

            lambda self: self.store.delete_delegation(field, authority, permission, user)
            )

    def get_field(self, field):
        return self.apply_permissions(
            self.store.has_permission(self.principal, field, "read"),

            self.store.field_exists(field),

            lambda self: self.store.get_field(field)
            )

    def default_delegator(self, user):
        self.apply_permissions(
            self.principal == "admin",

            self.store.user_exists(user),

            lambda self: self.store.set_default(user)
            )

    # Used to make sure identifiers are fields and not attributes
    def _is_field(self, field):
        return field.count('.') == 0

    def _parse_expression(self, expression):
        if type(expression) == str:
            return expression

        elif type(expression) == list:
            if len(expression) > 0:
                raise RuntimeError("FAILED")
            else:
                return []

        elif type(expression) == dict:
            resolved_dict = {}
            for key in expression.keys():
                resolved_dict[key] = self._parse_value(expression[key])

            return resolved_dict

    def _parse_value(self, value):
        if type(value) == str:
            return value

        elif type(value) == LexToken:
            if value.type == "ID" or value.type == "ID_GROUP":
                if self.store.has_permission(self.principal, value.value):
                    if self.store.field_exists(value.value):
                        return self.store.get_field(value.value)
                    else:
                        raise RuntimeError("FAILED")
                else:
                    raise RuntimeError("DENIED")
            else:
                raise RuntimeError("Unknown token type")

# has_permission should return true if the field doesn't exist
