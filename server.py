#!/usr/bin/python2

import socket
from parser import Lexer

class Server(object):
    def __init__(self, interpreter, hostname, port):
        self.interpreter = interpreter
        self.address = (hostname, port)

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.address)
        sock.listen(1)
        while True:
            self.connection, client_address = self.sock.accept()    
            try:
                result = ""
                while True:
                    data = self.connection.recv(4096)
                    result = result + data
                    if "***" in data:
                        break
                self.connection.sendall(self.interpreter.accept(Lexer(result)))
            finally:
                self.connection.close()
