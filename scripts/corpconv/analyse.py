#!/usr/bin/env python3

import argparse, re
import cglib
#from rnclib import parseRnc, getRncSentences

def countFullyDisambiguatedSentences(corpus):
	#for tuple in getRncSentences(corpus):
	#	print(tuple)
	totalWords = 0
	totalWordsFullyDisambiguated = 0
	totalSents = 0
	totalSentsFullyDisambiguated = 0
	totalUnknownWords = 0

	for sentence in corpus:
		thisSentNumWords = 0
		thisSentFullyDisambiguatedWords = 0
		thisSentUnanalysedWords = 0
		for form in sentence:
			#print(form)
			numRemainingAnalyses = 0
			numUnanalysedWords = 0
			totalNumAnalyses = 0
			for analysis in form:
				if "*" not in analysis.lemma:
					if not analysis.commented:
						numRemainingAnalyses += 1
					if "@RNC" not in analysis.tags:
						totalNumAnalyses += 1
				else:
					numUnanalysedWords += 1
					totalUnknownWords += 1
			if numRemainingAnalyses == 1:
				fullDisam = True
				thisSentFullyDisambiguatedWords += 1
				totalWordsFullyDisambiguated += 1
			else:
				fullDisam = False
			#print(fullDisam, numUnanalysedWords, numRemainingAnalyses, totalNumAnalyses)
			totalWords += 1
			thisSentNumWords += 1
			thisSentUnanalysedWords += numUnanalysedWords
		#print(sentence, "***********")
		#print(thisSentNumWords, thisSentFullyDisambiguatedWords, thisSentUnanalysedWords)
		totalSents += 1
		if thisSentNumWords == thisSentFullyDisambiguatedWords:
			totalSentsFullyDisambiguated += 1
	print("Fully disambiguated words: {}/{} ({} unk)".format(totalWordsFullyDisambiguated, totalWords, totalUnknownWords))
	print("Fully disambiguated sentences: {}/{}".format(totalSentsFullyDisambiguated, totalSents))

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
