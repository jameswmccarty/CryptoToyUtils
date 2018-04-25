#!/usr/bin/python

import random

"""
A simple example implementation of the Diffie-Hellman key exchange algorithm.
"""


"""
Modular Exponentiation
given a, b, and p
solve for:

(a**b) % p

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
Choose a modulus (p) and a base (g) where p is prime and g is a primative root modulo p.  These values are public and agreed upon.
"""

# set p to example NIST value
NISTp = 'FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF'
p = int(NISTp,16) # modulus
g = 2  # NIST base

"""
Choose a secret (a).  Compute A = (g**a) % p

A is a public key.

"""

a = random.getrandbits(256)
#A = (g**a) % p
A = modexp(g,a,p)

"""
Choose a secret (b).  Compute B = (g**b) % p

B is a public key.

"""

b = random.getrandbits(256)
#B = (g**b) % p
B = modexp(g,b,p)

"""
Generate a session key.  Example:
s = (B**a) % p
s = (A**b) % p
"""
def session_key(public, secret, modulus):
	#s = (public**secret) % modulus
	s = modexp(public,secret,modulus)	
	return s

key1 = session_key(A,b,p)
key2 = session_key(B,a,p)

print "Modulus:\t\t" + str(p)
print "Base:\t\t\t" + str(g)
print "Alice secret:\t\t" + str(a)
print "Bob secret:\t\t" + str(b)
print "Alice's session key:\t" + str(key1)
print "Bob's session key:\t" + str(key2)
