#!/usr/bin/env/python

import string
result = string.ascii_letters + string.digits 
#print(result)

def get_english_score(input_bytes):	
	"""Compares each input byte to a character frequency 
	chart and returns the score of a message based on the
	relative frequency the characters occur in the English
	language"""
	
	englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07,' ':13.00}
	
	return sum([englishLetterFreq.get(chr(byte), 0) for byte in input_bytes.upper()])
	
	
def brute_single_char_xor(input_bytes):
	max_score = 0;
	actual_string = b''
	for r in result:
		score = get_english_score(single_char_xor(input_bytes,ord(r)))
		if score > max_score:
			max_score = score		
			actual_string = single_char_xor(input_bytes,ord(r))
	return actual_string
		
		

def single_char_xor(input_bytes,ch):
	"""Returns the result of each byte being XOR'd with a single value.
    	"""	
	output_bytes = b''
	for byte in input_bytes:
		output_bytes += bytes([byte^ch])
	return output_bytes

def main():

	#hex_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
	ciphers = open('input_data.txt').read().splitlines()
	potential_plaintext = []
	for hexstring in ciphers:
		ciphertext = bytes.fromhex(hexstring)
		potential_plaintext.append(brute_single_char_xor(ciphertext))	
	best_score = sorted(potential_plaintext, key=lambda x: get_english_score(x), reverse=True)	
	print("Actual Xored String >> "+best_score[0].decode())
				
	
if __name__=="__main__":
	main()


