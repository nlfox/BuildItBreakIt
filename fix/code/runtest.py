#!/usr/bin/python

from store import Store
from controller import Controller
from interpreter import Interpreter
from parser import Lexer
from argparse import ArgumentParser
import json

requests = ['''
as principal admin password \"admin\" do\ncreate principal bob \"B0BPWxxd\"\nset x = \"my string\"\nset delegation x admin read -> bob\nreturn x\n***\n
'''.strip()]

if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument("file", type=str)
    args = argparser.parse_args()
    filename = args.file
    f = open(filename, 'r')
    test = json.loads(f.read())

    store = Store("admin")
    controller = Controller(store, None)
    interpreter = Interpreter(controller)

    for program in test["programs"]:
        print program["program"].decode("string-escape")
        print "Expected:"
        for line in program["output"]:
            print json.dumps(line).replace(": ", ":")
        print
        print "Actual:"
        print interpreter.accept(program["program"])
        print
        print

