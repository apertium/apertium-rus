#!/usr/bin/env python3

import argparse, re
import cglib
#from rnclib import parseRnc, getRncSentences

def countFullyDisambiguatedSentences(corpus):
	#for tuple in getRncSentences(corpus):
	#	print(tuple)
	for sentence in corpus:
		for form in sentence:
			print(form)
			numRemainingAnalyses = 0
			for analysis in form:
				if not analysis.commented:
					if "*" not in analysis.lemma:
						numRemainingAnalyses += 1
			if numRemainingAnalyses == 1:
				fullDisam = True
			else:
				fullDisam = False
			print(fullDisam)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='analyse coverage of CG files')
	parser.add_argument('corpus', help="uri to a corpus file")
	parser.add_argument('-d', '--disambiguated', help="number of sentences and words completely disambiguated", action='store_true', default=False)

	args = parser.parse_args()

	#corpus = parseRnc(args.corpus)

	with open(args.corpus, 'r') as cgFile:
		content = cgFile.read()
		#print(content)
	corpus = cglib.Sentences(content)

	if args.disambiguated:
		countFullyDisambiguatedSentences(corpus)
