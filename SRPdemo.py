import hashlib
import random
import binascii

"""
Implement Secure Remote Password

https://en.wikipedia.org/wiki/Secure_Remote_Password_protocol

 To understand SRP, look at how you generate an AES key from DH; now, just observe you can do the "opposite" operation an generate a numeric parameter from a hash. Then:
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

# Replace A and B with C and S (client & server)
# C & S
#  Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)

random_s = 64

NISTp = 'FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF'
N = int(NISTp,16) # modulus

g = 2
k = 3

I = "me@example.com"
P = "Password123Password123"

# S
#  Generate salt as random integer
#  Generate string xH=SHA256(salt|password)
#  Convert xH to integer x somehow (put 0x on hexdigest)
#  Generate v=g**x % N
#  Save everything but x, xH

salt = random.getrandbits(random_s)
x = int(hashlib.sha256(str(salt)+P).hexdigest(),16)
v = modexp(g,x,N) # g**x % N
del x

# C->S
#  Send I, A=g**a % N (a la Diffie Hellman)

a = random.getrandbits(random_s)
A = modexp(g,a,N) # g**a % N

# S->C
#  Send salt, B=kv + g**b % N
b = random.getrandbits(random_s)
B = k*v + modexp(g,b,N)

# S, C
#  Compute string uH = SHA256(A|B), u = integer of uH

uS = int(hashlib.sha256(str(A)+str(B)).hexdigest(),16)
uC = int(hashlib.sha256(str(A)+str(B)).hexdigest(),16)

# C
#  Generate string xH=SHA256(salt|password)
#  Convert xH to integer x somehow (put 0x on hexdigest)
#  Generate S = (B - k * g**x)**(a + u * x) % N
#  Generate K = SHA256(S)

x = int(hashlib.sha256(str(salt)+P).hexdigest(),16)
CS = modexp(B - k * modexp(g,x,N),a+uC*x,N)
CK = hashlib.sha256(str(CS)).hexdigest()

# S
#  Generate S = (A * v**u) ** b % N
#  Generate K = SHA256(S)

SS = modexp(A * modexp(v,uS,N),b,N)
SK = hashlib.sha256(str(SS)).hexdigest()

print CK
print SK

# C->S
#  Send HMAC-SHA256(K, salt)

client_val = hashlib.pbkdf2_hmac('sha256',str(CK),str(salt),10000)
print binascii.hexlify(client_val)
	
# S->C
#  Send "OK" if HMAC-SHA256(K, salt) validates

server_val = hashlib.pbkdf2_hmac('sha256',str(SK),str(salt),10000)
print binascii.hexlify(server_val)

if server_val == client_val:
	print "OK"
else:
	print "Fail"
