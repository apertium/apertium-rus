#!/usr/bin/env python3

import re

tokenRe = re.compile("^\"<(.*?)>\"$")
parseRe = re.compile("^(;?).*\"(.*?)\" (.*)$")

class Sentence:
	global tokenRe
	global parseRe
	tokens = []
	sentence = ""

	def __init__(self, data):
		started = False
		parseLines = []
		for line in data.split('\n'):
			if tokenRe.match(line):
				if started:
					#print(parseLines)
					newToken = Token(thisToken, parseLines)
					self.tokens.append(newToken)
					parseLines = []
					newToken = None
				else:
					started = True
				thisToken = line
			elif parseRe.match(line):
				parseLines.append(line)

			else:
				print(line)
			#print(parseLines)

		first = True
		for token in self.tokens:
			if not first:
				self.sentence += " "
			self.sentence += token.token
			first = False
		self.sentence = "\"%s\"" % self.sentence

	def __repr__(self):
		return self.tokens
	
	def __str__(self):
		output = ""
		for token in self.tokens:
			output+=str(token)+"\n"
		output+= self.sentence+"\n"
		return output


class Token:
	global tokenRe
	global parseRe

	token = ""
	parses = []

	def __init__(self, token, parseLines):
		self.parses = []
		self.token = tokenRe.match(token).group(1)
		#print(self.token)
		#print("W", len(self.parses))
		#print(len(parseLines))
		for parse in parseLines:
			self.parses.append(Parse(parse))
		#print(self.parses)
	
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
	with open("testdata", "r") as datafile:
		testdata = datafile.read()
	sent = Sentence(testdata)
	print(sent)
