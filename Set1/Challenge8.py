#!/usr/bin/env/python

import base64

def count_repetitions(cipher_text,block_size):
	""""Breaks the ciphertext into block_size sized chunks and counts the no of repetitions.Returns the ciphertext and repetitions as a dictionary"""
	chunks = []

	for i in range(0,len(cipher_text),block_size):
		chunks.append(cipher_text[i:i+block_size])
		
	number_of_repetitions = len(chunks) - len(set(chunks))

	result = {
		'ciphertext':cipher_text,
		'repetitions':number_of_repetitions	
	}
	return result


def main():
	ciphertext = []
	with open('chall_8_input.txt','r') as fil:
		for line in fil.readlines():
			ciphertext.append(bytes.fromhex(line.strip()))

	block_size = 16
	#for cipher in ciphertext:
	#	print(cipher)
	repetitions = [count_repetitions(cipher,block_size) for cipher in ciphertext]
	
	most_repeat = sorted(repetitions,key=lambda x: x['repetitions'],reverse=True)[0]
	print("[+] Cipher text >> "+str(most_repeat['ciphertext']))
	print("[+] No of repeating blocks >> "+str(most_repeat['repetitions']))	
	
	
		
		

		

		

if __name__=="__main__":
	main()

