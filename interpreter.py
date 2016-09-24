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

    # Removes and returns first element and throws error if types don't match
    def expect(self, *args):
        next_token = self.next()
        if next_token == None:
            raise ValueError("Unexpected end of input")
        if next_token.type not in args:
            raise ValueError("Unexpected token")
        return next_token
    
    # Pemoves and returns first element or None if empty
    def next(self):
        try:
            return self.tokens.pop(0)
        except IndexError:
            return None

class Interpreter(object):
    # custom init command to be called after actual initialization 
    def init(self, store, server):
        self.store = store
        self.server = server

    def accept_tokens(self, tokens):
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
