import os
import time
import socket
import sys

s = socket.socket()
host = "192.168.1.95"
port = 1234
s.connect((host, port))
print("")
print("Connected to Server")

command = s.recv(1024)

command = command.decode()

if command == 'shutdown' or command == 'shut down':
    print("shutting down")
