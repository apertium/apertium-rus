#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import re
from lxml.html import fromstring, parse, etree


stressMark = '`'

def parseRnc(fn):
	global stressMark
	with open(fn, 'r', encoding="windows-1251") as corpusFile:
		content = corpusFile.read()
	corpusTree = ET.fromstring(content)

	return corpusTree

def textContents(elem, stress=False):
	htmlTree = fromstring(ET.tostring(elem))
	output = re.sub('[\n \r]+', ' ', htmlTree.text_content()).strip()
	if not stress:
		output = re.sub(stressMark, "", output)

	return(output)

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
