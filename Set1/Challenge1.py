#!/usr/bin/env/python
import base64
import codecs

def main():
	str = input("[+] Enter hex string > ")
	str = codecs.decode(str,'hex_codec') # hex to string convert
	decoded = base64.b64encode(str) # encode string with base64 and convert to bytearray
	print("[+] Your Base64 encoded string is > "+decoded.decode())



if __name__=="__main__":
	main()

