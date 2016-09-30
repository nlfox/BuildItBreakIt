#!/usr/bin/python2

import sys
import re
from store import Store
from controller import Controller
from server import Server
from interpreter import Interpreter
from argparse import ArgumentParser


def main():
    argparser = ArgumentParser()
    argparser.add_argument("port", help="Port number to be used by the server", type=str)
    argparser.add_argument("password", help="Password to be used for the admin account", nargs="?", default="admin",
                           type=str)
    args = argparser.parse_args()

    if len(args.password) > 4096 or len(args.port) > 4096:
        sys.exit(255)
    if not args.port.isdigit() or args.port[0] == "0":
        sys.exit(255)
    if int(args.port) < 1024 or int(args.port) > 65535:
        sys.exit(255)

    pattern = re.compile("^[A-Za-z0-9_ ,;.?!-]*$")
    if not pattern.match(args.password):
        sys.exit(255)

    hostname = "localhost"
    port = int(args.port)

    if port < 1024 or port > 65535:
        sys.exit(0)

    store = Store(args.password)

    server = Server(hostname, port)
    controller = Controller(store, server)
    interpreter = Interpreter(controller)

    server.start(interpreter)


if __name__ == "__main__":
    main()
