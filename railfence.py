#!/usr/bin/python

PUZZ = "DNETLEEDHESWLXFTAAX"

def applyRot(ascii, key):
	output = ''
	for i,byte in enumerate(ascii):
		if ord(byte) < 65 or ord(byte) > 90:
			output += byte
		else:
			output += chr(65+(((ord(byte)-65)+key)%26))
	return output

def railFenceDecrypt(string, key):
	string = string.upper()
	main = []
	for i in range(key):
		main.append( [' '] * len(string))
	q = 0;
	for t in range(len(main)):
		j = 0;
		r = 0;
		for i in range(len(string)):
			if (j == t):
				c = string[q]
				main[j][i] = c
				q = q + 1
			if (r == 0):
				j = j + 1
			elif (r == 1):
				j = j - 1
			if (j == key - 1):
				r = 1
			elif (j == 0):
				r = 0
	j = 0
	r = 0
	plain = ""
	for i in range(len(string)):
		plain = plain + str(main[j][i])
		if r == 0:
			j = j + 1
		elif r == 1:
			j = j - 1
		if j == key - 1:
			r = 1
		elif j == 0:
			r = 0
	plain = plain.lower()
	return plain

print(len(PUZZ))
print(PUZZ)
#for _ in range(26):
#	for i in range(2,len(PUZZ)):
#		sol = railFenceDecrypt(applyRot(PUZZ,_), i)
#		print(sol)
for i in range(2,len(PUZZ)):
	sol = railFenceDecrypt(PUZZ, i)
	print(sol)
