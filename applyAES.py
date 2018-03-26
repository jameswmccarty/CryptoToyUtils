#!/usr/bin/python

#depends pyopenssl
from Crypto.Cipher import AES
from struct import pack
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
	decoder = pkcs7.PKCS7Encoder()
	plain = decoder.decode(plain)
	return plain

def encryptAES_ECB(stream, key):
	encoder = pkcs7.PKCS7Encoder()
	stream = encoder.encode(stream)
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
	decoder = pkcs7.PKCS7Encoder()
	plain = decoder.decode(plain)
	return plain

def encryptAES_CBC(stream, key, iv):
	encoder = pkcs7.PKCS7Encoder()
	stream = encoder.encode(stream)
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

def encryptAES_CTR(pt, key, nonce):
	ct = b''
	ks = b''
	nonce = bytearray(nonce)
	counter = 0
	while True:
		count = bytearray(pack('l', counter))
		ks = encryptAES_ECB_blk(str(nonce+count), key)
		counter += 1
		for byte in ks:
			if len(pt) > 0:
				ct += chr(ord(byte) ^ ord(pt[0]))
				pt = pt[1:]
			else:
				return ct

def decryptAES_CTR(ct, key, nonce):
	return encryptAES_CTR(ct, key, nonce)

if __name__ == "__main__":

	aes_key = "FOO BAR FIZZBUZZ"	
	iv = chr(0) * 16
	nonce = chr(0) * 8

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

	#Test for CTR Mode
	infile = open("tests/trial_text.txt", "r")
	intext = infile.read()
	infile.close()

	cipher = encryptAES_CTR(intext, aes_key, nonce)
	print "Encrypted with CTR Mode."
	print base64.b64encode(cipher)
	plain = decryptAES_CTR(cipher, aes_key, nonce)
	print plain
	#End of CTR Mode Test
