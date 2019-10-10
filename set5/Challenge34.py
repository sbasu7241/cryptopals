#!/usr/bin/env/python
from random import randint
from Crypto import Random
from Crypto.Cipher import AES
from binascii import unhexlify
import hashlib
from Crypto import Random

class DiffieHellman():
	"""Implements the Diffie-Helman key exchange. Each class is a party, which has his secret key (usually
	referred to as lowercase a or b) shares the public key (usually referred to as uppercase A or B) and can
	compute the shared secret key between itself and another party, given their public key, assuming that
	they are agreeing on the same p and g.
	"""

	DEFAULT_G = 2
	DEFAULT_P = int('ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b225'
                    '14a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f4'
                    '4c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc20'
                    '07cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed5'
                    '29077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff', 16)

	def __init__(self, g=DEFAULT_G, p=DEFAULT_P):
		self.g = g
		self.p = p
		self._secret_key = randint(0, p - 1)
		self.shared_key = None

	def get_public_key(self):
		return pow(self.g, self._secret_key, self.p)

	def get_shared_secret_key(self, other_party_public_key):
		if self.shared_key is None:
			self.shared_key = pow(other_party_public_key, self._secret_key, self.p)
		return self.shared_key

def parameter_injection_attack(alice,bob):
	"""Simulates a MITM key-fixing attack on Diffie-Hellman with parameter injection."""
	
	# Step 1: Alice computes A and sends it to the MITM (thinking of Bob)

	A = alice.get_public_key()

	# Step 2: the MITM changes A with p and sends it to Bob
	
	A = alice.p
	
	# Step 3: Bob computes B and sends it to the MITM (thinking of Alice)

	B = bob.get_public_key()
	
	# Step 4: the MITM changes B with p and sends it to Alice

	B = bob.p

	# Step 5: Alice finally sends her encrypted message to Bob (without knowledge of MITM)
	
	_msg = b'Hello, how are you?abcdefpjhtyio'
	_a_key = unhexlify(hashlib.sha1(str(bob.get_shared_secret_key(A)).encode()).hexdigest()[:16])
	_a_iv = Random.new().read(16)
	print(len(_a_key))
	cipher = AES.new(_a_key, AES.MODE_CBC, _a_iv)
	a_question = cipher.encrypt(_msg) + _a_iv

	# Step 6: the MITM relays that to Bob

	# Step 7: Bob decrypts the message sent by Alice (without knowing of the attack), encrypts it and sends it again

	_b_key = unhexlify(sha1(str(bob.get_shared_secret_key(A)).encode()))[:16]
	_a_iv = a_question[-16:]
	cipher = AES.new(_b_key, AES.MODE_CBC, _a_iv)
	_a_message = cipher.decrypt(a_question[:-16])
	print(_a_message)
	_b_iv = Random.new().read(AES.block_size)
	cipher = AES.new(_b_key, AES.MODE_CBC, _b_iv)
	_b_answer = cipher.encrypt(_a_message)+ _b_iv
	print(_b_answer)	
	
	# Step 8: the MITM relays that to Alice	
	
	# Step 9: the MITM decrypts the message (either from a_question or from b_answer, it's the same).
	#
	# Finding the key after replacing A and B with p is, in fact, very easy.
	# Instead of (B^a % p) or (A^b % p), the shared secret key of the exercise became (p^a % p)
	# and (p^b % p), both equal to zero!
	

	# Hack Alice's question
	mitm_hacked_key = unhexlify(sha1(b'0').encode())[:16]
	mitm_a_iv = a_question[-AES.block_size:]
	cipher = AES.new(mitm_hacked_key,AES.MODE_CBC,mitm_a_iv)
	mitm_hacked_message_a = cipher.decrypt(a_question[:-AES.block_size])
	
	# Hack Bob's answer (which here is the same)
	mitm_b_iv = b_answer[-AES.block_size:]
	cipher = AES.new(mitm_hacked_key,AES.MODE_CBC,mitm_b_iv)
	mitm_hacked_message_b = cipher.sdecrypt(b_answer[:-AES.block_size])

    	# Check if the attack worked
	assert _msg == mitm_hacked_message_a == mitm_hacked_message_b	



def main():
	alice = DiffieHellman()
	bob = DiffieHellman()
	parameter_injection_attack(alice, bob)

if __name__ == '__main__':
	main()



