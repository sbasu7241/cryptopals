#!/usr/bin/env/python
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint

unknown_string=bytes( "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"+"aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"+"dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"+"YnkK",encoding='utf8')

# List to do

# Create random key and assign to global variable
# Create such a function AES-128-ECB(your-string || unknown-string, random-key)
# Discover the block size of the cipher by feeding identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on

key = get_random_bytes(16)

# PKCS padding is added
def pkcs(data,block_size):
	"""Returns data padded to the supplied block size in PKCS#7 format"""
	
	pad_length = block_size - (len(data) % block_size)
	
	# if pad_length is 0 it means data is of correct size but we will add extra blocks of padding	
	if pad_length == 0:
		pad_length = block_size
	#print(pad_length)

	return  data+ (chr(pad_length) * pad_length).encode() #.encode() will convert string to byte representation




# Encrypt oracle for ECB is made
def encrypt_oracle(data):
		base64_decoded = bytes(base64.b64decode(unknown_string))
		plain_text = pkcs(data + base64_decoded,AES.block_size)
		return AES.new(key, AES.MODE_ECB).encrypt(plain_text)
		
		 
# Detect block_size
def get_block_size(data):
	ciphertext_length = len(encrypt_oracle(b''))
	i = 1
	while True:
		data = bytes("A" * i,encoding='utf8')
		new_ciphertext_length = len(encrypt_oracle(bytes(data)))
		block_size = new_ciphertext_length - ciphertext_length
		if block_size:
			return block_size
		i += 1

# Check ecb encryption
def confirm_encrypt_ECB(blocksize):
	key = get_random_bytes(blocksize)	
	plaintext = get_random_bytes(blocksize) * 2	
	ciphertext_b = encrypt_oracle(plaintext)
			
	if ciphertext_b[0:blocksize] != ciphertext_b[blocksize:blocksize*2]:
		raise Exception("The function encrypt_oracle is not using ECB")
	else:
		print ("[+] The function encrypt_oracle is using ECB")

# Get cipher length size
def get_unknown_string_size(data):
    ciphertext_length = len(encrypt_oracle(b''))
    i = 1
    while True:
        data = bytes("A" * i,encoding='utf8')
        new_ciphertext_length = len(encrypt_oracle(data))
        if ciphertext_length != new_ciphertext_length:
            return new_ciphertext_length - i
        i += 1

def get_unknown_string(data):
	
	unknown_string_size = get_unknown_string_size(data)
	unknown_string = b''
	unknown_string_size_rounded = ((unknown_string_size // block_size) + 1) * block_size	# Say 159
	for i in range(unknown_string_size_rounded - 1, 0, -1):			# Loop from i=159 to 0
		d1 = bytes("A" * i,encoding='utf8')				# d1 = 'AAAAAAAA...(i times)..AAA'
		c1 = encrypt_oracle(d1)[:unknown_string_size_rounded]		# c1 = encrypted('AAAAAAA...((159-i) times)...AAA' + 'Cipher_text[0:i]') 
		for c in range(256):
		    d2 = d1[:] + unknown_string + bytes(chr(c),encoding='utf8')			
		    c2 = encrypt_oracle(d2)[:unknown_string_size_rounded]
		    if c1 == c2:
		        unknown_string += bytes(chr(c),encoding='utf8')
		        break
	return unknown_string

if __name__ == '__main__':	
	
	block_size = get_block_size(bytes(unknown_string)) #block_size = 16	
	confirm_encrypt_ECB(AES.block_size)
	cipher_size = get_unknown_string_size(unknown_string)
	
	print('[+] Cipher text size is >> '+str(cipher_size))
	
	print('[+] Decoded text is >>\n'+str(get_unknown_string(unknown_string).decode()))


	
	
	
	
