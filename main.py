#!/usr/bin/python2

from store import Store
from parser import Parser
from server import Server
from interpreter import Interpreter

def __main__():
    hostname = "localhost"
    port = -1

    store = Store()
    parser = Parser()
    server = Server()
    interpreter = Interpreter()

    store.init()
    interpreter.init(store, server)
    parser.init(server)
    server.init(hostname, port)

