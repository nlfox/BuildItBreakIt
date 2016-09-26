#!/usr/bin/python

from store import Store
from controller import Controller
from interpreter import Interpreter
from parser import Lexer

request = '''

as principal admin password "admin" do
create principal alice "password"
set x = "test"
set delegation x admin read -> alice
return x
***

'''.strip()

request2 = '''

as principal alice password "password" do
return x
***

'''.strip()

if __name__ == '__main__':
    store = Store("admin")
    controller = Controller(store, None)
    interpreter = Interpreter(controller)
    print interpreter.accept(Lexer(request))
    print interpreter.accept(Lexer(request2))

