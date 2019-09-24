#!/usr/bin/env/python



def repeating_key_xor(message_bytes,key):
	"""Return's message xored with a key. If the message, is longer then the key will repeat"""

	output_bytes=b''
	index = 0
	for byte in message_bytes:
		output_bytes += bytes([byte^key[index]])
		if (index+1) == len(key):
			index = 0
		else:
			index += 1
		
	return output_bytes


def main():
	message = ["Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"]
	key = b"ICE"
	cipher_text=[]
	cipher_text.append(repeating_key_xor(message[0].encode(),key))
	#cipher_text.append(repeating_key_xor(message[1].encode(),key))

	print("Repeating key XOR encoded >> "+cipher_text[0].hex())	#Convert from byte array to hex
	#print(cipher_text[1].hex())


if __name__=="__main__":
	main()


