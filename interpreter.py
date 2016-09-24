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

class _TokenParser(object):
    def __init__(self, tokens):
        self.tokens = tokens

    def expect(self, *args):
        '''Removes and returns first element, or throws an error if types do not match'''
        next_token = self.next()
        if next_token == None:
            raise ValueError("Unexpected end of input")
        if next_token.type not in args:
            raise ValueError("Unexpected token")
        return next_token
    
    def next(self):
        '''Removes and returns first element or None if queue empty'''
        try:
            return self.tokens.pop(0)
        except IndexError:
            return None

class Interpreter(object):
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
                
                if token.value == "COMMAND":
                    #handle command
                    pass
                elif token.value == "TERMINATOR":
                    break
            #update store
        except Exception:
            #rollback changes
            pass
