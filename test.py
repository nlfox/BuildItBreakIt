#!/usr/bin/python

from store import Store
from controller import Controller
from interpreter import Interpreter
from parser import Lexer

requests = ['''

as principal admin password "admin" do
   create principal bob "B0BPWxxd"
   set x = []
   append to x with "test"
   append to x with "test1"
   append to x with "test2"
   append to x with { a = "x", b = "y", c = x }
   append to x with x
   set delegation x admin read -> bob
   return x
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
        print interpreter.accept(Lexer(request))

