#!/usr/bin/python

from store import Store
from controller import Controller
from interpreter import Interpreter
from parser import Lexer

requests = ['''

as principal admin password "admin" do
   create principal bob "B0BPWxxd"
   set x = "my string" //test comment
   set y = {f1 = x, f2 = "field2" }
   set delegation x admin read -> bob
return y.f2
***

'''.strip(), '''

as principal bob password "B0BPWxxd" do
    return x
***

'''.strip()]

if __name__ == '__main__':
    store = Store("admin")
    controller = Controller(store, None)
    interpreter = Interpreter(controller)
    for request in requests:
        print interpreter.accept(request)

