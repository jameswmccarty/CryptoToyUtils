#!/usr/bin/python

"""
This code will 'score' input against an English ASCII characters
frequency distrubution.  If run with multiple inputs, the
lowest score represents the closest match to English text.
"""


"""
 Letter frequencies for the English language
 values from https://en.wikipedia.org/wiki/Letter_frequency
"""
eng_charfreqs = [
	8.167, 
	1.492, 
	2.782, 
	4.253, 
	12.702, 
	2.228, 
	2.015, 
	6.094, 
	6.966, 
	0.153, 
	0.772, 
	4.025, 
	2.406, 
	6.749, 
	7.507, 
	1.929, 
	0.095, 
	5.987, 
	6.327, 
	9.056, 
	2.758, 
	0.978, 
	2.360, 
	0.150, 
	1.974, 
	0.074,
	0.0]

def meanSquareError(charHist):
	totalError = 0.0
	temp = 0.0
	for i in range(27):
		temp = charHist[i] - eng_charfreqs[i]
		totalError += temp * temp #square the error
	return totalError

def normalizeAndCheck(charHist):
	total = 0.0
	normalCharHist = [0.0] * 27
	for i in range(27):
		total += charHist[i]
	if total <= 0.0:
		total = 1.0
	for i in range(27):
		normalCharHist[i] = charHist[i] / total
		normalCharHist[i] *= 100.0
	return meanSquareError(normalCharHist)

def testForEnglish(rawbytes):
	histogram = [0.0] * 27
	for byte in rawbytes:
		byte = ord(byte)
		if(byte >= 65 and byte <= 90):
			histogram[byte-65] += 1.0;	
		if(byte >= 97 and byte <= 122):
			histogram[byte-97] += 1.0;
		if(byte > 127 or byte < 32):
			histogram[26] += 1.0;
		if(byte >= 33 and byte <= 47):
			histogram[26] += 1.0;
	return normalizeAndCheck(histogram)

#Testing below

b64input = "VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIHRoZSBsYXp5IHByb2dyYW1tZXIu"
ASCIIinput = "The quick brown fox jumps over the lazy programmer."


print testForEnglish(b64input)
print testForEnglish(ASCIIinput)
print testForEnglish("")


	
