#!/usr/bin/env/python



def main():
	str1 = bytes.fromhex(input("[+] Enter String1 > "))
	str2 = bytes.fromhex(input("[+] Enter String2 > "))
	encoded = "".join(hex(a ^ b)[2:] for (a,b) in zip(str1,str2))
	print("[-] XOred output > "+encoded)
	
	encode = [a^b for (a,b) in zip(str1,str2)]
	encoded = ''.join(chr(i) for i in encode)
	print("[-] Decoded String > "+ encoded)

if __name__=="__main__":
	main()
