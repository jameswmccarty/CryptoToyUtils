#!/usr/bin/python

# A pure Python implementation of the
# MD4 Message-Digest Algorithm 
# Based on RFC1320

# For educational purposes only
# Not for use in production code

from struct import pack
from struct import unpack

class MD4:

	# initial magic numbers
	A = 0x67452301
	B = 0xefcdab89
	C = 0x98badcfe
	D = 0x10325476

	ml  = None # Length of message in bits
	msg = None # Padded message

	def __init__(self, m, a=None, b=None, c=None, d=None, length=None):
		# allow internal state to be set
		if a != None:
			self.A = a & 0xffffffff
		if b != None:
			self.B = b & 0xffffffff
		if c != None:
			self.C = c & 0xffffffff
		if d != None:
			self.D = d & 0xffffffff
		# get the message length in bits
		if length == None:
			self.ml = len(m) * 8
		else: # override for length extension attacks
			self.ml = length
		# append the bit '1' to the message by adding 0x80
		# if the message length is a multiple of 8-bits
		m += chr(0x80)
		# append 0 <= k <= 512 bits '0' such that the
		# resulting message lenght in bits is congruent to
		# -64 === 448 (mod 512)
		while (len(m) % 64) != 56:
			m += chr(0x00)
		# append ml, the original message length as a
		# 64-bit big-endian integer.  The total length
		# is 512 bits
		m += pack('<Q', self.ml)
		self.msg = m
		self.digest()

	def state(self):
		 # byte order has to be swapped for printing
		 return '%08x%08x%08x%08x' % unpack('<IIII', pack('>IIII', self.A, self.B, self.C, self.D))[0:4]

	def digest(self):
		#break message into 512-bit chunks
		chunks = []
		for i in range(0, len(self.msg), 64):
			chunks.append(self.msg[i:i+64])
		for chunk in chunks:
			w = []
			for i in xrange(16):
				w.append(unpack('<I', chunk[0:4])[0])
				chunk = chunk[4:]
			self.MD4Transform(w)

	def F(self, x, y, z):
		return x & y | ~x & z

	def G(self, x, y, z): 
		return x & y | x & z | y & z

	def H(self, x, y, z):
		return x ^ y ^ z

	def FF(self, a, b, c, d, x, s):
		a = (a + self.F(b, c, d) + x) & 0xffffffff
		return self.rotl(a, s)

	def GG(self, a, b, c, d, x, s):
		a = (a + self.G(b, c, d) + x + 0x5a827999) & 0xffffffff
		return self.rotl(a, s)

	def HH(self, a, b, c, d, x, s):
		a = (a + self.H(b, c, d) + x + 0x6ed9eba1) & 0xffffffff
		return self.rotl(a, s)

	# rotate integer Left by n bits
	def rotl(self, i, n):
		return ((i << n) | (i >> (32-n))) & 0xffffffff

	def MD4Transform(self, x):

		a = self.A
		b = self.B
		c = self.C
		d = self.D

		# Constants for MD4Transform
		S11 = 3
		S12 = 7
		S13 = 11
		S14 = 19
		S21 = 3
		S22 = 5 
		S23 = 9
		S24 = 13
		S31 = 3
		S32 = 9 
		S33 = 11
		S34 = 15

  		# Round 1 
  		a = self.FF(a, b, c, d, x[ 0], S11); # 1 
  		d = self.FF(d, a, b, c, x[ 1], S12); # 2 
		c = self.FF(c, d, a, b, x[ 2], S13); # 3 
		b = self.FF(b, c, d, a, x[ 3], S14); # 4 
		a = self.FF(a, b, c, d, x[ 4], S11); # 5 
		d = self.FF(d, a, b, c, x[ 5], S12); # 6 
		c = self.FF(c, d, a, b, x[ 6], S13); # 7 
		b = self.FF(b, c, d, a, x[ 7], S14); # 8 
		a = self.FF(a, b, c, d, x[ 8], S11); # 9 
  		d = self.FF(d, a, b, c, x[ 9], S12); # 10 
  		c = self.FF(c, d, a, b, x[10], S13); # 11 
  		b = self.FF(b, c, d, a, x[11], S14); # 12 
  		a = self.FF(a, b, c, d, x[12], S11); # 13 
  		d = self.FF(d, a, b, c, x[13], S12); # 14 
  		c = self.FF(c, d, a, b, x[14], S13); # 15 
  		b = self.FF(b, c, d, a, x[15], S14); # 16 

  		# Round 2 
  		a = self.GG(a, b, c, d, x[ 0], S21); # 17 
  		d = self.GG(d, a, b, c, x[ 4], S22); # 18 
  		c = self.GG(c, d, a, b, x[ 8], S23); # 19 
  		b = self.GG(b, c, d, a, x[12], S24); # 20 
  		a = self.GG(a, b, c, d, x[ 1], S21); # 21 
 		d = self.GG(d, a, b, c, x[ 5], S22); # 22 
  		c = self.GG(c, d, a, b, x[ 9], S23); # 23 
  		b = self.GG(b, c, d, a, x[13], S24); # 24 
  		a = self.GG(a, b, c, d, x[ 2], S21); # 25 
  		d = self.GG(d, a, b, c, x[ 6], S22); # 26 
  		c = self.GG(c, d, a, b, x[10], S23); # 27 
  		b = self.GG(b, c, d, a, x[14], S24); # 28 
  		a = self.GG(a, b, c, d, x[ 3], S21); # 29 
  		d = self.GG(d, a, b, c, x[ 7], S22); # 30 
  		c = self.GG(c, d, a, b, x[11], S23); # 31 
  		b = self.GG(b, c, d, a, x[15], S24); # 32

		# Round 3
		a = self.HH(a, b, c, d, x[ 0], S31); # 33
		d = self.HH(d, a, b, c, x[ 8], S32); # 34 
 		c = self.HH(c, d, a, b, x[ 4], S33); # 35 
 		b = self.HH(b, c, d, a, x[12], S34); # 36 
  		a = self.HH(a, b, c, d, x[ 2], S31); # 37 
  		d = self.HH(d, a, b, c, x[10], S32); # 38 
  		c = self.HH(c, d, a, b, x[ 6], S33); # 39 
  		b = self.HH(b, c, d, a, x[14], S34); # 40 
  		a = self.HH(a, b, c, d, x[ 1], S31); # 41 
  		d = self.HH(d, a, b, c, x[ 9], S32); # 42 
  		c = self.HH(c, d, a, b, x[ 5], S33); # 43 
  		b = self.HH(b, c, d, a, x[13], S34); # 44 
  		a = self.HH(a, b, c, d, x[ 3], S31); # 45 
  		d = self.HH(d, a, b, c, x[11], S32); # 46 
  		c = self.HH(c, d, a, b, x[ 7], S33); # 47 
  		b = self.HH(b, c, d, a, x[15], S34); # 48 

		self.A = (self.A + a) & 0xffffffff
		self.B = (self.B + b) & 0xffffffff
		self.C = (self.C + c) & 0xffffffff
		self.D = (self.D + d) & 0xffffffff

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
	glue += pack('<Q', ml)
	return glue

# server-side function, unavailable to attacker
def sign(msg):
	secret_key = "foobarsecret" #unknown to attacker
	mac = MD4(secret_key+msg)
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

	# repair byte order of internal state

	a = unpack('<I', pack('>I', a))[0]
	b = unpack('<I', pack('>I', b))[0]
	c = unpack('<I', pack('>I', c))[0]
	d = unpack('<I', pack('>I', d))[0]	
	
	keylen = 0 # we do not know the lenght of the signing key
	while True:
		msg = glue_pad(origmsg, keylen) + attack
		mac = MD4(attack, a, b, c, d, (len(msg)+keylen)*8).state()
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

	# paper test vectors
	"""
	print MD4("").state()		#31d6cfe0d16ae931b73c59d7e0c089c0
	print MD4("a").state()		#bde52cb31de33e46245e05fbdbd6fb24
	print MD4("abc").state()	#a448017aaf21d8525fc10ae87aa6729d
	print MD4("message digest").state()	#d9130a8164549fe818874806e1c7014b
	print MD4("abcdefghijklmnopqrstuvwxyz").state() #d79e1c308aa5bbcdeea8ed63df412da9
	print MD4("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789").state() #043f8582f241db351ce627e153e7f0e4
	print MD4("12345678901234567890123456789012345678901234567890123456789012345678901234567890").state() #e33b4ddc9c38f2199c3e7b164fcc0536
	"""

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


	
