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

class Interpreter(object):
    def __init__(self, controller):
        self.controller = controller
        self.operation_queue = []

    def accept(self, parser):
        '''Accepts the parser and interprets provided tokens to perform actions on the store and server'''
        
        result = ""
        try:
            # authenticate user
            parser.expect("AS_PRINCIPAL")
            username = parser.expect("ID").value
            parser.expect("PASSWORD")
            password = parser.expect("STRING").value
            parser.expect("DO")

            self.controller.begin_transaction(username, password)

            # read commands
            expected_line = 2
            while True:
                token = parser.expect("COMMAND", "TERMINATOR")
                
                if token.lineno != expected_line:
                    raise RuntimeError("FAILED")

                if token.type == "COMMAND":
                    cmd = token.value
                    if cmd == "set":
                        _parse_set(parser)
                    else:
                        raise ValueError("Unsupported command was provided")
                # terminate command block
                elif token.type == "TERMINATOR":
                    break

                expected_line = expected_line + 1
            for operation in self.operation_queue:
                operation()
            self.controller.accept_changes()
        except Exception:
            self.controller.rollback()
            pass
        return result

    def _parse_dict(self, parser):
        dictionary = []
        while True:
            key = parser.expect("ID")
            parser.expect("EQUAL")
            value = parser.expect("ID", "STRING")
            dictionary[key] = value
            next_token = parser.expect("COMMA", "RCURLYPAREN")
            if next_token.type == "RCURLYPAREN":
                break
        return dictionary

    def _parse_set(self, parser):
        variable = parser.expect("ID").value
        parser.expect("EQUAL")
        next_token = parser.expect("ID", "STRING", "LCURLYPAREN")
        if next_token.type == "LCURLYPAREN":
            token_dict = self._parse_dict(parser)
            self.controller.set(variable, token_dict)
        else:
            self.controller.set(variable, next_token)
