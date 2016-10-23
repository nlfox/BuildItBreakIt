# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import lex


class Lexer(object):
    # Regular expression rules for simple tokens
    reserved = {
        'do': 'DO',
        'to': 'TO',
        'with': 'WITH',
        'in': 'IN',
        'replacewith': 'REPLACEWITH',
        'read': 'RIGHT',
        'write': 'RIGHT',
        'append': 'RIGHT',
        'delegate': 'RIGHT',
        'password': "PASSWORD",
        'all': "ALL",
        'let': "LET",
    }

    # List of token names.   This is always required
    tokens = [
                 'ID',
                 'NUMBER',
                 'COMMA',
                 'LPAREN',
                 'RPAREN',
                 'STRING',
                 'LET',
                 'COMMAND',
                 'STRFUNC',
                 'TERMINATOR',
                 'SQUBRACKETS',
                 'ID_GROUP',
                 'PROG',
                 'NEWLINE',
                 'LISTFILTER',
                 'EQUAL',
                 'ARROW',
                 'LCURLYPAREN',
                 'RCURLYPAREN',
                 'COMMENT'
             ] + list(reserved.values())
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LCURLYPAREN = r'\{'
    t_RCURLYPAREN = r'\}'
    t_SQUBRACKETS = r'\[\]'
    t_EQUAL = r'='
    t_COMMA = r','
    t_DO = r'\ {1,}do'
    t_WITH = r'\ {1,}with\ {1,}'
    t_IN = r'\ {1,}in\ {1,}'
    t_PASSWORD = r'\ {1,}password\ {1,}'
    t_REPLACEWITH = r'\ {1,}replacewith\ {1,}'
    t_ARROW = r'->'
    t_TERMINATOR = r'\*\*\*'
    t_RIGHT = r'\ {1,}(read|write|append|delegate)'
    t_ALL = r'\ {1,}all\ {1,}'
    t_LET = r'\ {1,}let\ {1,}'

    # This position has the highest priority
    # TODO: add more command
    def t_COMMAND(self, t):
        r'(create\ +principal|change\ +password|append\ +to|set\ +delegation|set|delete\ +delegation|default\ +delegator|local|return|exit|foreach|filtereach)\ {1,}'
        t.value = " ".join(t.value.split())
        return t

    def t_STRFUNC(self, t):
        r'\b(split)\b|\b(concat)\b|\b(tolower)\b'
        #| ^ concat$ | ^ tolower$
        return t

    def t_LISTFILTER(self, t):
        r'equal|notequal{1,}'
        return t

    def t_PROG(self, t):
        r'as\ +principal{1,}'
        t.value = " ".join(t.value.split())
        return t

    def t_COMMENT(self, t):
        r'\n?\/\/[A-Za-z0-9_\ ,;\.?!-]*'
        pass

    def t_ID_GROUP(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*\.[a-zA-Z][a-zA-Z0-9_]*'
        return t

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_NEWLINE(self, t):
        r'\n|\r\n'
        t.lexer.lineno += len(t.value)
        return t

    def t_STRING(self, t):
        r'"[A-Za-z0-9_ ,;\.?!-]{,65535}"'
        t.type = "STRING"
        t.value = t.value[1:-1]
        return t

    def t_ID(self, t):
        r'[a-zA-Z][a-zA-Z0-9_]*(?!\")'
        t.type = self.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' '

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
        next = self.gen.next()
        print next
        return next

    def __init__(self, data="", **kwargs):
        self.data = data
        self.lexer = lex.lex(module=self, errorlog=lex.NullLogger(), **kwargs)
        self.gen = self._initGen()

    def setNewData(self, data):
        self.data = data
        self.gen = self._initGen()
