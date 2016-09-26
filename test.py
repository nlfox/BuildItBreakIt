#!/usr/bin/python

from store import Store
from controller import Controller
from interpreter import Interpreter
from parser import Lexer

requests = ['''

as principal admin password "admin" do
create principal alice "password"
set x = "test"
set y = "test2"
set delegation x admin read -> alice
set delegation y admin write -> alice
return x
***

'''.strip(), '''

as principal alice password "password" do
set y = "testerino"
return x
***

'''.strip(), '''

as principal admin password "admin" do
return y
***

'''.strip()]

if __name__ == '__main__':
    store = Store("admin")
    controller = Controller(store, None)
    interpreter = Interpreter(controller)
    for request in requests:
        print interpreter.accept(Lexer(request))

