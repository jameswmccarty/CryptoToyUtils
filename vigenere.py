#Keyword Cipher

def applyKey(ascii, key, add):
	output = ''	
	if len(key) == 0:
		print("Error: pad cannot be zero length")
		return
	for i,byte in enumerate(ascii):
		output += chr(65+(((ord(byte)-65)+add*(ord(key[i%len(key)])-65))%26))
	return output

def genkey():
	arr = ['A']
	yield ''.join(arr)
	while True:
		pos = 0
		solving = True
		while solving:
			if arr[pos] >= 'Z':
				arr[pos] = 'A'
				pos += 1
				if pos > len(arr)-1:
					arr += ['A']
					solving = False
			else:
				arr[pos] = chr(ord(arr[pos])+1)
				solving = False
		yield ''.join(arr)

#Testing below
if __name__ == "__main__":
	plain = "DIQDMLQSLOXUYXFBIC" # key = 'KEY'

	"""
	with open("words.txt", 'r') as infile:
		wordpool = infile.read()
	ignore = [".", ",", "(", ")", "-", ' '] + [ str(x) for x in range(10) ]
	for item in ignore:
		wordpool = wordpool.replace(item, ' ')
	words = list(set(wordpool.split("\n")))
	words = [ x.strip().upper() for x in words if len(x.strip()) > 0]
	for key in words:
	"""
	
	"""
	for x in genkey():
		if len(x) > 4:
			exit()
		key = x

	"""

	while True:
		key = input("key --> ")

		print(key.strip().upper(), '\t', applyKey(plain, key, 1), applyKey(plain, key, -1), applyKey(plain[::-1], key, 1), applyKey(plain[::-1], key, -1))

