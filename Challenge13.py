#!/usr/bin/env/python

import base64
import re
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
	
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)

def pkcs(data,block_size):
	"""Returns data padded to the supplied block size in PKCS#7 format"""
	
	pad_length = block_size - (len(data) % block_size)
	
	# if pad_length is 0 it means data is of correct size but we will add extra blocks of padding	
	if pad_length == 0:
		pad_length = block_size
	#print(pad_length)

	return  bytes(data,encoding = 'utf8')+ (chr(pad_length) * pad_length).encode() #.encode() will convert string to byte representation

def profile_for(email):
	email = email.replace('&','').replace('=','')
	profile = {
		'email': email,
		'uid': 10,
		'role': 'user'
	}
	query_str = 'email={0}&uid={1}&role={2}'.format(profile['email'], profile['uid'], profile['role'])
	query_str = pkcs(query_str,16)
	#print(query_str)
	return cipher.encrypt(query_str)	

def tamper_data(cipher_text,fake_data):
	if(len(fake_data)%16!=0):
		fake_data = pkcs(fake_data,16)
	return  cipher_text[:-16] + cipher.encrypt(fake_data)



ft = profile_for("fake@mail.com")

new_ct = tamper_data(ft,'admin')

print("[+] Original data >> "+"email=fake@mail.com&uid=10&role=user\n")

print("[+] Tampered data >> "+cipher.decrypt(new_ct)[:16-len('admin')].decode())

# Decrypt new_ct to get admin role to fake@mail.com


