import math

alphabet = "abcdefghijklmnopqrstuvwxyz ,."

# implemented from the Extended Euclidean Algorithm pseudocode
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def invmod(a,b):
	old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
	while r:
		q = old_r // r
		old_r, r = r, old_r - q*r
		old_s, s = s, old_s - q*s
		old_t, t = t, old_t - q*t
	return (old_s%b+b)%b

# a measure of similarity of character frequency to the English language
def english_score(m: str) -> float:
	"""
	 Letter frequencies for the English language
	 values from https://en.wikipedia.org/wiki/Letter_frequency
	"""
	eng_charfreqs = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150,1.974, 0.074]
	histogram = [0.0]*26
	letter_count = 0
	for char in m.lower():
		if ord(char) >= ord('a') and ord(char) <= ord('z'):
			histogram[ord(char)-ord('a')] += 1
			letter_count += 1
	histogram = [ (x/letter_count) for x in histogram ]
	return sum( pow(histogram[i]-eng_charfreqs[i],2) for i in range(26) )


# get the message from the cipher using the keyset
def affine_decrypt_cipher(cipher: str, keyset: tuple) -> str:
	cipher = [ alphabet.index(i) for i in cipher.lower() if i in alphabet ]
	a,b = keyset
	a_inv = invmod(a,len(alphabet))
	message = ''.join(alphabet[a_inv*(x-b) % len(alphabet)] for x in cipher)
	return message

def affine_encrypt_message(message: str, keyset: tuple) -> str:
	message = [ alphabet.index(i) for i in message.lower() if i in alphabet ]
	a,b = keyset
	cipher = ''.join(alphabet[(a*x+b) % len(alphabet)] for x in message)
	return cipher

def affine_decrypt_without_key(cipher: str) -> str:
	sols = [] # tuple (score, message)
	# we're going to brute force the key space and see which output looks the best
	for a in [ i for i in range(1,30) if math.gcd(i,29) == 1 ]:
		for b in range(29):
			message = affine_decrypt_cipher(cipher,(a,b))
			sols.append((english_score(message),message))
	message = sorted(sols)[0][1] # take the most English-like phrase
	return message

if __name__ == "__main__":
	message = "Before the modern era, cryptography focused on message confidentiality i.e., encryption conversion of messages from a comprehensible form into an incomprehensible one and back again at the other end, rendering it unreadable by interceptors or eavesdroppers without secret knowledge namely the key needed for decryption of that message. Encryption attempted to ensure secrecy in communications, such as those of spies, military leaders, and diplomats. In recent decades, the field has expanded beyond confidentiality concerns to include techniques for message integrity checking, sender receiver identity authentication, digital signatures, interactive proofs and secure computation, among others.".lower()

	cipher = affine_encrypt_message(message,(5,7))

	print(affine_decrypt_without_key(cipher))
