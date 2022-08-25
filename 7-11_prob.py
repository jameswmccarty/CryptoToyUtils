#!/usr/bin/python

from itertools import combinations

"""
A man buys 4 items from a 7-11.  The sum and product of the prices of the items he bough equal $7.11.  What are the prices of the individual items?
"""

def prod(n):
	acc = 1
	for item in n:
		acc *= item
	return acc

factors = [ x for x in range(1,711) if 711000000 % x == 0 ]

for combo in combinations(factors,4):
	if sum(combo) == 711 and prod(combo) == 711000000:
		print(combo)
