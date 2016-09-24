#!/usr/bin/python2

import socket

class Server(object):
    def __init__(self, hostname, port):
        self.address = (hostname, port)

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.address)
        sock.listen(1)
        while True:
            connection, client_address = self.sock.accept()

