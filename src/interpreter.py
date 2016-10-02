#!/usr/bin/python2

# --------------------------------------#
# Interpreter module                   #
# --------------------------------------#
# Accepts a list of LexTokens and      #
# interprets it to perform actions on  #
# the store and server                 #
# --------------------------------------#
# Important methods:                   #
# - Interpreter::init(store, server)   #
# - Interpreter::accept_tokens(tokens) #
# --------------------------------------#

import json
from parser import Lexer
import traceback


class Interpreter(object):
    def __init__(self, controller):
        self.controller = controller
        self.operation_queue = []
        self.result = ""
        self.flag = False
        self.parser = Lexer()

    def _execute_operations(self):
        for operation in self.operation_queue:
            operation()
        self.operation_queue = []

    def accept(self, data):
        """Accepts the parser and interprets provided tokens to perform actions on the store and server"""
        if len(data) > 1000000:
            return _status_json("FAILED")

        self.result = []
        self.flag = True
        parser = self.parser.setNewData(data)
        try:
            self._auth()
            while self.flag:
                self.parser.expect("NEWLINE")
                token = self.parser.expect("COMMAND")  # Checking for terminator not needed since return or exit is needed first
                #try:
                getattr(self, "_" + "_".join(token.value.split(" ")))()
                #except AttributeError:
                 #   print "_" + "_".join(token.value.split(" "))
                  #  raise NotImplementedError("Unknown command: " + token.value)

        except RuntimeError as err:
#            traceback.print_exc()
            self.operation_queue = []
            return _status_json(err.args[0])
        return ''.join(self.result)

    def _parse_expr(self, variable):
        token = self.parser.expect("ID", "ID_GROUP", "STRING", "LCURLYPAREN", "SQUBRACKETS", "STRFUNC")
        if token.type == "SQUBRACKETS":
            return []
        if token.type == "LCURLYPAREN":
            return self._parse_dict()
        if token.type == "STRFUNC":
            return self._parse_func(token.value, variable)
        return token

    def _parse_func(self, func, variable):
        if func == "tolower":
            self.parser.expect("LPAREN")
            arg = self.parser.expect("ID", "ID_GROUP", "STRING")
            self.parser.expect("RPAREN")
            return lambda: self.controller.tolower(variable, arg)
        else:
            self.parser.expect("LPAREN")
            fstarg = self.parser.expect("ID", "ID_GROUP", "STRING")
            self.parser.expect("COMMA")
            sndarg = self.parser.expect("ID", "ID_GROUP", "STRING")
            self.parser.expect("RPAREN")
            if func == "concat":
                return lambda: self.controller.tolower(variable, fstarg, sndarg)
            else:
                return lambda: self.controller.split(variable, fstarg, sndarg)

    def _parse_dict(self):
        dictionary = {}
        while True:
            key = self.parser.expect("ID").value
            if key in dictionary:
                raise RuntimeError("FAILED")

            self.parser.expect("EQUAL")
            value = self.parser.expect("ID", "ID_GROUP", "STRING")
            dictionary[key] = value
            next_token = self.parser.expect("COMMA", "RCURLYPAREN")
            if next_token.type == "RCURLYPAREN":
                break
        return dictionary

    def _auth(self):
        self.parser.expect("PROG")
        username = self.parser.expect("ID").value
        self.parser.expect("PASSWORD")
        password = self.parser.expect("STRING").value
        self.parser.expect("DO")
        self.controller.begin_transaction(username, password)

    def _set(self):
        variable = self.parser.expect("ID").value
        self.parser.expect("EQUAL")
        expr = self._parse_expr()
        if type(expr) == dict or type(expr) == list or type(expr) == str:
            self.operation_queue.append(lambda: self.controller.set(variable, expr))
        else:
            self.operation_queue.append(expr)
        self.result.append(_status_json("SET"))

    def _change_password(self):
        name = self.parser.expect("ID").value
        new_pass = self.parser.expect("STRING").value
        self.operation_queue.append(lambda: self.controller.change_password(name, new_pass))
        self.result.append(_status_json("CHANGE_PASSWORD"))

    def _create_principal(self):
        name = self.parser.expect("ID").value
        new_pass = self.parser.expect("STRING").value
        self.operation_queue.append(lambda: self.controller.create_principal(name, new_pass))
        self.result.append(_status_json("CREATE_PRINCIPAL"))

    def _append_to(self):
        val = self.parser.expect("ID").value
        self.parser.expect("WITH")
        expr = self._parse_expr()
        self.operation_queue.append(lambda: self.controller.append_to(val, expr))
        self.result.append(_status_json("APPEND"))

    def _local(self):
        variable = self.parser.expect("ID").value
        self.parser.expect("EQUAL")
        expr = self._parse_expr()
        self.operation_queue.append(lambda: self.controller.local(variable, expr))
        self.result.append(_status_json("LOCAL"))

    def _foreach(self):
        y = self.parser.expect("ID").value
        self.parser.expect("IN")
        x = self.parser.expect("ID").value
        self.parser.expect("REPLACEWITH")
        expr = self._parse_expr()
        self.operation_queue.append(lambda: self.controller.foreach(y, x, expr))
        self.result.append(_status_json("FOREACH"))

    def _set_delegation(self):
        tgt = self.parser.expect("ID", "ALL").value
        q = self.parser.expect("ID").value
        right = self.parser.expect("RIGHT").value
        self.parser.expect("ARROW")
        p = self.parser.expect("ID").value
        self.operation_queue.append(lambda: self.controller.set_delegation(tgt, q, right, p))
        s = _status_json("SET_DELEGATION")
        self.result.append(s)

    def _delete_delegation(self):
        tgt = self.parser.expect("ID", "ALL").value
        q = self.parser.expect("ID").value
        right = self.parser.expect("RIGHT").value
        self.parser.expect("ARROW")
        p = self.parser.expect("ID").value
        self.operation_queue.append(lambda: self.controller.delete_delegation(tgt, q, right, p))
        self.result.append(_status_json("DELETE_DELEGATION"))

    def _default_delegator(self):
        self.parser.expect("EQUAL")
        user = self.parser.expect("ID").value
        self.operation_queue.append(lambda: self.controller.default_delegator(user))
        self.result.append(_status_json("DEFAULT_DELEGATOR"))

    def _exit(self):
        self.parser.expect("NEWLINE")
        self.parser.expect("TERMINATOR")
        self._execute_operations()
        self.result.append(_status_json("EXITING"))
        self.controller.end_transaction_exit()
        self.flag = False

    def _return(self):
        return_value = self._parse_expr()
        self.parser.expect("NEWLINE")
        self.parser.expect("TERMINATOR")
        self._execute_operations()
        value = self.controller.get_value(return_value)
        self.result.append('{"status":"RETURNING", "output":%s}' % (json.dumps(value)))
        self.controller.end_transaction()
        self.flag = False


def _status_json(status):
    return '{"status":"%s"}\n' % (status)
