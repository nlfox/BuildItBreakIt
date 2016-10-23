#!/usr/bin/python

from store import Store
from controller import Controller
from interpreter import Interpreter
from parser import Lexer

requests = ['''

as principal admin password "admin" do
    set records = []
    append to records with { name = "mike", date = "1-1-90" }
    append to records with { name = "dave", date = "1-1-85" }
    local names = records
    foreach rec in names replacewith rec.name
return names
***

'''.strip()]

if __name__ == '__main__':
    store = Store("admin")
    controller = Controller(store, None)
    interpreter = Interpreter(controller)
    for request in requests:
        print interpreter.accept(request)

