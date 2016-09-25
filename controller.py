#!/usr/bin/python2

from store import Store
import ply.lex as lex

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

    def end_transaction(self, result):
        # apply changes and submit result
        pass

    def end_transaction_exit(self, result):
        # apply changes, check for permission, submit result and exit
        pass

    def return_error(self, msg):
        # return {"status":"msg"} to client and rollback
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
            self.store.has_permission(authority, field, "delegate"),

            self.store.shallow_field_exists(field) and
            self.store.user_exists(user) and
            self.store.user_exists(authority),

            lambda self: self.store.set_delegation(field, authority, permission, user)
            )

    def delete_delegation(self, field, authority, permission, user):
        self.apply_permission(
            self.principal == "admin" or
            (self.principal == authority and self.store.has_permission(authority, field, "delegate")) or
            self.principal == user,

            self.store.shallow_field_exists(field) and
            self.store.user_exists(user) and
            self.store.user_exists(authority),

            lambda self: self.store.delete_delegation(field, authority, permission, user)
            )

    def default_delegator(self, user):
        pass

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
