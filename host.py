import os
import time
import socket
import sys

s = socket.socket()
host = "docxy"
port = 1234


while True:
    try:
        print(s.connect((host, port)))
        print("")
        print("Connected to Server")

        command = s.recv(1024)

        command = command.decode()

        if command == "shutdown" or command == "shut down":
            print("shutting down")
            os.system("Assets\shutdown.bat")
            break
    except:
        "Error Not Server"
