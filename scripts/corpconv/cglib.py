#!/usr/bin/env python3

import re

with open("testdata", "r") as datafile:
	testdata = datafile.read()

tokenRe = re.compile("^\"<(.*?)>\"$")
parseRe = re.compile("^(;?).*\"(.*?)\" (.*)$")

class Sentence:
	global tokenRe
	global parseRe
	tokens = []

	def __init__(self, data):
		started = False
		parseLines = []
		for line in data.split('\n'):
			if tokenRe.match(line):
				if started:
					self.tokens.append(Token(thisToken, parseLines))
					parseLines = []
				else:
					started = True
				thisToken = line
			elif parseRe.match(line):
				parseLines.append(line)

			else:
				print(line)
		#print(parseLines)
	
	def __repr__(self):
		return self.tokens
	
	def __str__(self):
		output = ""
		for token in self.tokens:
			output+=str(token)+"\n"
		return output


class Token:
	global tokenRe
	global parseRe

	token = ""
	parses = []

	def __init__(self, token, parseLines):
		self.token = tokenRe.match(token).group(1)
		#print(self.token)
		print(len(parseLines))
		for parse in parseLines:
			self.parses.append(Parse(parse))
	
	def __repr__(self):
		return {self.token: self.parses}
	
	def __str__(self):
		output = "=="+self.token+"\n"
		for parse in self.parses:
			output += str(parse)+"\n"
		return output
	
class Parse:
	global tokenRe
	global parseRe

	lemma = ""
	tags = []
	decisions = []
	commented = False

	def __init__(self, line):
		#print(line)
		(commented, self.lemma, tags) = parseRe.match(line).groups()
		if commented != "": self.commented = True
		#print(self.commented)
		self.tags = tags.split()

	def __str__(self):
		output = self.lemma+": "
		for tag in self.tags:
			output += tag+", "
		return output


if __name__ == '__main__':
	sent = Sentence(testdata)
	print(sent)
