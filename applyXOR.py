#!/usr/bin/python

"""
Example utility function to accept a string (or raw bytes)
and XOR it with a key.  Key can be of any size, and will
apply as a repeating key if necessary.

Output is a hex encoded string.
"""

import base64

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

#Returns: 	HEX encoded string of rawbytes XOR pad (repeating)
#Inputs: 	rawbytes - ASCII string to encode
#			pad - One or more ASCII chars
def applyXORpad(rawbytes, pad):
	padidx = 0;
	output = ""
	if len(str(pad)) == 0:
		print "Error: pad cannot be zero length"
		exit()
	for byte in rawbytes:
		output += chr(ord(byte) ^ ord(pad[padidx]))
		padidx += 1
		padidx %= len(pad)
	return base64.b16encode(output)

#Testing below
if __name__ == "__main__":
	plaintext = "The quick brown fox jumps over the lazy programmer."
	key = "ABC"

	print applyXORpad(plaintext, key)

	#Verify
	print base64.b16decode(applyXORpad(base64.b16decode(applyXORpad(plaintext, key)), key))
