#!/usr/bin/python

import urllib
import time

"""
There is a server with a timing leak.

We want to submit a valid input (filename, signature), but we don't know the signature.

i.e. http://localhost:8080/?filename=foo&signature=46b4ec586117154dacd49d664e5d63fdc88efb51

Goal: Determine a valid signature for a given filename by exploiting the timing leak.

Server returns 'HTTP 500' for an invalid signature.
Server returns 'HTTP 200' for a valid signature.

Keys that are more correct take longer to compare.

Start with a base key.  Try combinations for the first byte.  See which one took the longest.
Add that value to our key.  Repeat until HTTP 200 is recieved from server.

Update: Perform several successive tests with each key value, and sum the results.
We expect that the timing difference will be very small, so take repeat samples
to magnify the error.
"""

servername = 'localhost'
port = "8080"
protocol = 'http'

def build_url(filename, usig):
	out = protocol + '://'
	out += servername
	if port != "80":
		out += ':' + port
	out += '/'
	out += '?filename=' + filename
	out += '&signature=' + usig
	return out

def pad(string):
	return string + "0" * (40 - len(string))

def solve_sig(filename):
	sig = ''
	valid = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']

	best_time = 0.00

	MAXTRIALS = 10 # multiple tests (since timing error is small) 

	while True:
		best = ''
		for char in valid:
			trial = sig + char
			print "Testing sig: " + pad(trial)
			delta = 0.0
			for i in xrange(MAXTRIALS):
				start = time.time()
				status = urllib.urlopen(build_url(filename,pad(trial)))
				stop = time.time()
				delta += stop-start
			#print delta
			code = status.getcode()
			if code == None:
				print "Unknown Server Error."
				exit()
			if code == 200:
				return trial
			if code == 500:
				if delta >= best_time:
					best_time = delta
					best = char
		sig += best

if __name__ == "__main__":
	print solve_sig("foo")
