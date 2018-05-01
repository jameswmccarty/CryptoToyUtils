#!/usr/bin/python

import web
import sys
import HMAC_SHA1 as hmac
import time

"""
Demonstrate breaking HMAC-SHA1 on a webserver
using an (artificial) timing attack
"""

""" This module serves as an insecure web server """


urls = ('/', 'index',
		'/debug/', 'debug')

server_key = 'foobarfizzbuzz' # unknown to the outside

class FileValidator:
	# timing leak introduced
	# compare char-by-char our given sig and server sig
	def insecure_compare(self, fname_, usig_):
		ssig_ = hmac.HMAC_SHA1(server_key, fname_)		
		for i in range(0, len(usig_)):
			if ssig_[i] != usig_[i]:
				return False
			time.sleep(0.005) # whoops!
		return True # sig is valid

	# for debugging, generate valid server keys
	def get_sig(self, fname_):
		return hmac.HMAC_SHA1(server_key, fname_)

# Takes a "file" argument and a "signature" argument, i.e.:
# http://localhost:8080/?filename=foo&signature=46b4ec586117154dacd49d664e5d63fdc88efb51
# Compares signature to file HMAC
# Returns a 500 if the MAC is invalid, and a 200 if it's OK.
class index:
	def GET(self):
		i = web.input(filename="", signature="")
		if i.filename == "" or i.signature == "":
			return "Example - http://localhost:8080/?filename=foo&signature=46b4ec586117154dacd49d664e5d63fdc88efb51"
		if FileValidator().insecure_compare(i.filename, i.signature):
			return web.ok() # 200 error
		else:
			return web.InternalError(message=None) # 500 error

# Takes a "file" argument and return a valid Server Signature:
# http://localhost:8080/debug/?filename=foo
# only here for testing
# http://localhost:8080/?filename=foo&signature=9e1d9f3ef7abc6d7e51366e4c7834e92b5bd1c71 #valid
class debug:
	def GET(self):
		i = web.input(filename="")
		return FileValidator().get_sig(i.filename)		
        

if __name__ == "__main__":
	#reload(sys)
	#sys.setdefaultencoding('utf-8')
	web.config.debug = False
	app = web.application(urls, globals())
	app.run()
