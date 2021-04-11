#!/usr/bin/python3

import socket 
import sys 
from threading import *
import manager
import time
import os
import json
import encrypt

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

if len(sys.argv) != 3: 
    print (f"{manager.__FAIL}Usage: python3 {sys.argv[0]} <IP addr> <Port number>{manager.__ENDC}")
    exit(1) 
  

ip = str(sys.argv[1]) 

port = int(sys.argv[2]) 
  

server.bind((ip, port)) 
  

server.listen(1) 

print(f"{manager.__OKGREEN}[+]{manager.__ENDC} Server is up at {ip}:{port}")

active_users = []

def clientthread(conn, addr): 
  
    while True: 
            try: 
                cmessage = conn.recv(2048)

                cmessage = cmessage.decode()
                if not cmessage:
                    continue

                cmessage = json.loads(cmessage)
                
                if cmessage["action"] == "login":
                    
                    u = manager.User(cmessage["username"], cmessage["password"])
                    s = u.login(cmessage["action"])

                    if s == "login_allow" and cmessage["username"] not in active_users:
                        print (f"{manager.__OKCYAN}{addr[0]} connected{manager.__ENDC}")
                        active_users.append(cmessage["username"])
                    elif s == "login_allow" and cmessage["username"] in active_users:
                        s = "login_failed"
                        conn.send(s.encode())
                        sys.exit(1)

                    elif s == "login_failed":
                        conn.send(s.encode())
                        sys.exit(1)

                    conn.send(s.encode())


                elif cmessage["action"] == "logout":
                    print (f"{manager.__FAIL}{addr[0]} disconnect{manager.__ENDC}")
                    active_users.remove(cmessage["username"])
                    sys.exit(0)
                    
                else:
                    mc = cmessage["content"]
                    print (f"> Client ({addr[0]}): {mc}")
                    smessage = input("> You: ")

                    conn.send(smessage.encode())

            except KeyboardInterrupt: 
                sys.exit(0)
  
while True: 
    
    try:
        conn, addr = server.accept() 
    
        
        th1 = Thread(target=clientthread, args=(conn,addr), name="cthread", daemon=True)
        th1.start()
    except KeyboardInterrupt:
        print(f"\n{manager.__FAIL}[-]{manager.__ENDC} Server is closed")
        break
    
conn.close() 
server.close() 
  
            
