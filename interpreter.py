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


class Interpreter(object):
    def __init__(self, controller):
        self.controller = controller
        self.operation_queue = []
        self.result = ""
        self.flag = False

    def _execute_operations(self):
        for operation in self.operation_queue:
            operation()
        self.operation_queue = []

    def accept(self, parser):
        """Accepts the parser and interprets provided tokens to perform actions on the store and server"""

        self.result = ""
        self.flag = True
        try:
            self._auth(parser)
            while self.flag:
                parser.expect("NEWLINE")
                token = parser.expect("COMMAND")  # Checking for terminator not needed since return or exit is needed first
                try:
                    getattr(self, "_" + "_".join(token.value.split(" ")))(parser)
                except AttributeError:
                    raise NotImplementedError("Unknown command: " + token.value)

        except RuntimeError as err:
            return _status_json(err.args[0])
        return self.result

    def _parse_expr(self, parser):
        token = parser.expect("ID", "ID_GROUP", "STRING", "LCURLYPAREN")
        if token.type == "LCURLYPAREN":
            return self._parse_dict(parser)
        return token

    def _parse_dict(self, parser):
        dictionary = {}
        while True:
            key = parser.expect("ID").value
            parser.expect("EQUAL")
            value = parser.expect("ID", "ID_GROUP", "STRING")
            dictionary[key] = value
            next_token = parser.expect("COMMA", "RCURLYPAREN")
            if next_token.type == "RCURLYPAREN":
                break
        return dictionary

    def _auth(self, parser):
        parser.expect("PROG")
        username = parser.expect("ID").value
        parser.expect("PASSWORD")
        password = parser.expect("STRING").value
        parser.expect("DO")
        self.controller.begin_transaction(username, password)

    def _set(self, parser):
        variable = parser.expect("ID").value
        parser.expect("EQUAL")
        expr = self._parse_expr(parser)
        self.operation_queue.append(lambda: self.controller.set(variable, expr))
        self.result += _status_json("SET")

    def _change_password(self, parser):
        name = parser.expect("ID").value
        new_pass = parser.expect("STRING").value
        self.operation_queue.append(lambda: self.controller.change_password(name, new_pass))
        self.result += _status_json("CHANGE_PASSWORD")

    def _create_principal(self, parser):
        name = parser.expect("ID").value
        new_pass = parser.expect("STRING").value
        self.operation_queue.append(lambda: self.controller.create_principal(name, new_pass))
        self.result += _status_json("CREATE_PRINCIPAL")

    def _append_to(self, parser):
        val = parser.expect("ID").value
        parser.expect("WITH")
        expr = self._parse_expr(parser)
        self.operation_queue.append(lambda: self.controller.append(val, expr))
        self.result += _status_json("APPEND")

    def _local(self, parser):
        variable = parser.expect("ID").value
        parser.expect("EQUAL")
        expr = self._parse_expr(parser)
        self.operation_queue.append(lambda: self.controller.local(variable, expr))
        self.result += _status_json("LOCAL")

    def _foreach(self, parser):
        y = parser.expect("ID").value
        parser.expect("IN")
        x = parser.expect("ID").value
        parser.expect("REPLACEWITH")
        expr = self._parse_expr(parser)
        self.operation_queue.append(lambda: self.controller.foreach(y, x, expr))
        self.result += _status_json("FOREACH")

    def _set_delegation(self, parser):
        tgt = parser.expect("ID", "ALL").value
        q = parser.expect("ID").value
        right = parser.expect("RIGHT").value
        parser.expect("ARROW")
        p = parser.expect("ID").value
        self.operation_queue.append(lambda: self.controller.set_delegation(tgt, q, right, p))
        self.result += _status_json("SET_DELEGATION")

    def _delete_delegation(self, parser):
        tgt = parser.expect("ID", "ALL").value
        q = parser.expect("ID").value
        right = parser.expect("RIGHT").value
        parser.expect("ARROW")
        p = parser.expect("ID").value
        self.operation_queue.append(lambda: self.controller.delete_delegation(tgt, q, right, p))
        self.result += _status_json("DELETE_DELEGATION")

    def _default_delegator(self, parser):
        parser.expect("EQUAL")
        user = parser.expect("ID").value
        self.operation_queue.append(lambda: self.controller.default_delegator(user))
        self.result += _status_json("DEFAULT_DELEGATOR")

    def _exit(self, parser):
        parser.expect("NEWLINE")
        parser.expect("TERMINATOR")
        self._execute_operations()
        result = self.result + _status_json("EXITING")
        self.controller.end_transaction_exit()
        self.flag = False

    def _return(self, parser):
        return_value = self._parse_expr(parser)
        parser.expect("NEWLINE")
        parser.expect("TERMINATOR")
        self._execute_operations()
        value = self.controller.get_value(return_value)
        self.result += '{"status":"RETURNING", "output":' + json.dumps(value) + '}'
        self.controller.end_transaction()
        self.flag = False


def _status_json(status):
    return '{"status":"' + status + '"}\n'
