#!/usr/bin/python

""" Utility functions to pad files using
the PKCS-7 mode of padding.  The number
of bytes used for padding is appended to
fill a blocksize fully. """

#Pad a single block
def pkcs7pad(pt, blksize):
	padsize = blksize - len(pt)
	if padsize < 0:
		print "Error: Message too long for block size."
		exit()
	padblock = ""
	for byte in pt:
		padblock += byte
	for i in range(len(pt),blksize):
		padblock += chr(padsize)
	return padblock

#When given a file's contents and a blocksize
#return the PKCS-7 padded version.
#
# Input: intext - Raw file contents
# Input: blksize - Number of bytes in block
# Output: PKCS-7 padded content
def padInput(intext, blksize):
	outtext = "" #return vector
	padblock = ""
	if blksize <= 0:
		print "Error: BLOCK SIZE cannot be <= 0"
		exit()
	wholeblks = len(intext) / blksize
	delta = len(intext) % blksize
	if delta == 0:
		#File length is a multiple of blksize
		#Nothing to do
		return intext
	outtext = intext[0:wholeblks*blksize] #out is all but last block
	padblock = pkcs7pad(intext[wholeblks*blksize:],blksize)
	outtext += padblock
	return outtext

#When given a file's contents that have been
#padded, test for and remove any padding from
#the final block.
#
# Input: padtext - Raw file contents (padded)
# Input: blksize - Number of bytes in block
# Output: unpadded content
def clearPad(padtext, blksize):
	outtext = ""
	lastblock = ""
	if blksize <= 0:
		print "Error: BLOCK SIZE cannot be <= 0"
		exit()
	if len(padtext) % blksize != 0:
		print "Error: Input is not a multiple of BLOCK SIZE"
		exit()	
	numblks = len(padtext) / blksize
	outtext = padtext[0:((numblks-1)*blksize)] #all but final block
	lastblock = padtext[((numblks-1)*blksize):] #finalblock
	byteval = ord(lastblock[blksize-1]) #read last byte
	if byteval == 0: #can never pad with zero
		outtext += lastblock
		return outtext
	if byteval >= blksize: #pad chars will never exceed blksize
		outtext += lastblock
		return outtext
	for i in range(blksize-1, blksize-byteval-1, -1):
		if byteval != ord(lastblock[i]): #Improperly padded
			print "Error: File was improperly padded."
			raise ValueError('File padding is incorrect.')
	lastblock = lastblock[0:blksize-byteval] #strip padding
	outtext += lastblock
	return outtext

""" Testing functions and examples below """
if __name__ == "__main__":
	#Pad a single block test
	plaintext = "FOOBAR FIZZ BUZZ"
	brokenblock = "0123456789AB"
	brokenblock += chr(5)
	brokenblock += chr(4)
	brokenblock += chr(4)
	brokenblock += chr(4)
	print pkcs7pad(plaintext, 20)

	plaintext2 = "The quick brown fox jumps over the lazy programmer."
	print padInput(plaintext2, 16)
	padtext = padInput(plaintext2, 16)
	print clearPad(padtext, 16)
	try:
		print clearPad(brokenblock, 16)
	except ValueError:
		print "Failure."
