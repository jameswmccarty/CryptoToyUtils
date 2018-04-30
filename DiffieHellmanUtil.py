#!/usr/bin/python

import random

"""
Utility Functinos for Diffie-Hellman key exchange algorithm.
"""

"""
Choose a modulus (p) and a base (g) where p is prime and g is a primative root modulo p.  
These values are public and agreed upon.
"""
# set p to example NIST value
NISTp = int('FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E\
088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0\
A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF\
5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC20\
07CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C\
62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327F\
FFFFFFFFFFFFFFF',16) 
NISTg = 2  # NIST base

# simple example values
SIMPp = 37 # modulus
SIMPg = 5  # base

"""
Modular Exponentiation
given a, b, and p
solve for: (a**b) % p
(a mod p)(b mod p) === (ab) mod p
"""
def modexp(a, b, p):
	s = 1
	a = a % p
	while b > 0:
		if b & 0x01 == 0x01:
			s = (s*a) % p
		b = b>>1
		a = (a*a) % p
	return s

"""
Choose a secret (a).  Compute A = (g**a) % p
A is a public key.

returns (private, public)

"""
def gen_key_pair(numbits=None, modulus=None, base=None):
	if numbits == None:
		numbits = 256
	if modulus == None:
		modulus = NISTp
	if base == None:
		base = NISTg #NIST base
	a = random.getrandbits(numbits)
	return (a, modexp(base,a,modulus))

"""
Generate a session key.  Example:
s = (B**a) % p
s = (A**b) % p
"""
def session_key(public, secret, modulus):
	#s = (public**secret) % modulus
	s = modexp(public,secret,modulus)	
	return s

if __name__ == "__main__":


	a, A = gen_key_pair()
	b, B = gen_key_pair()

	key1 = session_key(A,b,NISTp)
	key2 = session_key(B,a,NISTp)

	print "Modulus:\t\t" + str(NISTp)
	print "Base:\t\t\t" + str(NISTg)
	print "Alice secret:\t\t" + str(a)
	print "Bob secret:\t\t" + str(b)
	print "Alice's session key:\t" + str(key1)
	print "Bob's session key:\t" + str(key2)
