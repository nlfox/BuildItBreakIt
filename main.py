#!/usr/bin/python2

from store import Store
from controller import Controller
from server import Server
from interpreter import Interpreter

def main():
    hostname = "localhost"
    port = -1

    store = Store()
    server = Server(hostname, port)
    controller = Controller(store, server)
    interpreter = Interpreter(controller)

    server.start(interpreter)

if __name__ == "__main__":
    main()
