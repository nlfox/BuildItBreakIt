#!/usr/bin/python2

from store import Store
from lex import LexToken


class Controller:
    def __init__(self, store, server):
        self.principal = ""
        self.store = store
        self.server = server

    def _error(self, message):
        self.store.discard_transaction()
        raise RuntimeError(message)

    def _assert_access(self, condition):
        if not condition:
            self._error("DENIED")

    def _assert_success(self, condition):
        if not condition:
            self._error("FAILED")

    def begin_transaction(self, principal, password):
        self._assert_success(self.store.user_exists(principal))
        self._assert_access(self.store.check_password(principal, password))
        self.principal = principal
        self.store.begin_transaction(principal)

    def end_transaction(self):
        self.store.complete_transaction()

    def end_transaction_exit(self):
        self._assert_access(self.principal == "admin")
        self.store.complete_transaction()
        self.server.run = False  # Stops server
        pass

    def create_principal(self, username, password):
        self._assert_access(self.principal == "admin")
        self._assert_success(not self.store.user_exists(username))
        self.store.modify_principal(username, password)

    def change_password(self, username, password):
        self._assert_access(self.principal == "admin" or self.principal == username)
        self._assert_success(self.store.user_exists(username))
        self.store.modify_principal(username, password)

    def get_value(self, token):
        # evaluate token value and return that
        if type(token) is dict:
            return token
        else:
            return self._parse_value(token)

    def set(self, field, expression):
        value = self._parse_expression(expression)
        self._assert_access(self.store.has_permission(self.principal, field, "write"))
        self._assert_success(is_field(field))
        self.store.set_field(field, value)

    def append_to(self, field, expression):
        value = self._parse_expression(expression)
        self._assert_access(self.store.has_permission(self.principal, field, "append"))
        self._assert_success(
            self.store.field_exists(field) and
            self.store.field_type(field) == list and
            is_field(field))
        self.store.append_to(field, value)

    def local(self, field, expression):
        value = self._parse_expression(expression)
        self._assert_access(
            not self.store.field_exists(field) and
            is_field(field))
        self.store.set_local(field, value)

    def foreach(self, iterator, field, expression):
        self._assert_access(
            self.store.has_permission(self.principal, field, "read") and
            self.store.has_permission(self.principal, field, "write"))
        self._assert_success(
            self.store.field_exists(field) and
            self.store.field_type(field) == list and
            not self.store.field_exists(iterator) and
            is_field(iterator) and
            is_field(field))
        l = self.store.get_field(field)
        new_value = []
        for element in l:
            self.store.set_local(iterator, element)
            value = self._parse_expression(expression)
            new_value.append(value)
        self.store.remove_local(iterator)
        self.set(field, new_value)

    def set_delegation(self, field, authority, permission, user):
        self._assert_access(
            (self.principal == "admin" or self.principal == authority) and
            (self.store.has_permission(authority, field, "delegate") or
             field == "all"))
        self._assert_success(
            (self.store.global_field_exists(field) or field == "all") and
            self.store.user_exists(user) and
            self.store.user_exists(authority) and
            is_field(field))
        self.store.set_delegation(field, authority, permission, user)

    def delete_delegation(self, field, authority, permission, user):
        self._assert_access(
            ((self.principal == "admin" or self.principal == authority) and
             (self.store.has_permission(authority, field, "delegate") or field == "all")) or
            (self.principal == user and field != "all"))
        self._assert_success(
            self.store.shallow_field_exists(field) and
            self.store.user_exists(user) and
            self.store.user_exists(authority) and
            is_field(field))
        self.store.delete_delegation(field, authority, permission, user)

    def get_field(self, field):
        self._assert_access(self.store.has_permission(self.principal, field, "read"))
        self._assert_success(self.store.field_exists(field))
        self.store.get_field(field)

    def default_delegator(self, user):
        self._assert_access(self.principal == "admin")
        self._assert_success(self.store.user_exists(user))
        self.store.set_default(user)

    def _parse_expression(self, expression):
        if type(expression) is LexToken:
            return self._parse_value(expression)
        elif type(expression) is list:
            return expression
        elif type(expression) is dict:
            resolved_dict = {}
            for key in expression.keys():
                value = self._parse_value(expression[key])
                self._assert_success(type(value) == str)
                resolved_dict[key] = value
            return resolved_dict
        else:
            self._error("FAILED")

    def _parse_value(self, value):
        if value.type == "ID" or value.type == "ID_GROUP":
            self._assert_access(self.store.has_permission(self.principal, value.value, "read"))
            self._assert_success(self.store.field_exists(value.value))
            return self.store.get_field(value.value)
        elif value.type == "STRING":
            return str(value.value)
        else:
            raise NotImplementedError("Unknown token type: " + value.type)


def is_field(field):
    """Used to make sure identifiers are fields and not attributes"""
    return field.count('.') == 0
