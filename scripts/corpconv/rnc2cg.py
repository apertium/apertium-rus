#!/usr/bin/env python3

import argparse, re
import xml.etree.ElementTree as etree

stressMark = '`'

def parseRnc(fn, stress=False):
	global stressMark
	with open(fn, 'r', encoding="windows-1251") as corpusFile:
		content = corpusFile.read()
	corpusTree = etree.fromstring(content)

	words = []
	for word in corpusTree.itertext():
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

	args = parser.parse_args()

	parseRnc(args.corpus, stress=args.stress)
