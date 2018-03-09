#!/usr/bin/python

#base64 definition table
b64 = ['A', 'B', 'C', 'D', 	'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']

#map base16 to text
hexkeys = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10, 'A': 10, 'b': 11, 'B': 11, 'c': 12, 'C': 12, 'd': 13, 'D': 13, 'e': 14, 'E': 14, 'f': 15, 'F': 15}

#opposite mapping
keyshex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

#returns converted string
def hextobase64(instr):
	outstr = ""
	b64idx = 5
	b64out = 0
	for char in instr:
		if char in list(hexkeys.keys()):
			for i in range(3,-1,-1):
				if (hexkeys[char] & (0x01 << i)):
					b64out |= 0x01 << b64idx
				b64idx -= 1
				if(b64idx < 0):
					outstr += b64[b64out]
					b64idx = 5
					b64out = 0		
		else:
			print "Error in input format."
			exit()
	if b64idx != 5:
		outstr += b64[b64out]
	return outstr

#returns converted string
def base64tohex(instr):
	outstr = ""
	hexidx = 7
	hexout = 0
	for char in instr:
		if char in b64:
			for i in range(5,-1,-1):
				if (b64.index(char) & (0x01 << i)):
					hexout |= 0x01 << hexidx
				hexidx -= 1
				if(hexidx < 0):
					outstr += keyshex[(hexout>>4)&0x0F]
					outstr += keyshex[hexout&0x0F]
					hexidx=7
					hexout=0
		else:
			print "Error in input format."
			exit()
	return outstr

#encode ASCII hex representation as bytestream
def base16toraw(instr):
	outstr = ""
	if len(instr) % 2 != 0:
		print "Error: malformed input."
		exit()
	for idx in range(0,len(instr),2):
		hi = hexkeys[instr[idx]] << 4
		lo = hexkeys[instr[idx+1]]
		outstr += chr(hi | lo)
	return outstr

#encode ASCII hex representation as bytestream
def base64toraw(instr):
	return base16toraw(base64tohex(instr))

def rawtobase16(instr):
	outstr = ""
	for byte in instr:
		outstr += keyshex[(ord(byte)>>4)&0x0F]
		outstr += keyshex[ord(byte)&0x0F]
	return outstr

def rawtobase64(instr):
	return hextobase64(rawtobase16(instr))
		

#Examples		
if __name__ == "__main__":
	demohexstr = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
	demob64str = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
	temp = hextobase64(demohexstr)
	print temp
	print base64tohex(temp)
	print base16toraw(demohexstr)
	print base64toraw(demob64str)
	print rawtobase16(base16toraw(demohexstr))
	print rawtobase64(base64toraw(demob64str))
