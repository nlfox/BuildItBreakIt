#!/usr/bin/python

from store import Store
from controller import Controller
from interpreter import Interpreter
from parser import Lexer

requests = ['''

as principal admin password "admin" do
   create principal bob "B0BPWxxd"
   set x = [] //test comment
   append to x with "Hello "
   set y = x
   append to y with "World!"
   set delegation x admin read -> bob
return x
***

'''.strip()]

if __name__ == '__main__':
    store = Store("admin")
    controller = Controller(store, None)
    interpreter = Interpreter(controller)
    for request in requests:
        print interpreter.accept(request)

