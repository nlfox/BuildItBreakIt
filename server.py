#!/usr/bin/python2

import socket
import sys
import signal
from parser import Lexer

class Server(object):
    def __init__(self, hostname, port):
        self.address = (hostname, port)
        self.run = True
        self.connection = None
        signal.signal(signal.SIGTERM, self.end)

    def start(self, interpreter):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind(self.address)
        except socket.error:
            sys.exit(63)
        self.sock.listen(1)
        while self.run:
            try:
                self.connection, client_address = self.sock.accept()
            except socket.error:
                self.end()
                return

            try:
                result = ""
                while True:
                    data = self.connection.recv(4096)
                    result = result + data
                    if "***" in data:
                        break
                self.connection.sendall(interpreter.accept(result.decode('string-escape')))
            finally:
                if self.connection:
                    self.connection.close()

    def end(self, signum=15, frame=None):
        self.run = False
        self.sock.close()
        sys.exit(0)
