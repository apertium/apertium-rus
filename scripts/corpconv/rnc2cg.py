#!/usr/bin/env python3

import argparse, re
import xml.etree.ElementTree as ET

stressMark = '`'

def parseRnc(fn):
	global stressMark
	with open(fn, 'r', encoding="windows-1251") as corpusFile:
		content = corpusFile.read()
	corpusTree = ET.fromstring(content)

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

def printRncAsCg(corpus):
	for word in corpus.findall('.//se/w'):
		wd = ''.join(word.itertext())
		anas = word.findall('ana')
		if len(anas)==1:
			ana = anas[0].attrib
		else: print("WARNING: more than one analysis!!!  Keeping only first for the moment")
		#for ana in word.findall('ana'):
		#	print(ana.attrib)
		print(wd, ana)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='rnc 2 cg mangler')
	parser.add_argument('corpus', help="uri to a corpus file")
	parser.add_argument('-s', '--stress', help="preserve stress marks", action='store_true', default=False)
	parser.add_argument('-c', '--clean', help="print clean output", action='store_true', default=False)
	parser.add_argument('-g', '--cg', help="print raw corpus in CG format", action='store_true', default=False)

	args = parser.parse_args()

	corpus = parseRnc(args.corpus)

	if(args.clean):
		printRnc(corpus, stress=args.stress)
	elif(args.cg):
		printRncAsCg(corpus)
