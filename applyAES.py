#!/usr/bin/python

#depends pyopenssl
from Crypto.Cipher import AES
import base64
import applyXOR as xorlib
import pkcs7

def decryptAES_ECB_blk(block, key):
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.decrypt(block)

def encryptAES_ECB_blk(block, key):
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(block)

def decryptAES_ECB(stream, key):
	plain = ""
	while stream != "":
		block  = stream[0:len(key)]
		stream = stream[len(key):]
		plain += decryptAES_ECB_blk(block, key)
	plain = pkcs7.clearPad(plain, 16)
	return plain

def encryptAES_ECB(stream, key):
	stream = pkcs7.padInput(stream, 16)	
	cipher = ""
	while stream != "":
		block  = stream[0:len(key)]
		stream = stream[len(key):]
		cipher += encryptAES_ECB_blk(block, key)
	return cipher

def decryptAES_CBC(stream, key, iv):
	cipherblk = iv
	plain = ""
	while stream != "":
		block =  stream[0:len(key)]
		stream = stream[len(key):]
		out   = decryptAES_ECB_blk(block, key)
		out   = xorlib.rawXORpad(out, cipherblk)
		cipherblk = block
		plain += out
	plain = pkcs7.clearPad(plain, 16)
	return plain

def encryptAES_CBC(stream, key, iv):
	stream = pkcs7.padInput(stream, 16)	
	cipherblk = iv
	ciphertxt = ""
	while stream != "":
		block  = stream[0:len(key)]
		stream = stream[len(key):]
		inpt   = xorlib.rawXORpad(block, cipherblk)
		inpt   = encryptAES_ECB_blk(inpt, key)
		cipherblk = inpt
		ciphertxt += inpt
	return ciphertxt

if __name__ == "__main__":

	aes_key = "FOO BAR FIZZBUZZ"	
	iv = chr(0) * 16

	#Test for ECB Mode 
	infile = open("tests/trial_text.txt", "r")
	intext = infile.read()
	infile.close()
	
	cipher = encryptAES_ECB(intext, aes_key)
	print "Encrypted with ECB Mode."
	print base64.b64encode(cipher)
	plain = decryptAES_ECB(cipher, aes_key)
	print plain
	#End of ECB Mode Test

	
	#Test for CBC Mode
	infile = open("tests/trial_text.txt", "r")
	intext = infile.read()
	infile.close()

	cipher = encryptAES_CBC(intext, aes_key, iv)
	print "Encrypted with CBC Mode."
	print base64.b64encode(cipher)
	plain = decryptAES_CBC(cipher, aes_key, iv)
	print plain
	#End of CBC Mode Test


