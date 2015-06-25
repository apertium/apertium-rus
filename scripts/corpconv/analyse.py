#!/usr/bin/env python3

import argparse, re
import cglib
from rnclib import parseRnc

def countFullyDisambiguatedSentences(corpus):
	print(corpus)  #FIXME: write this function

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='analyse coverage of CG files')
	parser.add_argument('corpus', help="uri to a corpus file")
	parser.add_argument('-d', '--disambiguated', help="number of sentences and words completely disambiguated", action='store_true', default=False)

	args = parser.parse_args()

	corpus = parseRnc(args.corpus)

	if args.disambiguated:
		countFullyDisambiguatedSentences(corpus)
