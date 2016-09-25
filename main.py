#!/usr/bin/python2

from store import Store
from controller import Controller
from server import Server
from interpreter import Interpreter
from argparse import ArgumentParser

def main():
    argparser = ArgumentParser()
    argparser.add_argument("port", help="Port number to be used by the server", type=int)
    argparser.add_argument("password", help="Password to be used for the admin account", nargs="?", default="admin", type=str)
    args = argparser.parse_args()

    hostname = "localhost"
    port = args.port

    store = Store(args.password)

    server = Server(hostname, port)
    controller = Controller(store, server)
    interpreter = Interpreter(controller)

    server.start(interpreter)

if __name__ == "__main__":
    main()
