#!/usr/bin/python

""" Utility functions to pad files using
the PKCS-7 mode of padding.  The number
of bytes used for padding is appended to
fill a blocksize fully. """

class PKCS7Encoder:
	blksize = None #Default

	def __init__(self, blksize=None):
		self.blksize = 16 if blksize is None else blksize
		if self.blksize < 2 or self.blksize > 255:
			raise ValueError('Specified Block Size of: ' + str(self.blksize) + ' is invalid.')
			exit()

	# Pad a raw byte stream and return.
	def encode(self, stream):
		pad = b''
		wb = len(stream) / self.blksize
		padsize = (wb*self.blksize-len(stream)) % self.blksize
		if padsize == 0: #Provide a full block of padding
			padsize = self.blksize
		pad = padsize * chr(padsize)
		return stream + pad

	# Validate and strip padding from a raw byte stream.
	def decode(self, stream):
		if len(stream) == 0: # Null input
			raise ValueError('Error: Zero-length input.')
		byteval = ord(stream[-1]) # Read last byte
		if byteval == 0 or byteval > self.blksize:
			raise ValueError('File padding is corrupt or incorrect.')
		for idx in range(len(stream)-1, len(stream)-byteval-1, -1):
			if byteval != ord(stream[idx]): # Improperly padded
				raise ValueError('File padding is incorrect.')
		return stream[0:-byteval] # Strip padding

""" Testing functions and examples below """
if __name__ == "__main__":

	import base64
	
	#Pad a single block test
	plaintext = "FOOBAR FIZZ BUZZ "
	brokenblock = "0123456789AB"
	brokenblock += chr(5)
	brokenblock += chr(4)
	brokenblock += chr(4)
	brokenblock += chr(4)

	encoder1 = PKCS7Encoder(blksize=64)
	print encoder1.blksize
	print base64.b16encode(encoder1.encode(plaintext))
	print encoder1.decode(encoder1.encode(plaintext))

	encoder2 = PKCS7Encoder()

	plaintext2 = "The quick brown fox jumps over the lazy programmer."
	padtext = encoder2.encode(plaintext2)
	print base64.b16encode(padtext)
	print encoder2.decode(padtext)
	print encoder2.decode(encoder2.encode("")) # Null input check
	try:
		print encoder2.decode(brokenblock)
	except ValueError:
		print "Failure."
