#!/usr/bin/python

import socket
host = ''
port = 12345

testfile = open("tests.txt", "r")
request = ""
for line in testfile:
    request += line

s = socket.socket()
s.connect((host,port))
s.send(request)
print s.recv(1024)
s.close