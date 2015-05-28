#!/usr/bin/env python3

import re

tokenRe = re.compile("^\"<(.*?)>\"$")
parseRe = re.compile("^(;?).*\"(.*?)\" (.*)$")
nullParseRe = re.compile("^(;?).*\"\*(.*?)\"$")

class Sentences:
	sentences = []

	def __init__(self, data):
		for sentenceData in data.split('\n\n'):
			newSentence = None
			newSentence = Sentence(sentenceData)
			self.sentences.append(newSentence)
			#print(len(self.sentences))
	
	def __repr__(self):
		return self.sentences
	
	def __str__(self):
		for sentence in self.sentences:
			print(str(sentence))
	
	#def len(self):
	#	return len(self.sentences)

	def all(self):
		for sentence in self.sentences:
			yield sentence

	def __len__(self):
		return len(self.sentences)

class Sentence:
	global tokenRe
	global parseRe
	tokens = []
	sentence = ""

	def __init__(self, data):
		self.tokens = []
		started = False
		parseLines = []
		for line in data.split('\n'):
			if tokenRe.match(line):
				#print(len(self.tokens))
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
			elif nullParseRe.match(line):
				parseLines.append(line)
			else:
				if line != "":
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
		return repr(self.tokens)
	
	def __str__(self):
		output = ""
		for token in self.tokens:
			output+=str(token)#+"\n"
		#output+= self.sentence+"\n"
		return output

	def __len__(self):
		#print(self.tokens[1])
		#print(self.__repr__())
		#for token in self.tokens:
		#	print(repr(token))
		#print("=========", len(self.tokens))
		return len(self.tokens)

class Token:
	global tokenRe
	global parseRe
	global nullParseRe

	punctuation = ["sent", "cm", "quot", "guio", "lpar", "rpar"]

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
		return repr({self.token: repr(self.parses)})
	
	def __str__(self):
		output = "\"<{}>\"\n".format(self.token)
		for parse in self.parses:
			output += str(parse)+"\n"
		return output
	
	def punctInParses(self):
		for punct in self.punctuation:
			if self.tagInParses(punct):
				return True
		return False

	def tagInParses(self, tag):
		for parse in self.parses:
			if parse.tags is not None:
				if tag in parse.tags:
					return True
		return False

class Parse:
	global tokenRe
	global parseRe
	global nullParseRe

	lemma = ""
	tags = []
	decisions = []
	commented = False

	def __init__(self, line):
		self.decisions = []
		#print(line)
		if parseRe.match(line):
			(commented, self.lemma, tags) = parseRe.match(line).groups()
			if commented != "": self.commented = True
			#print(self.commented)
			self.tags = tags.split()
		elif nullParseRe.match(line):
			self.lemma = None
			self.tags = None

	def __repr__(self):
		return repr({self.lemma: self.tags})

	def __str__(self):
		if self.lemma != None:
			tagOutput = ""
			First = True
			for tag in self.tags:
				if not First:
					tagOutput += " "
				tagOutput += tag
				First = False
			comment = ";" if self.commented else " "
			rules = ' '.join(self.decisions)
			template = "{}       \"{}\" {} {}"
			return template.format(comment, self.lemma, tagOutput, rules)

		else:
			return ""

	def comment(self, rule=None):
		self.commented = True
		if rule is not None:
			self.decisions.append(rule)
	
	def uncomment(self):
		self.commented = False
		self.decisions = []
	
	def addDecision(self, rule):
		self.decisions.append(rule)

	def isSelected(self):
		for decision in self.decisions:
			if "SELECT" in decision:
				return True
		return False


if __name__ == '__main__':
	with open("testdata", "r") as datafile:
		testdata = datafile.read()
	sent = Sentence(testdata)
	#print(sent)
	#print(sent.tokens[0].parses[0])
