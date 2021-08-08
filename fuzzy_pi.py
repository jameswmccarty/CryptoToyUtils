#!/usr/bin/python

import random
import math

samples = 2000000
hits    = 0
for _ in range(samples):
	x,y = random.random(), random.random()
	if math.sqrt(x*x+y*y) < 1.0:
		hits += 1
pi = hits/samples*4
print(pi)
