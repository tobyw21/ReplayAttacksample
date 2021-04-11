#!/usr/bin/python3 
import hashlib

# just user global var as credential for convience
USER = "admin"
PSWD = "admin"

on_hash = True

__HEADER = '\033[95m'
__OKBLUE = '\033[94m'
__OKCYAN = '\033[96m'
__OKGREEN = '\033[92m'
__WARNING = '\033[93m'
__FAIL = '\033[91m'
__ENDC = '\033[0m'
__BOLD = '\033[1m'
__UNDERLINE = '\033[4m'


class User:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, action):
        u = USER
        p = PSWD

        if on_hash is True:
            md5_hash = hashlib.md5()
            md5_hash.update(p.encode('utf-8'))
            p = md5_hash.hexdigest()


        if action == "login" and self.username == u and self.password == p:
            status = "login_allow"
            return status
        else:
            status = "login_failed"
            return status


    def logout(self, action):
        if action == "logout":
            status = "logged_out"
            return status

