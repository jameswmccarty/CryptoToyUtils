#!/usr/bin/python

"""
This code will 'score' input against a 'trained' 
frequency distribution.
"""

import random

#Trainable model
model_norm = [0.0] * 256
model_raw  = [0.0] * 256
model_normalized = False

def resetModel():
	global model_norm 
	global model_raw 
	global model_normalized 
	model_norm = [0.0] * 256
	model_raw  = [0.0] * 256
	model_normalized = False

def meanSquareError(normHist):
	global model_norm
	totalError = 0.0
	temp = 0.0
	for i in range(255):
		temp = normHist[i] - model_norm[i]
		totalError += temp * temp #square the error
	return totalError

def finalizeModel():
	global model_raw
	global model_norm
	global model_normalized
	total = 0.0
	for i in range(255):
		total += model_raw[i]
	if total <= 0.0:
		total = 1.0
	for i in range(255):
		model_norm[i] = model_raw[i] / total
		model_norm[i] *= 100
	model_normalized = True

def updateModel(rawbytes):
	global model_raw
	global model_normalized
	model_normalized = False
	for byte in rawbytes:
		byte = ord(byte)
		model_raw[byte] += 1.0

def printModel():
	global model_normalized
	global model_norm
	if False == model_normalized:
		print "Error: Model not yet finalized."
		exit()
	print '[',
	for i in range(255):
		print model_norm[i],
		print ',',
	print '\b\b]'		

def scoreInput(charHist):
	total = 0.0
	normalCharHist = [0.0] * 256
	if(model_normalized == False):
		print "Error: Training model not yet setup properly."
		exit()
	for i in range(255):
		total += charHist[i]
	if total <= 0.0:
		total = 1.0
	for i in range(255):
		normalCharHist[i] = charHist[i] / total
		normalCharHist[i] *= 100.0
	return meanSquareError(normalCharHist)



#Testing below
if __name__ == "__main__":
	f = open("tests/training_text.txt", "r")
	example1 = f.read()
	f.close()
	#Build up model for text
	resetModel()
	updateModel(example1)
	finalizeModel()
	#printModel()

	print "Testing against Text."

	#Scorable input
	charHist = [0.0] * 256
	f = open("tests/trial_text.txt", "r")
	trial = f.read()
	f.close()
	for byte in trial:
		byte = ord(byte)
		charHist[byte] += 1.0

	print "Text: " + str(scoreInput(charHist))

	charHist = [0.0] * 256
	for i in range(20000):
		charHist[random.randrange(0,255)] += 1.0
	print "Random: " + str(scoreInput(charHist))
	
	charHist = [0.0] * 256
	f = open("tests/wikipedia_Sunset_2007-1.jpg", "r")
	trial = f.read()
	f.close()
	for byte in trial:
		byte = ord(byte)
		charHist[byte] += 1.0
	print "JPEG: " + str(scoreInput(charHist))

	f = open("tests/wikipedia_Ash_Tree.jpg", "r")
	example1 = f.read()
	f.close()
	#Build up model for jpeg
	resetModel()
	updateModel(example1)
	finalizeModel()
	#printModel()


	print "Testing against JPEG."

	#Scorable input
	charHist = [0.0] * 256
	f = open("tests/trial_text.txt", "r")
	trial = f.read()
	f.close()
	for byte in trial:
		byte = ord(byte)
		charHist[byte] += 1.0

	print "Text: " + str(scoreInput(charHist))

	charHist = [0.0] * 256
	for i in range(20000):
		charHist[random.randrange(0,255)] += 1.0
	print "Random: " + str(scoreInput(charHist))
	
	charHist = [0.0] * 256
	f = open("tests/wikipedia_Sunset_2007-1.jpg", "r")
	trial = f.read()
	f.close()
	for byte in trial:
		byte = ord(byte)
		charHist[byte] += 1.0
	print "JPEG: " + str(scoreInput(charHist))
	
	


	
