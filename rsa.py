import base64
import random
import math
from Crypto.Util import number


def is_prime(n):
	if n < 2:
		return False
	i = 2
	while i < int(math.sqrt(n))+1:
		if n%i == 0:
			return False
		i += 1
	return True

def random_prime(size):
	return number.getPrime(size)
	#while True:
	#	n = random.getrandbits(size) | 1 << (size - 1 ) | 1
	#	if is_prime(n):
	#		return n
	#	n += 2

def invmod(a,b):
	old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
	while r:
		q = old_r // r
		old_r, r = r, old_r - q*r
		old_s, s = s, old_s - q*s
		old_t, t = t, old_t - q*t
	return (old_s%b+b)%b

def gen_rsa_keypair(size):

	# Generate 2 random primes.  Call them "p" and "q".

	p = random_prime(size)
	q = random_prime(size)
	while p == q:
		q = random_prime(size)

	# Let n be p * q. Your RSA math is modulo n.
	n = p*q
	#Let et be (p-1)*(q-1) (the "totient"). You need this value only for keygen.
	et = math.lcm(p-1,q-1)
	e = 3
	while math.gcd(e,et) != 1 and e < et:
		e += 1
	# Compute d = invmod(e, et)
	d = invmod(e,et)
	#Your public key is [e, n]. Your private key is [d, n]
	return (e,n),(d,n)

# input public key and plain text message
def encrypt(public_key,message):
	e,n = public_key
	message = int.from_bytes(message.encode('utf-8'))
	return pow(message,e,n)

# input private key and cipher text
def decrypt(private_key,cipher_text):
	d,n = private_key
	m = pow(cipher_text,d,n)
	return m.to_bytes(m.bit_length()+7//8).decode('utf-8')

if __name__ == "__main__":

	# RSA Example

	public_key,private_key = gen_rsa_keypair(1024)
	print(public_key,private_key)
	c = encrypt(public_key,"This is a long test of RSA encryption.")
	print(c)
	print(decrypt(private_key,c))
