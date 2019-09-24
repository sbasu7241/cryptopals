#!/usr/bin/env/python

from Crypto.Cipher import AES
import base64
cipher_text=b''


with open('chall_7_input.txt','r') as fi:
	cipher_text = base64.b64decode(fi.read())

key = b'YELLOW SUBMARINE'

cipher = AES.new(key, AES.MODE_ECB)

plain_text = cipher.decrypt(cipher_text)

print("Plain Text >> "+plain_text.decode())

