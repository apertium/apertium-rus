#!/usr/bin/env python3

import argparse, re
import xml.etree.ElementTree as ET

from lxml.html import fromstring, parse, etree

from subprocess import Popen, PIPE

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

def printRncAsCg(corpus, stress=False):
	global stressMark
	for word in corpus.findall('.//se/w'):
		wd = ''.join(word.itertext())
		if not stress:
			wd = re.sub(stressMark, "", wd)
		anas = word.findall('ana')
		if len(anas)==1:
			ana = anas[0].attrib
		else: print("FIXME: more than one analysis!!!  Keeping only first for the moment")
		#for ana in word.findall('ana'):
		#	print(ana.attrib)
		print(wd, ana)

def textContents(elem, stress=False):
	htmlTree = fromstring(ET.tostring(elem))
	output = re.sub('[\n \r]+', ' ', htmlTree.text_content()).strip()
	if not stress:
		output = re.sub(stressMark, "", output)

	return(output)

def getSentences(corpus, stress=False):
	global stressMark
	for se in corpus.findall('.//se'):
		sentence = textContents(se, stress=stress)
		yield sentence

def analyseCg(corpus, stress=False):
	for sentence in getSentences(corpus, stress=False):
		p1 = Popen(["echo", sentence], stdout=PIPE)
		p2 = Popen(["rusmorph.sh"], stdin=p1.stdout, stdout=PIPE)
		p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
		output = p2.communicate()[0]
		print(output.decode())

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='rnc 2 cg mangler')
	parser.add_argument('corpus', help="uri to a corpus file")
	parser.add_argument('-s', '--stress', help="preserve stress marks", action='store_true', default=False)
	parser.add_argument('-c', '--clean', help="print clean output", action='store_true', default=False)
	parser.add_argument('-g', '--cg', help="print raw corpus in CG format", action='store_true', default=False)
	parser.add_argument('-a', '--analyse', help="analyse all sentences with rusmorph.sh and cache the analyses", action='store_true', default=False)

	args = parser.parse_args()

	corpus = parseRnc(args.corpus)

	if(args.clean):
		printRnc(corpus, stress=args.stress)
	elif(args.cg):
		printRncAsCg(corpus, stress=args.stress)
	elif(args.analyse):
		analyseCg(corpus, stress=args.stress)

