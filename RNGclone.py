#!/usr/bin/python

import MT19937 as rand
import time

def untempS(y):
	b = int('9D2C5680', 16)
	low7 = y & 0x0000007F 
	high0 = (~b & ~0x0000007F) & y 
	mid7 = ((y)^((low7&(b>>7))<<7))&(0x3F80) 
	#solve remaining bits cascade
	if(mid7 & (0x01<<7)) != 0: 
		bit15 = (~y & (0x01<<14))
	else:
		bit15 = (y & (0x01<<14))
	if(mid7 & (0x01<<11)) != 0:
		bit19 = (~y & (0x01<<18))
	else:
		bit19 = (y & (0x01<<18))
	if(mid7 & (0x01<<12)) != 0:
		bit20 = (~y & (0x01<<19))
	else:
		bit20 = (y & (0x01<<19))
	if(bit15 != 0):
		bit22 = (~y & (0x01<<21))
	else:
		bit22 = (y & (0x01<<21))
	if (high0 & (0x01<<17)) != 0:
		bit25 = (~y & (0x01<<24))
	else:
		bit25 = (y & (0x01<<24))
	if bit20 != 0:
		bit27 = (~y & (0x01<<26))
	else:
		bit27 = (y & (0x01<<26))
	if (high0 & (0x01<<20))!= 0:
		bit28 = (~y & (0x01<<27))
	else:
		bit28 = (y & (0x01<<27))
	if (bit22)!= 0:
		bit29 = (~y & (0x01<<28))
	else:
		bit29 = (y & (0x01<<28))
	if (bit25)!= 0:
		bit32 = (~y & (0x01<<31))
	else:
		bit32 = (y & (0x01<<31))	
	y = mid7 | low7 | high0 | bit15 | bit19 | bit20 | bit22 | bit25 | bit27 | bit28 | bit29 | bit32
	return y

def untempU(y):
	high11 = y & 0xFFE00000
	out = high11	
	for i in range(20,-1,-1):
		bit = ((out&(0x01<<(i+11)))>>11)^(y&((0x01)<<i))
		out |= bit
	return out

# Inverse of Tempering function in MT19937
def untemper(x):
	u = 11
	d = int('FFFFFFFF', 16)
	s = 7	
	t = 15
	c = int('EFC60000', 16)
	l = 18

	x ^= ((x >> l) & d) & d 
	x ^= ((x << t) & c) & d 
	x = untempS(x)
	x = untempU(x)
	
	return x

if __name__ == "__main__":
	server_rnds = [0]*624 # Collected from "server"
	print "Creating new RNG."
	z = rand.RNG(int(time.time()))    # Target RNG to Clone
	
	#secret_state = z.getState() # Verify values
	
	for i in range(len(server_rnds)):
		server_rnds[i] = untemper(z.rand())

	print "Collected 624 random numbers."

	#for i in range(len(server_rnds)):
	#	print "Secret: " + str(secret_state[i]),
	#	print " Recovered: " + str(server_rnds[i])

	print "Seeding Clone RNG..."

	clone = rand.RNG()
	clone.seedState(server_rnds)

	print "Next 100 random values: "
	for i in range(1, 100):
		print "Target: " + str(z.rand()) + "\t",
		print "Clone: " + str(clone.rand())

	


	

	

