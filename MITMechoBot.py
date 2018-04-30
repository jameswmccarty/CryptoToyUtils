#!/usr/bin/python

import HMAC_SHA1
import DiffieHellmanUtil as DH
import applyAES
import random

"""
Mimic an echo server that performs a DH key exchange, then sends a message from client-server-client using the shared key to encrypt.
"""

server_aeskey = None # server side secret
mitm_aeskey   = None # observer key

# return a public key to sender with sender
# accepts: Diffie Hellman modulus, and base
# accepts: client's public key
def init_server_keys(clientpub, dhmod=None, dhbase=None):
	global server_aeskey
	# create server key pair (same lenght as client)
	server_privkey, server_pubkey = DH.gen_key_pair(len(str(clientpub))*8,dhmod,dhbase)
	server_sessionkey = DH.session_key(clientpub,server_privkey,dhmod)
	# print "Generated server session key: " + str(hex(server_sessionkey))
	# AES Key is first 16 bytes of SHA1 of session key
	hv = HMAC_SHA1.SHA1(str(server_sessionkey)).state()
	server_aeskey = hv[0:16]
	# print "Server Session AES key is: " + str(server_aeskey)
	return server_pubkey

def randIV():
	iv = ""
	for i in xrange(16):
		iv += chr(random.randint(0,255))
	return iv

# decode message from client from session key
# re-encode with a new IV and return to client
def server_echo(packet):
	global server_aeskey
	# packet = AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
	iv = packet[-16:]
	packet = packet[:-16]

	msg = applyAES.decryptAES_CBC(packet,server_aeskey,iv)
	print "Server got msg: " + msg

	server_iv = randIV()
	server_msg = applyAES.encryptAES_CBC(msg,server_aeskey,server_iv)
	# send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
	return server_msg+server_iv

# an evil Man-in-the-Middle
# intercept and forward packets from client to server
# and vice versa
def mitm_init_server_keys(clientpub,dhmod=None, dhbase=None):
	global mitm_aeskey
	# send "p", "g", "p"
	temp = init_server_keys(dhmod,dhmod,dhbase) # won't keep server's key
	# key generated from this switch is (p**g) % p == 0
	# our MITM AES key will be the hash of Zeros
	hv = HMAC_SHA1.SHA1('0').state()
	mitm_aeskey = hv[0:16]
	# print "MITM Session Key: " + str(mitm_aeskey)
	return dhmod # return "p" to sender (so they generate the same key)
	
# an evil Man-in-the-Middle
# intercept and forward packets from client to server
# and vice versa
def mitm_server_echo(packet):
	# we can read the packet, then forward the contents
	iv = packet[-16:]
	print "Evil MITM got Client data: ",
	print applyAES.decryptAES_CBC(packet[:-16],mitm_aeskey,iv)
	reply = server_echo(packet) # forward packet
	iv = packet[-16:]
	print "Evil MITM got Server reply: ",
	print applyAES.decryptAES_CBC(packet[:-16],mitm_aeskey,iv)
	# pass reply back to client
	return reply


if __name__ == "__main__":

	clientmsg = "Cooking MCs like a pound of bacon."

	"""
	Normal server communication
	"""

	print ""
	print "Normal secure client-server comms:"
	print ""


	# client A generates a 1024-bit keypair
	client_a, client_A = DH.gen_key_pair(1024)
	# A->B a modulus "p", base "g", and public key "A"
	# B->A public key "B"
	server_B = init_server_keys(client_A,DH.NISTp,DH.NISTg)
	# "A" generates session key
	client_s = DH.session_key(server_B,client_a,DH.NISTp)
	# AES key is first 16 byes of SHA1 of session key
	client_aeskey = HMAC_SHA1.SHA1(str(client_s)).state()[0:16]
	# print "Client Session key: " + str(client_aeskey)

	# A sends encrypted message to server.
	# B echo's message back to A

	client_iv = randIV()
	client_packet = applyAES.encryptAES_CBC(clientmsg,client_aeskey,client_iv)
	client_packet += client_iv

	# send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
	reply = server_echo(client_packet)
	new_iv = reply[-16:]
	reply = reply[:-16]
	plain = applyAES.decryptAES_CBC(reply,client_aeskey,new_iv)
	print "Got from Server: " + plain

	"""
	Man in the Middle attack (with injection)
	"""

	print ""
	print "Demo Man-in-the-Middle with parameter injection:"
	print ""

	# client A generates a 1024-bit keypair
	client_a, client_A = DH.gen_key_pair(1024)
	# A->B a modulus "p", base "g", and public key "A"
	# B->A public key "B"
	server_B = mitm_init_server_keys(client_A,DH.NISTp,DH.NISTg)
	# "A" generates session key
	client_s = DH.session_key(server_B,client_a,DH.NISTp)
	# AES key is first 16 byes of SHA1 of session key
	client_aeskey = HMAC_SHA1.SHA1(str(client_s)).state()[0:16]
	# print "Client Session key: " + str(client_aeskey)

	# A sends encrypted message to server.
	# B echo's message back to A

	client_iv = randIV()
	client_packet = applyAES.encryptAES_CBC(clientmsg,client_aeskey,client_iv)
	client_packet += client_iv

	# send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
	reply = mitm_server_echo(client_packet)
	new_iv = reply[-16:]
	reply = reply[:-16]
	plain = applyAES.decryptAES_CBC(reply,client_aeskey,new_iv)
	print "Got from Server: " + plain
