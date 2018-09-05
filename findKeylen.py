#!/usr/bin/python

"""
This is a utility program that will, for a source
file that has been encrypted using repeating char XOR,
locate the most likely keylengh, and recover the most
likely key.

Assumption is that the source file is ASCII English text.
"""

import base64		#built in
import check_lang	#from repo
import applyXOR		#from repo

def hammingDist(str1, str2):
	dist = 0;
	if len(str1) != len(str2):
		print "Error: Input lengths must match."
		exit()
	for idx in range(0,len(str1)):
		for i in range(7,-1,-1):
			mask = 0x00
			mask |= 0x01 << i
			if (ord(str1[idx]) & mask) ^ (ord(str2[idx]) & mask):
				dist += 1
	return dist

def checkKeysize(instr, guess):
	return hammingDist(instr[0:guess],instr[guess:guess*2])

def normalEditDist(instr, size):
	sets = 0
	total = 0.0
	for i in range(0, len(instr) / size, size):
		total += float(checkKeysize(instr[i:i+size*2],size))
		sets += 1
	total /= float(size)
	total /= float(sets)
	return total

def guessKeysize(instr, maxguess):
	mintrial = 1e9
	bestguess = 0
	for guess in range(2,maxguess+1):
		trial = normalEditDist(instr, guess)
		#print "Keylen: " + str(guess) + " value " + str(trial)
		if trial < mintrial:
			mintrial = trial
			bestguess = guess
	return bestguess

def rebuildKey(instr, keylen):
	fullkey = r""
	for keyidx in range(0,keylen):
		bestkey = 0
		min_err = 1e9
		transpose = r""
		for inidx in range(keyidx,len(instr),keylen):
			transpose += instr[inidx]
		for key in range(0,256):	
			cur_err = check_lang.testForEnglish(applyXOR.rawXORpad(transpose,chr(key)))
			if cur_err < min_err:
				min_err = cur_err
				bestkey = key
		fullkey += chr(bestkey)
	return fullkey

#Examples		
if __name__ == "__main__":
	totaltext = r""
	infile = open("tests/xorpuzzle.txt", "r")
	line = infile.read()
	totaltext = base64.b16decode(line.strip())
	print line
	guess = guessKeysize(totaltext, 40)
	print "Best key length: " + str(guess)
	key = rebuildKey(totaltext, guess)
	print "Key: " + key
	print ""
	print applyXOR.rawXORpad(totaltext, key)



