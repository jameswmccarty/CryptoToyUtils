#!/usr/bin/python

import base64

#what is the largest block size that
#will fit evenly into a buffer of
#given length?
def pow2blocks(length):
	guess = 2
	while length % guess == 0:
		guess *= 2
	return guess / 2

#search a bytestream for repeat blocks
#down to size of minsize bytes
def checkECB(rawbytes, minsize):
	chksize = pow2blocks(len(rawbytes)) #must be at least two whole blocks
	while chksize >= minsize:
		buf = rawbytes
		while buf != "":		
			segment = buf[0:chksize]
			buf = buf[chksize:]
			if segment in buf:
				print "ECB Block Duplicate of size " + str(chksize)
				print "Block " + base64.b16encode(segment)
				return True
		chksize /= 2
	return False

if __name__ == "__main__":
	index = 1
	f = open("tests/one_line_has_ECB.txt", "r")
	for text in f:
		text = base64.b16decode((text.strip()).upper())
		if checkECB(text,8) == True:
			print "Input Line number " + str(index)
		index += 1
	f.close()
