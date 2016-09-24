# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# Reserved words
reserved = {
    '=' : 'EQUAL',
    '->' : 'ARROW',
    '{' : 'CLPAREN',
    '}' : 'CRPAREN',
    '[' : 'SLPAREN',
    ']' : 'SRPAREN',
    ',' : 'COMMA',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'as' : 'AS',
    'principal' : 'PRINCIPAL',
    'password' : 'PASSWORD',
    'do' : 'DO',
    'exit' : 'EXIT',
    'return' : 'RETURN',
    'create' : 'CREATE',
    'change' : 'CHANGE',
    'set' : 'SET',
    'append' : 'APPEND',
    'to' : 'TO',
    'with' : 'WITH',
    'local' : 'LOCAL',
    'foreach' : 'FOREACH',
    'in' : 'IN',
    'replacewith' : 'REPLACEWITH',
    'delegation' : 'DELEGATION',
    'default' : 'DEFAULT',
    'delegator' : 'DELEGATOR',
    'read' : 'READ',
    'write' : 'WRITE',
    'delete' : 'DELETE'
}

# List of token names.   This is always required
tokens = [
             'ID',
             'NUMBER',
             'PLUS',
             'MINUS',
             'TIMES',
             'DIVIDE',
             'OLPAREN',
             'ORPAREN',
             'STRING'] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_OLPAREN = r'\('
t_ORPAREN = r'\)'
t_SRPAREN = r'\]'
t_SLPAREN = r'\['
t_CLPAREN = r'\{'
t_CRPAREN = r'\}'
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


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_STRING(t):
    r'\"[a-zA-Z_][a-zA-Z0-9]*\"'
    t.type = "STRING"
    t.value = t.value[1:-1]
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


def main():
    # Test it out
    data = '''
    as principal admin "password" u, "1-1" {} do ->
    exit
    '''

    # OUTPUT:
    # PARSE: LexToken(AS, 'as',...)


    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)


main()
