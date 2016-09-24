#!/usr/bin/python2

from store import Store
from parser import Parser
from server import Server
from interpreter import Interpreter

def main():
    hostname = "localhost"
    port = -1

    store = Store()
    server = Server(hostname, port)
    parser = Parser(server)
    interpreter = Interpreter(store, server)

if __name__ == "__main__":
    main()
