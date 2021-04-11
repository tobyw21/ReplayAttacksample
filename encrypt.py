#!/usr/bin/python3

import random

# all ascii characters on keyboard
ascii_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()-=[];',./?><\":}{_+\| "

def keygen():
   s = sorted(ascii_chars, key=lambda k: random.random())
   return dict(zip(ascii_chars, s))

def encrypt(key, text):
   return ''.join(key[i] for i in text)

def decrypt(key, ctext):
   f = {k: j for j, k in key.items()}
   return ''.join(f[i] for i in ctext)

k = keygen()

print(encrypt(k, "Hello World!"))
print(decrypt(k, encrypt(k, "Hello World!")))
print(k)

