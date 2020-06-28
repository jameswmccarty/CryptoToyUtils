""" makes a copy of itself """

import sys

if __name__ == "__main__":
	n = sys.argv[0]
	with open(n, 'r') as infile:
		o = infile.read()
	n = n.split(".")
	with open(n[0]+"_cp.py", 'w') as outfile:
		outfile.write(o)
