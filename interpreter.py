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

    def _status_json(self, status):
        return '{"status":"' + status + '"}\n'

    def accept(self, parser):
        '''Accepts the parser and interprets provided tokens to perform actions on the store and server'''

        result = ""
        try:
            self._auth(parser)

            expected_line = 2
            while True:
                token = parser.expect("COMMAND")
                if token.lineno != expected_line:
                    raise RuntimeError("FAILED")
                expected_line = expected_line + 1

                cmd = token.value
                if cmd == "set":
                    self._set(parser)
                    result = result + self._status_json("SET")
                elif cmd == "create principal":
                    self._create_principal(parser)
                    result = result + self._status_json("CREATE_PRINCIPAL")
                elif cmd == "set delegation":
                    self._set_delegation(parser)
                    result = result + self._status_json("SET_DELEGATION")
                elif cmd == "change password":
                    self._change_password(parser)
                    result = result + self._status_json("CHANGE_PASSWORD")
                elif cmd == "append to":
                    self._append(parser)
                    result = result + self._status_json("APPEND")
                elif cmd == "local":
                    self._local(parser)
                    result = result + self._status_json("LOCAL")
                elif cmd == "foreach":
                    self._foreach(parser)
                    result = result + self._status_json("FOREACH")
                elif cmd == "delete delegation":
                    self._delete_delegation(parser)
                    result = result + self._status_json("DELETE_DELEGATION")
                elif cmd == "default delegator":
                    self._default_delegator(parser)
                    result = result + self._status_json("DEFAULT_DELEGATOR")
                elif cmd == "exit":
                    parser.expect("TERMINATOR")
                    for operation in self.operation_queue:
                        operation()
                    result = result + self._status_json("EXITING")
                    self.controller.end_transaction_exit(result)
                    break
                elif cmd == "return":
                    return_value = parser.expect(*EXPR)
                    parser.expect("TERMINATOR")
                    for operation in self.operation_queue:
                        operation()
                    value = self.controller.get_value(return_value)
                    result = result + '{"status":"RETURNING", "output":' + json.dumps(value) + '}'
                    self.controller.end_transaction(result)
                    break
                else:
                    raise ValueError("Unsupported command was provided")

        except RuntimeError as err:
            self.controller.return_error(err.args[0])
            pass
        return result

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

    def _change_password(self, parser):
        name = parser.expect("ID").value
        new_pass = parser.expect("STRING").value
        self.operation_queue.append(lambda: self.controller.change_password(name, new_pass))

    def _create_principal(self, parser):
        name = parser.expect("ID").value
        new_pass = parser.expect("STRING").value
        self.operation_queue.append(lambda: self.controller.create_principal(name, new_pass))

    def _append(self, parser):
        val = parser.expect("ID").value
        parser.expect("WITH")
        expr = self._parse_expr(parser)
        self.operation_queue.append(lambda: self.controller.append(val, expr))

    def _local(self, parser):
        variable = parser.expect("ID").value
        parser.expect("EQUAL")
        expr = self._parse_expr(parser)
        self.operation_queue.append(lambda: self.controller.local(variable, expr))

    def _foreach(self, parser):
        y = parser.expect("ID").value
        parser.expect("IN")
        x = parser.expect("ID").value
        parser.expect("REPLACEWITH")
        expr = self._parse_expr(parser)
        self.operation_queue.append(lambda: self.controller.foreach(y, x, expr))

    def _set_delegation(self, parser):
        tgt = parser.expect("ID", "ALL")
        q = parser.expect("ID").value
        right = parser.expect("RIGHT").value
        parser.expect("ARROW")
        p = parser.expect("ID").value
        self.operation_queue.append(lambda: self.controller.set_delegation(tgt, q, right, p))

    def _delete_delegation(self, parser):
        tgt = parser.expect("ID", "ALL")
        q = parser.expect("ID").value
        right = parser.expect("RIGHT").value
        parser.expect("ARROW")
        p = parser.expect("ID").value
        self.operation_queue.append(lambda: self.controller.delete_delegation(tgt, q, right, p))

    def _default_delegator(self, parser):
        parser.expect("EQUAL")
        user = parser.expect("ID").value
        self.operation_queue.append(lambda: self.controller.default_delegator(user))
