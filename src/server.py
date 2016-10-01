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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        signal.signal(signal.SIGTERM, self.end)

    def start(self, interpreter):
        try:
            self.sock.bind(self.address)
        except socket.error:
            sys.exit(63)
        self.sock.listen(1)
        while self.run:
            # Initiate connection
            self.sock.settimeout(None)
            try:
                self.connection, client_address = self.sock.accept()
            except socket.error:
                continue

            # Accept data
            self.sock.settimeout(30.0)
            try:
                result = ""
                while True:
                    data = self.connection.recv(4096)
                    result += data
                    if "***" in data:
                        break
            except socket.timeout:
                self.connection.sendall('{"status":"TIMEOUT"}')
                self.connection.close()
                continue

            # Execute commands
            try:
                self.connection.sendall(interpreter.accept(result.decode("string-escape")))
            except:
                self.end()
            finally:
                if self.connection:
                    self.connection.close()

    def end(self, signum=15, frame=None):
        self.run = False
        if self.sock:
            self.sock.close()
        sys.exit(0)
