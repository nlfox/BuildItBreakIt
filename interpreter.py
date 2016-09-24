#!/usr/bin/python2

#--------------------------------------#
# Interpreter module                   #
#--------------------------------------#
# Accepts a list of LexTokens and      #
# interprets it to perform actions on  #
# the store and server                 #
#--------------------------------------#
# Important methods:                   #
# - Interpreter::init(store, server)   #
# - Interpreter::accept_tokens(tokens) #
#--------------------------------------#

EXPR = ["ID", "ID_GROUP", "STRING", "LCURLYPAREN", "STR_FN"]

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
                    result = result + self._satus_json("CREATE_PRINCIPAL")
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
                    result = parser.expect(*EXPR)
                    parser.expect("TERMINATOR")
                    for operation in self.operation_queue:
                        operation()
                    value = self.controller.get_value(result)
                    result = result + self._status_json('RETURNING", "output":"' + result)
                    self.controller.end_transaction(result)
                    break
                else:
                    raise ValueError("Unsupported command was provided")

        except Exception:
            self.controller.rollback()
            pass
        return result

    def _parse_dict(self, parser):
        dictionary = {}
        while True:
            key = parser.expect("ID")
            parser.expect("EQUAL")
            value = parser.expect("ID", "ID_GROUP", "STRING")
            dictionary[key] = value
            next_token = parser.expect("COMMA", "RCURLYPAREN")
            if next_token.type == "RCURLYPAREN":
                break
        return dictionary

    def _auth(self, parser):
        parser.expect("AS_PRINCIPAL")
        username = parser.expect("ID").value
        parser.expect("PASSWORD")
        password = parser.expect("STRING").value
        parser.expect("DO")

        self.controller.begin_transaction(username, password)

    def _set(self, parser):
        variable = parser.expect("ID", "ID_GROUP")
        parser.expect("EQUAL")
        next_token = parser.expect(*EXPR)
        if next_token.type == "LCURLYPAREN":
            token_dict = self._parse_dict(parser)
            self.controller.set(variable, token_dict)
        else:
            self.controller.set(variable, next_token)
