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
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'while': 'WHILE',
        'as': 'AS',
        'principal': 'PRINCIPAL',
        'password': 'PASSWORD',
        'do': 'DO',
        'exit': 'EXIT',
        'return': 'RETURN',
        'create': 'CREATE',
        'change': 'CHANGE',
        'set': 'SET',
        'append': 'APPEND',
        'to': 'TO',
        'with': 'WITH',
        'local': 'LOCAL',
        'foreach': 'FOREACH',
        'in': 'IN',
        'replacewith': 'REPLACEWITH',
        'delegation': 'DELEGATION',
        'default': 'DEFAULT',
        'delegator': 'DELEGATOR',
        'read': 'READ',
        'write': 'WRITE',
        'delete': 'DELETE'
    }

    # List of token names.   This is always required
    tokens = [
                 'ID',
                 'NUMBER',
                 'PLUS',
                 'MINUS',
                 'TIMES',
                 'DIVIDE',
                 'LPAREN',
                 'RPAREN',
                 'STRING',
                 'COMMAND',
                 'TERMINATOR',
                 'LSQUBRA',
                 'RSQUBRA',
                 'ID_GROUP'
             ] + list(reserved.values())

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LSQUBRA = r'\['
    t_RSQUBRA = r'\]'
    t_EQUAL = r'='
    t_COMMA = r','
    t_AS = r'as'
    t_PRINCIPAL = r'principal'
    t_PASSWORD = r'password'
    t_DO = r'do'
    t_EXIT = r'exit'
    t_RETURN = r'return'
    t_CREATE = r'create'
    t_CHANGE = r'change'
    t_SET = r'set'
    t_APPEND = r'append'
    t_TO = r'to'
    t_WITH = r'with'
    t_LOCAL = r'local'
    t_FOREACH = r'foreach'
    t_IN = r'in'
    t_REPLACEWITH = r'replacewith'
    t_DELEGATION = r'delegation'
    t_DELETE = r'delete'
    t_DEFAULT = r'default'
    t_DELEGATOR = r'delegator'
    t_READ = r'read'
    t_WRITE = r'write'
    t_ARROW = r'->'
    t_TERMINATOR = r'\*\*\*'

    # This position has the highest priority
    # TODO: add more command
    def t_COMMAND(self, t):
        r'as\ +principal|create\ +principal|change\ +password|append\ +to|set\ +delegation|delete\ +delegation|default\ +delegator'
        t.value = " ".join(t.value.split())
        return t

    def t_ID_GROUP(self, t):
        r'([a-zA-Z0-9]+\.){1,}[a-zA-Z0-9]+'
        t.value = t.value.split(".")
        return t

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

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
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

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
            raise ValueError("Unexpected token")
        return next_token

    def next(self):
        return self.gen.next()

    def __init__(self, data="", **kwargs):
        self.data = data
        self.lexer = lex.lex(module=self, **kwargs)
        self.gen = self._initGen()
        pass


# Test it out
data = '''
as  principal    set  delegate admin  "as principle" u do  -> set xa.ya.zzz = "1" [] *** exit as
'''

# OUTPUT:
# PARSE: LexToken(AS, 'as',...)

m = Lexer(data)

for i in m.gen:
    print i
