#!/usr/bin/python

#32-bit MT19937 based Random Number Generator

class RNG:
	# Spec defined coefficients for MT19937
	w = 32; n = 624; m = 397; r = 31;
	mt = [0]*n
	idx = None

	def xSubA(self, x):
		a = int('9908B0DF', 16)
		if (x & 0x01) == 0x01:
			return a
		return 0x0

	def __init__(self, seed = None):
		if seed == None:
			seed = 4357
		self.seed(seed)

	def seed(self, seed):
		f = 1812433253
		w = 32
		self.mt[0] = int(seed) & 0xffffffff
		for i in range(1,self.n):
			self.mt[i] = f*(self.mt[i-1]^(self.mt[i-1]>>(w-2)))+i 
			self.mt[i] &= 0xffffffff
		self.idx = self.n

	def seedState(self, arr):
		if len(arr) != self.n:
			raise ValueError("Must supply 624 values as Array.")
			exit()
		self.idx = 0		
		for elem in arr:
			self.mt[self.idx] = elem
			self.idx += 1
		self.prepareState()
		

	def showState(self):
		print self.mt

	def getState(self):
		return self.mt

	def prepareState(self):
		UM = int('80000000', 16)
		LM = int('7FFFFFFF', 16)
		for k in range(0,self.n-self.m):
			y = (self.mt[k]&UM) | (self.mt[k+1]&LM)
			self.mt[k] = self.mt[k+self.m] ^ (y>>1) ^ self.xSubA(y)
		for k in range(self.n-self.m, self.n-1):
			y = (self.mt[k]&UM) | (self.mt[k+1]&LM)
			self.mt[k] = self.mt[k+(self.m-self.n)] ^ (y>>1) ^ self.xSubA(y)
		y = self.mt[self.n-1]&UM | self.mt[0]&LM
		self.mt[self.n-1] = self.mt[self.m-1] ^ (y>>1) ^ self.xSubA(y)
		self.idx = 0
		
	def rand(self):
		u = 11
		d = int('FFFFFFFF', 16)
		s = 7
		b = int('9D2C5680', 16)
		t = 15
		c = int('EFC60000', 16)
		l = 18
	
		if self.idx == self.n:
			self.prepareState()
		
		# Tempering
		y = self.mt[self.idx]
		self.idx += 1
		y ^= ((y >> u) & d)
		y ^= ((y << s) & b)
		y ^= ((y << t) & c)
		y ^= (y >> l)
		return y

	def randFloat(self):
		return float(self.rand()) / int('FFFFFFFF', 16)


if __name__ == "__main__":
	z = RNG(5489)

	print "Integers: "
	for i in range(0, 100):		
		if i%5==0:
			print ""
		print z.rand(),

	print "\n\nFloats: "
	for i in range(0, 100):		
		if i%5==0:
			print ""
		print z.randFloat(),





	

