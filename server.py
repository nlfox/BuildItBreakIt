#!/usr/bin/python2

import socket
from parser import Lexer

class Server(object):
    def __init__(self, hostname, port):
        self.address = (hostname, port)
        self.run = True

    def start(self, interpreter):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.address)
        self.sock.listen(1)
        while self.run:
            self.connection, client_address = self.sock.accept()    
            try:
                result = ""
                while True:
                    data = self.connection.recv(4096)
                    result = result + data
                    if "***" in data:
                        break
                self.connection.sendall(interpreter.accept(result.decode('string-escape')))
            finally:
                self.connection.close()
