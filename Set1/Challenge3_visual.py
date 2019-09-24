#!/usr/bin/env/python

import string
result = string.ascii_letters + string.digits 
#print(result)

def single_char_xor(input_bytes,ch):
	output_bytes = b''
	for byte in input_bytes:
		output_bytes += bytes([byte^ch])
	return output_bytes

def main():

	hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
	str1 = bytes.fromhex(hex_string) #Byte array of hex string

	for r in result:
		print("Xored with "+r+" >> "+single_char_xor(str1,ord(r)).decode())

if __name__=="main":
	main()


