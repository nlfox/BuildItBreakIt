#!/usr/bin/python2

class _TokenParser(object):
    def __init__(self, tokens):
        self.tokens = tokens

    # Removes and returns first element and throws error if types don't match
    def expect(self, token_type):
        next_token = self.next()
        if next_token.type != token_type:
            raise ValueError("Got unexpected token")
        return next_token
    
    # Pemoves and returns first element or None if empty
    def next(self):
        try:
            return self.tokens.pop(0)
        except IndexError:
            return None

def accept_tokens(tokens):
    parser = _TokenParser(tokens)
    
    try:
        while True:
            command = parser.expect("COMMAND")
            #execute command
    except Exception:
        #rollback changes
        pass
