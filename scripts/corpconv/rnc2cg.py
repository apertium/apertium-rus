#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as etree

def parseRnc(fn):
	with open(fn, 'r', encoding="windows-1251") as corpusFile:
		content = corpusFile.read()
	corpusTree = etree.fromstring(content)

	words = []
	for word in corpusTree.itertext():
		if word.strip()!='':
			words.append(word.strip())

	#print(words)
	print(' '.join(words))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='rnc 2 cg mangler')
	parser.add_argument('corpus', help="uri to a corpus file")
	args = parser.parse_args()

	parseRnc(args.corpus)
