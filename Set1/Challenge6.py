#!/usr/bin/env/python
import base64
import string
cipheredtext = ''
str1 = "this is a test".encode()
str2 = "wokka wokka!!!".encode()


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
	for r in string.printable:
		#print(r)
		score = get_english_score(single_char_xor(input_bytes,ord(r)))
		if score > max_score:
			max_score = score		
			actual_key = ord(r)
	return actual_key
		
def single_char_xor(input_bytes,ch):
	"""Returns the result of each byte being XOR'd with a single value.
    	"""	
	output_bytes = b''
	for byte in input_bytes:
		output_bytes += bytes([byte^ch])
	return output_bytes

def hamming_distance(chaine1, chaine2):
	xored_bytes = [b1^b2 for b1,b2 in zip(chaine1,chaine2)]
	hamming_distance = 0
	for byte in xored_bytes:
		hamming_distance += sum([1 for bi in bin(byte) if bi=='1'])
	return hamming_distance	


def repeating_key_xor(message_bytes, key):
    """Returns message XOR'd with a key. If the message, is longer
    than the key, the key will repeat.
    """
    output_bytes = b''
    index = 0
    for byte in message_bytes:
        output_bytes += bytes([byte ^ key[index]])
        if (index + 1) == len(key):
            index = 0
        else:
            index += 1
    return output_bytes


with open('chall_6_input.txt','r') as input_file:
	cipheredtext = base64.b64decode(input_file.read())

average_distances = []
# Take the keysize from suggested range
for key_size in range(2,41):
	
	distances = []
	chunks = [cipheredtext[i:i+key_size] for i in range(0,len(cipheredtext),key_size)]
	# Like if keysize be 2 and cipher be "hello" chunks will be ['he','ll','o']
	
	while True:
		try:
			#Take two chunks at the list beginning and get hamming distance
			chunk_1 = chunks[0]
			chunk_2 = chunks[1]
			
			#Normalize result by dividing it with keysize			
			distance = hamming_distance(chunk_1,chunk_2)
			
			#Remove these chunks so that hamming distance for next two can be calculated and normalize distances
			distances.append(distance/key_size)
			
			#Remove these chunks when the loop starts over so that hamming for next two chunks may be calculated
			del chunks[0]
			del chunks[1]

		# When an exception occurs ie all chunks have been processed break out of the loop
		except Exception as e:
			break

	
	result = {
    		'key': key_size,
    		'avg distance': sum(distances) / len(distances)
    		 }
	average_distances.append(result)
	
possible_key_lengths = sorted(average_distances,key=lambda x:x['avg distance'])[0]
estimated_size = possible_key_lengths['key']
print("Estimated key size >> "+str(possible_key_lengths['key']))

"""Here’s a great explanation of why guessing the right key size shortens the Hamming Distance. There are two reasons:

    If you XOR a thing with itself, the result is zero. So if you guess the correct block size, XORing the ciphertext sized to this block length means that the key “drops out” of the Hamming calculation, reducing the Hamming distance. If you guess the wrong block size, then the two blocks you compare each have a different key.

    Intelligible English text exhibits more uniformity than randomly chosen bits. If we guess the block size correctly, it’ll fall within the ASCII values for A-Za-z0-9 instead of being anywhere between 0 and 255."""

# Now let us break the cipher text into blocks of the estimated key_size
chunks = [cipheredtext[i:i+estimated_size] for i in range(0,len(cipheredtext),estimated_size)]
key = b''

# Will populate with a single character as each transposed 
# block has been single-byte XOR brute forced

for i in range(estimated_size):
	
	# Creates an block made up of each nth byte, where n
        # is the keysize
	block = b''
	for j in range(i, len(cipheredtext), estimated_size):
            block += bytes([cipheredtext[j]])
	key += bytes([brute_single_char_xor(block)])
print("\nKey is >> "+key.decode())

plain_text = repeating_key_xor(cipheredtext, key)
print("\nDecrypted text >> "+plain_text.decode())













	
		

	

	


