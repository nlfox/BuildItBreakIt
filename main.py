#!/usr/bin/python2

from store import Store
from parser import Parser
from server import Server
from interpreter import Interpreter

def main():
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

if __name__ == "__main__":
    main()
