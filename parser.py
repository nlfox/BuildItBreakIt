# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

class Lexer(object):
    # Regular expression rules for simple tokens
    reserved = {
        '=': 'EQUAL',
        '->': 'ARROW',
        '{': 'LCURLYPAREN',
        '}': 'RCURLYPAREN',
        ',': 'COMMA',
        'do': 'DO',
        'exit': 'EXIT',
        'return': 'RETURN',
        'set': 'SET',
        'to': 'TO',
        'with': 'WITH',
        'local': 'LOCAL',
        'foreach': 'FOREACH',
        'in': 'IN',
        'replacewith': 'REPLACEWITH',
        'read': 'RIGHT',
        'write': 'RIGHT',
        'append': 'RIGHT',
        'delegate': 'RIGHT',
        'date' : 'DATE',
        'password' : "PASSWORD"
    }

    # List of token names.   This is always required
    tokens = [
                 'ID',
                 'NUMBER',
                 'LPAREN',
                 'RPAREN',
                 'STRING',
                 'COMMAND',
                 'TERMINATOR',
                 'SQUBRACKETS',
                 'ID_GROUP',
                 'PROG',
                 'NEWLINE'
             ] + list(reserved.values())
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_SQUBRACKETS = r'\[\]'
    t_EQUAL = r'='
    t_COMMA = r','
    t_DO = r'do'
    t_EXIT = r'exit'
    t_RETURN = r'return'
    t_SET = r'set'
    t_TO = r'to'
    t_WITH = r'with'
    t_LOCAL = r'local'
    t_FOREACH = r'foreach'
    t_IN = r'in'
    t_REPLACEWITH = r'replacewith'
    t_ARROW = r'->'
    t_TERMINATOR = r'\*\*\*'
    t_DATE = r'date'
    t_RIGHT = r'read|write|append|delegate'

    # This position has the highest priority
    # TODO: add more command
    def t_COMMAND(self, t):
        r'create\ +principal|change\ +password|append\ +to|set\ +delegation|delete\ +delegation|default\ +delegator'
        t.value = " ".join(t.value.split())
        return t

    def t_PROG(self, t):
        r'as\ +principal'
        t.value = " ".join(t.value.split())
        return t

    def t_ID_GROUP(self, t):
        r'[a-zA-Z0-9]+\.[a-zA-Z0-9]+'
        return t

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += len(t.value)
        return t

    def t_STRING(self, t):
        r'"[A-Za-z0-9_ ,;\.?!-]*"'
        t.type = "STRING"
        t.value = t.value[1:-1]
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        raise RuntimeError("FAILED")

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    def tokenize(self):
        self.lexer.input(self.data)
        r = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            r += [tok]
        return r

    def _initGen(self):
        self.lexer.input(self.data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            yield tok

    def expect(self, *args):
        '''Removes and returns first element, or throws an error if types do not match'''
        next_token = self.next()
        if next_token.type not in args:
            print "expected " + str(args) + " but got " + next_token.type
            raise RuntimeError("FAILED")
        return next_token

    def next(self):
        return self.gen.next()

    def __init__(self, data="", **kwargs):
        self.data = data
        self.lexer = lex.lex(module=self,errorlog=lex.NullLogger(), **kwargs)
        self.gen = self._initGen()
        pass


# Test it out
data = '''
as  principal read write delegate append set  delegate admin  "as principle" u do  -> set xa.y = "1" [] *** exit as
'''

# OUTPUT:
# PARSE: LexToken(AS, 'as',...)

m = Lexer(data)

for i in m.gen:
    print i
