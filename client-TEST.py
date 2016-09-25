#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = '' # Get local machine name
port = 12345               # Reserve a port for your service.

s.connect((host,port))
s.send(
"""as principal admin password "admin" do
local s = "abc"
return s
***
""")
print s.recv(1024)
s.close