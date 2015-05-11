#!/usr/bin/env python3

import argparse, re
import xml.etree.ElementTree as ET

from lxml.html import fromstring, parse, etree

from subprocess import Popen, PIPE

import os

import cglib

stressMark = '`'
cacheDir = ""

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

def getRncWords(se, stress=False):
	global stressMark
	words = []
	for word in se.findall('.//w'):
		analyses = []
		token = ''.join(word.itertext())
		if not stress:
			token = re.sub(stressMark, "", token)
		anas = word.findall('ana')
		for ana in anas:
			lemma = ana.attrib['lex']
			tags = ana.attrib['gr']
			thisAna = {lemma: tags}
			analyses.append(thisAna)
		words.append({token: analyses})
	return words


def getRncSentences(corpus, stress=False):
	global stressMark
	for se in corpus.findall('.//se'):
		sentence = textContents(se, stress=stress)
		words = getRncWords(se, stress=stress)
		yield (sentence, words)


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
		yield output.decode()

def getCorpusCg(corpus, filename, stress=False, force=False):
	global cacheDir

	# get the cache directory
	dirname = os.path.dirname(filename)
	cacheDir = os.path.join(dirname, '.cache')
	if(not os.path.exists(cacheDir)):
		os.mkdir(cacheDir)
	
	# make the filename for the cg file
	(base, ext) = os.path.splitext(os.path.basename(filename))
	cgBase = base + '.cg'
	cgFn = os.path.join(cacheDir, cgBase)

	# if no cache file, or if being forced to recache, create and fill cache
	if (not os.path.exists(cgFn)) or force:
		with open(cgFn, 'w') as cgFile:
			for sentence in analyseCg(corpus, stress):
				cgFile.write(sentence)
	
	# return contents of cache file as Sentences object
	with open(cgFn, 'r') as cgFile:
		content = cgFile.read()
	return cglib.Sentences(content)
		


def compareRncCg(corpusRnc, corpusCg, stress=False):
	global cacheDir
	#print(corpusCg)

	for (sentenceRnc, sentenceCg) in zip(getRncSentences(corpusRnc, stress=stress), corpusCg.all()):
		#sentlen = len(sentenceCg)
		#print(len(sentenceCg), len(sentenceRnc[1]))
		#print(sentenceCg, sentenceRnc[1])
		cur = 0
		for token in sentenceCg.tokens:
			#if not token.tagInParses("sent") and not token.tagInParses("cm") and not token.tagInParses("quot") and not token.tagInParses("guio") and not token.tagInParses("lpar") and not token.tagInParses("rpar"):
			if not token.punctInParses():
				if cur >= len(sentenceRnc[1]):
					print("DRAGONS")
				else:
					#print(token.token, sentenceRnc[1][cur])
					if token.token in sentenceRnc[1][cur]:
						print(token.token)
				cur += 1
		

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='rnc 2 cg mangler')
	parser.add_argument('corpus', help="uri to a corpus file")
	parser.add_argument('-s', '--stress', help="preserve stress marks", action='store_true', default=False)
	parser.add_argument('-c', '--clean', help="print clean output", action='store_true', default=False)
	parser.add_argument('-g', '--cg', help="print raw corpus in CG format", action='store_true', default=False)
	parser.add_argument('-a', '--analyse', help="analyse all sentences with rusmorph.sh and cache the analyses", action='store_true', default=False)
	parser.add_argument('-f', '--force', help="force cached cg to be regenerated", action='store_true', default=False)

	args = parser.parse_args()

	corpus = parseRnc(args.corpus)

	if(args.clean):
		printRnc(corpus, stress=args.stress)
	elif(args.cg):
		printRncAsCg(corpus, stress=args.stress)
	elif(args.analyse):
		analyseCg(corpus, stress=args.stress)
	else:
		corpusCg = getCorpusCg(corpus, args.corpus, force=args.force, stress=args.stress)
		compareRncCg(corpus, corpusCg, stress=args.stress)

