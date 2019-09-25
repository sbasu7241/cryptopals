#!/usr/bin/env/python

def pkcs(data,block_size):
	"""Returns data padded to the supplied block size in PKCS#7 format"""
	
	pad_length = block_size - (len(data) % block_size)
	
	# if pad_length is 0 it means data is of correct size but we will add extra blocks of padding	
	if pad_length == 0:
		pad_length = block_size
	#print(pad_length)

	return  data+ (chr(pad_length) * pad_length).encode() #.encode() will convert string to byte representation


	
print("[+] PKCS#7 padded byte_array >> "+str(pkcs(b'YELLOW SUBMARINE',20)))
