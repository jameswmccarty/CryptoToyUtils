#/usr/bin/python

# A pure Python implementation of the SHA-1 algorithm
# Code adapted from Wikipedia https://en.wikipedia.org/wiki/SHA-1

# Not for use in production code :-)

from struct import pack
from struct import unpack

class SHA1:

	# Initial values
	h0 = 0x67452301
	h1 = 0xEFCDAB89
	h2 = 0x98BADCFE
	h3 = 0x10325476
	h4 = 0xC3D2E1F0

	ml = None # Length of message in bits
	msg = None # Padded message

	def __init__(self, m, a=None, b=None, c=None, d=None, e=None, length=None):
		# allow internal state to be set
		if a != None:
			self.h0 = a & 0xFFFFFFFF
		if b != None:
			self.h1 = b & 0xFFFFFFFF
		if c != None:
			self.h2 = c & 0xFFFFFFFF
		if d != None:
			self.h3 = d & 0xFFFFFFFF
		if e != None:
			self.h4 = e	& 0xFFFFFFFF	
		# get the message length in bits
		if length == None:
			self.ml = len(m) * 8
		else: # override for length extension attacks
			self.ml = length
		# append the bit '1' to the message by adding 0x80
		# if the message length is a multiple of 8-bits
		m += b'0x80'
		# append 0 <= k <= 512 bits '0' such that the
		# resulting message lenght in bits is congruent to
		# -64 === 448 (mod 512)
		while (len(m) % 64) != 56:
			m += chr(0x00)
		# append ml, the original message length as a
		# 64-bit big-endian integer.  The total length
		# is 512 bits
		m += pack('>Q', self.ml)
		self.msg = m
		self.digest() 

	def state(self):
		 return '%08x%08x%08x%08x%08x' % (self.h0, self.h1, self.h2, self.h3, self.h4)

	# rotate integer Left by n bits
	def rotl(self, i, n):
		return ((i << n) | (i >> (32-n))) & 0xFFFFFFFF

	def digest(self):
		#break message into 512-bit chunks
		chunks = []
		for i in range(0, len(self.msg), 64):
			chunks.append(self.msg[i:i+64])
		for chunk in chunks:
			w = []
			for i in range(16):
				w.append(unpack('>I', chunk[0:4])[0])
				chunk = chunk[4:]
			for i in range(16,80):
				w.append(self.rotl(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1))

			a = self.h0
			b = self.h1
			c = self.h2
			d = self.h3
			e = self.h4

			for i in range(80):
				if 0 <= i <= 19:
					f = (b&c) | ((~b)&d)
					k = 0x5A827999
				elif 20 <= i <= 39:
					f = b ^ c ^ d
					k = 0x6ED9EBA1
				elif 40 <= i <= 59:
					f = (b&c) | (b&d) | (c&d) 
					k = 0x8F1BBCDC
				elif 60 <= i <= 79:
					f = b ^ c ^ d
					k = 0xCA62C1D6

				temp = (self.rotl(a,5)+f+e+k+w[i]) & 0xFFFFFFFF
				e = d
				d = c
				c = self.rotl(b,30)
				b = a
				a = temp

			#Add this chunk's hash to result so far:
			self.h0 = (self.h0 + a) & 0xFFFFFFFF
			self.h1 = (self.h1 + b) & 0xFFFFFFFF
			self.h2 = (self.h2 + c) & 0xFFFFFFFF
			self.h3 = (self.h3 + d) & 0xFFFFFFFF
			self.h4 = (self.h4 + e) & 0xFFFFFFFF

# provided a key length, forge a message that
# contains the orignal padding that was input
# to the hash function
def glue_pad(msg, keylen):
	ml = (len(msg)+keylen)*8
	glue = msg
	# append the bit '1' to the message by adding 0x80
	# if the message length is a multiple of 8-bits
	glue += chr(0x80)
	# append 0 <= k <= 512 bits '0' such that the
	# resulting message length in bits is congruent to
	# -64 === 448 (mod 512)
	while (len(glue) % 64) != 56:
		glue += chr(0x00)
	if keylen > 0:
		glue = glue[:-keylen] # Strip bytes for key
	# append ml, the original message length as a
	# 64-bit big-endian integer.  The total length
	# is 512 bits
	glue += pack('>Q', ml)
	return glue

# server-side function, unavailable to attacker
def sign(msg):
	secret_key = "fizzbuzz" #unknown to attacker
	mac = SHA1(secret_key+msg)
	return mac.state()

# server-side function that validates inputs
def verify(msg, mac):
	if mac == sign(msg):
		print "Message with MAC:\t" + sign(msg) + " is valid."
		return True
	else:
		print "Message with MAC:\t" + sign(msg) + " is invalid."
		return False

# provided an original message and valid MAC
# prepare an attack message and forged MAC
# that the server will accept as valid
def forge(origmsg, orig_mac, attack):
	# register states from the valid MAC
	a = int(orig_mac[0:8],  16)
	b = int(orig_mac[8:16], 16)
	c = int(orig_mac[16:24],16)
	d = int(orig_mac[24:32],16)
	e = int(orig_mac[32:40],16)
	
	keylen = 0 # we do not know the lenght of the signing key
	while True:
		msg = glue_pad(origmsg, keylen) + attack
		mac = SHA1(attack, a, b, c, d, e, (len(msg)+keylen)*8).state()
		print "Generated extended MAC:\t" + mac
		if verify(msg, mac):
			print "--------------------------------"
			print "Forged MAC: " + mac
			return msg
		keylen += 1
		if keylen > 64:
			print "Could not solve.  Trialed keysize up to: " + str(keylen)
			return False
			

if __name__ == "__main__":
	import base64
	server_msg = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
	attack = ";admin=true"
	server_mac = sign(server_msg)

	print "--------------------------------"
	print "Server message: " + server_msg 
	print "Server MAC: " + server_mac
	print "--------------------------------"
	print "Desired attack message: " + server_msg+attack
	print "--------------------------------"

	f = forge(server_msg, server_mac, attack)
	if f != False:
		print "--------------------------------"
		print "Forged attack message (hex): "
		print base64.b16encode(f)
	

		
			
		
		
		

	
