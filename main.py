#!/usr/bin/python2

import sys
import re
from store import Store
from controller import Controller
from server import Server
from interpreter import Interpreter
from argparse import ArgumentParser


def main():

    args = sys.argv
    print args
    if len(args) < 2 or len(args) > 3:
        sys.exit(1)

    arg_port = sys.argv[1]
    if len(arg_port) > 4096:
        sys.exit(255)
    if not arg_port.isdigit() or arg_port[0] == "0":
        sys.exit(255)

    password = "admin"
    if len(args) == 3:
        password = sys.argv[2]
        if len(password) > 4096:
            sys.exit(255)
        pattern = re.compile("^[A-Za-z0-9_ ,;.?!-]*$")
        if not pattern.match(password):
            sys.exit(255)

    hostname = "localhost"
    port = int(arg_port)

    if port < 1024 or port > 65535:
        sys.exit(255)

    store = Store(password)

    server = Server(hostname, port)
    controller = Controller(store, server)
    interpreter = Interpreter(controller)

    server.start(interpreter)


if __name__ == "__main__":
    main()
