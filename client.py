#!/usr/bin/python3

import socket 
import select 
import sys
import manager
import json
import hashlib
import encrypt

on_hash = True

if len(sys.argv) != 3: 
    ip = input("IP: ")
    port = int(input("Port: "))
else:
    ip = sys.argv[1]
    port = int(sys.argv[2]) 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip, port))

username = input("> Username: ")
password = input("> Password: ")

if on_hash is True:
    md5_hash = hashlib.md5()
    md5_hash.update(password.encode('utf-8'))
    password = md5_hash.hexdigest()


c = {
    "action": "login",
    "username": username,
    "password": password
}

c = json.dumps(c)
server.send(c.encode())
auth_msg = server.recv(2048)

if auth_msg.decode() == "login_failed":
    server.close()
    exit(1)

else:
    print("> WELCOME!")
    while True: 
        try:
            message = input("> You: ")

            m = {
                "action": "msg",
                "content": message
            }

            m = json.dumps(m)
            server.send(m.encode()) 
            server_msg = server.recv(2048)

            print(f"> Server: {server_msg.decode()}")    
        except KeyboardInterrupt:
            o = {
                "action": "logout",
                "username": username
            }

            o = json.dumps(o)
            server.send(o.encode())
            print("\nKilling client process")
            break

server.close()
