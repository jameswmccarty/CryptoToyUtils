def gen_primes():
	i = 2
	divs = {}
	while True:
		yield i
		if i+i in divs:
			divs[i+i].add(i)
		else:
			divs[i+i] = {i}
		i += 1
		while i in divs:
			factors = divs.pop(i)
			for j in factors:
				if i+j in divs:
					divs[i+j].add(j)
				else:
					divs[i+j] = {j}
			i += 1

if __name__ == "__main__":

	# first 1000 primes
	z = gen_primes()
	print( [next(z) for _ in range(1000)] )
