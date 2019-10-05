#!/usr/bin/env/python3


def unpad_pkcs(padded_data,block_size=16):
	if len(padded_data) % block_size != 0:
		raise PaddingError
	else:
		last_byte = padded_data[-1]
		padding_size = int(last_byte)
		padding = padded_data[-padding_size:]
		test_byte = bytes([padding_size]) * padding_size
		if padding == test_byte:		
			print(padded_data[:-padding_size])
		else:
			raise PaddingError


unpad_pkcs(b'ICE ICE BABY\x04\x04\x04\x04')

	
