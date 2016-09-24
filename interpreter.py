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

from parser import Lexer as _TokenParser


class Interpreter(object):
    def __init__(self):
        self.operation_queue = []

    def init(self, store, server):
        '''Custom init command to be called after the actual initialization'''
        self.store = store
        self.server = server

    def accept_tokens(self, tokens):
        '''Accepts a list of LexTokens and interprets it to perform actions on the store and server'''
        parser = _TokenParser(tokens)

        try:
            while True:
                token = parser.expect("COMMAND", "TERMINATOR")
                if token.type == "COMMAND":
                    # handle command
                    pass
                elif token.type == "TERMINATOR":
                    break
            for operation in self.operation_queue:
                operation()
        except Exception:
            # rollback changes
            pass

    def _parse_dict(self, parser):
        '''Parses and returns dictionary using the parser, expects opening brace to be already parsed.
        Resulting dictionary's values will be LexTokens'''

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
        variable = parser.expect("ID")
        parser.expect("EQUAL")
        next_token = parser.expect("ID", "STRING", "LCURLYPAREN")
        if next_token.type == "ID":
            pass
        elif next_token.type == "STRING":
            pass
        elif next_token.type == "LCURLYPAREN":
            dictionary = self._parse_dict(parser)
            pass
