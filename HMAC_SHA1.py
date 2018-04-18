#/usr/bin/python

# A pure Python implementation of the SHA-1 algorithm
# Code adapted from Wikipedia https://en.wikipedia.org/wiki/SHA-1

# Not for use in production code :-)

from struct import pack
from struct import unpack
import base64

class SHA1:

	# Initial values
	h0 = 0x67452301
	h1 = 0xEFCDAB89
	h2 = 0x98BADCFE
	h3 = 0x10325476
	h4 = 0xC3D2E1F0

	ml = None # Length of message in bits
	msg = None # Padded message

	def __init__(self, m):
		# set the message length in bits
		self.ml = len(m) * 8
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

#Returns: 	raw string of rawbytes XOR pad (repeating)
#Inputs: 	rawbytes - ASCII string to encode
#			pad - One or more ASCII chars
def rawXORpad(rawbytes, pad):
	padidx = 0;
	output = ""
	if len(str(pad)) == 0:
		print "Error: pad cannot be zero length"
		exit()
	for byte in rawbytes:
		output += chr(ord(byte) ^ ord(pad[padidx]))
		padidx += 1
		padidx %= len(pad)
	return output


def HMAC_SHA1(key, message):
	if len(key) > 64:
		key = SHA1(key).state()         # key is the hash of the key value
	key += chr(0) * (64-len(key))		# pad to 64 bytes with zeros to the right
	o_key_pad = rawXORpad(key, chr(92)) # 0x5C
	i_key_pad = rawXORpad(key, chr(54)) # 0x36
	first = SHA1(i_key_pad+message).state()
	first = base64.b16decode(first.upper()) # requires raw bytes
	return SHA1(o_key_pad+first).state()

if __name__ == "__main__":
	print HMAC_SHA1("", "") #fbdb1d1b18aa6c08324b7d64b71fb76370690e1d
	print HMAC_SHA1("key", "The quick brown fox jumps over the lazy dog") #de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9	
