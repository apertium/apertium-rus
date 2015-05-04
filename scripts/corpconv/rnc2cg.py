#!/usr/bin/env python3

import argparse, re
import xml.etree.ElementTree as etree

stressMark = '`'

def parseRnc(fn):
	global stressMark
	with open(fn, 'r', encoding="windows-1251") as corpusFile:
		content = corpusFile.read()
	corpusTree = etree.fromstring(content)

	return corpusTree

def printRnc(corpus, stress=False):
	words = []
	for word in corpus.itertext():
		if word.strip()!='':
			if not stress:
				word = re.sub(stressMark, "", word)
			words.append(word.strip())

	#print(words)
	print(' '.join(words))



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='rnc 2 cg mangler')
	parser.add_argument('corpus', help="uri to a corpus file")
	parser.add_argument('-s', '--stress', help="preserve stress marks", action='store_true', default=False)
	parser.add_argument('-c', '--clean', help="print clean output", action='store_true', default=False)

	args = parser.parse_args()

	corpus = parseRnc(args.corpus)

	if(args.clean):
		printRnc(corpus, stress=args.stress)

