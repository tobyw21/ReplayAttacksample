#!/usr/bin/env python3

import socket
import manager
import sys
import os
from struct import *
import json

captured = []

if __name__ == "__main__":

    while True:
        cmd = input("Select Mode:\n s:\tsniffing mode\n c:\tcommand mode\n q:\tquit\n>>> ")

        if cmd == "s":
            print(f"{manager.__OKGREEN}[+]{manager.__ENDC}Sniffing Mode activating")
            sniff = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

            # idea from https://stackoverflow.com/questions/49517459/python-how-to-get-http-header-using-raw-sockets
            # and https://www.binarytides.com/python-packet-sniffer-code-linux/
            while True:
                try:
                    packet = sniff.recvfrom(65565)
                    
                    #packet string from tuple
                    packet = packet[0]
                    
                    #take first 20 characters for the ip header
                    ip_header = packet[0:20]
                    
                    #now unpack them :)
                    iph = unpack('!BBHHHBBH4s4s' , ip_header)
                    
                    version_ihl = iph[0]
                    version = version_ihl >> 4
                    ihl = version_ihl & 0xF
                    
                    iph_length = ihl * 4
                    
                            
                    tcp_header = packet[iph_length:iph_length+20]
                    
                    #now unpack them :)
                    tcph = unpack('!HHLLBBHHH' , tcp_header)
                    
                    source_port = tcph[0]
                    dest_port = tcph[1]
                    sequence = tcph[2]
                    acknowledgement = tcph[3]
                    doff_reserved = tcph[4]
                    tcph_length = doff_reserved >> 4
                    
                    h_size = iph_length + tcph_length * 4
                    data_size = len(packet) - h_size
                    
                    #get data from the packet
                    data = packet[h_size:]
                    
                    if not data:
                        continue

                    print('Data :\t' + str(data) + "\n\n")

                except KeyboardInterrupt:
                    print("\nQuitting sniffing mode")
                    sniff.close()
                    break

        elif cmd == "c":
            print(f"{manager.__OKGREEN}[+]{manager.__ENDC}Command Mode activating")
            
            try:
                while True:
                
                    print("Enter your payload\nIt will be transffered into dictionary and send to server")
                    username = input("USERNAME: ")
                    print(f"{manager.__WARNING}WARNING{manager.__ENDC}: Password will be a hash")
                    passsword = input("PASSWORD: ")

                    payload = {
                        "username": username,
                        "password": passsword,
                        "action": "login"
                    }

                    print("Building Connection...")
                    send_pl = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #, socket.IPPROTO_TCP
                    ip = input("Enter target  IP: ")
                    port = int(input("Enter target port: "))
                    send_pl.connect((ip, port))

                    payload = json.dumps(payload)
                    send_pl.send(payload.encode())
                    auth_msg = send_pl.recv(2048)

                    if auth_msg.decode() == "login_allow":
                        try:
                            while True:

                                message = input("attclient disguised You: ")

                                m = {
                                    "action": "msg",
                                    "content": message
                                }

                                m = json.dumps(m)
                                send_pl.send(m.encode()) 
                                server_msg = send_pl.recv(2048)

                                print(f"attclient target Server: {server_msg.decode()}")
                        except KeyboardInterrupt:
                            o = {
                                "action": "logout",
                                "username": username
                            }

                            o = json.dumps(o)
                            send_pl.send(o.encode())
                            print("\nattclient logged out")
                            send_pl.close()
                            break
            
            except KeyboardInterrupt:
                print("\nQuitting Command mode")
                break
            
        
        else:
            break

    print("Quitting attclient")



