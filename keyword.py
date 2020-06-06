#!/usr/bin/python

puzz = "ZLJEFTDTOT"

alpha = [chr(x) for x in range(65,91)]

def accept_keyword(word):
	word = word.strip().upper()
	new_alpha = []
	for letter in word:
		if letter not in new_alpha:
			new_alpha.append(letter)
	t = [ x for x in alpha ]
	for letter in new_alpha:
		try:
			t.remove(letter[0])
		except:
			print("Count not filter", letter)
	new_alpha += t
	if(len(new_alpha) > 26):
		print("Invalid Keyword")
		exit()
	return new_alpha

def decode(msg, alpha):
	out = ''
	for char in msg:
		out += chr(65+alpha.index(char))
	return(out)

def encode(msg, alpha):
	out = ''
	for char in msg:
		out += alpha[ord(char)-65]
	return(out)

tester = accept_keyword("secret")
#print(tester)
#print(encode("ZOMBIEHERE", tester))
print(decode(puzz, tester))
