#!/usr/bin/env python3

import argparse, re
import cglib
#from rnclib import parseRnc, getRncSentences
from collections import Counter, OrderedDict

def countFullyDisambiguatedSentences(corpus):
	#for tuple in getRncSentences(corpus):
	#	print(tuple)
	totalWords = 0
	totalWordsFullyDisambiguated = 0
	totalSents = 0
	totalSentsFullyDisambiguated = 0
	totalUnknownWords = 0
	listUnknownWords = []

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
					for analysis2 in form:
						if "@RNC" in analysis2.tags:
							listUnknownWords.append(analysis2.simple())
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
	toReturn = {
		"tot": {
			"disamwords": totalWordsFullyDisambiguated,
			"words": totalWords,
			"unk": totalUnknownWords,
			"disamsents": totalSentsFullyDisambiguated,
			"sents": totalSents,
		},
		"lists": {
			"unk": listUnknownWords
		}
	}
	return toReturn

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='analyse coverage of CG files')
	parser.add_argument('corpus', help="uri to a corpus file")
	parser.add_argument('-d', '--disambiguated', help="number of sentences and words completely disambiguated", action='store_true', default=False)
	parser.add_argument('-u', '--unanalysed', help="print out unanalysed forms", action='store_true', default=False)
	parser.add_argument('-a', '--ambiguous', help="print out forms with more than one RNC reading", action='store_true', default=False)
	parser.add_argument('-c', '--count', help="use with -a to just count the number of forms with more than one RNC reading", action='store_true', default=False)

	args = parser.parse_args()

	#corpus = parseRnc(args.corpus)

	with open(args.corpus, 'r') as cgFile:
		content = cgFile.read()
		#print(content)
	corpus = cglib.Sentences(content)

	if args.disambiguated:
		data = countFullyDisambiguatedSentences(corpus)
		print("Fully disambiguated words: {}/{} ({} unk)".format(data["tot"]["disamwords"], data["tot"]["words"], data["tot"]["unk"]))
		print("Fully disambiguated sentences: {}/{}".format(data["tot"]["disamsents"], data["tot"]["sents"]))

	if args.unanalysed:
		data = countFullyDisambiguatedSentences(corpus)
		counted = Counter(data["lists"]["unk"])
		ordered = OrderedDict(sorted(counted.items(), reverse=True, key=lambda t: t[1]))
		toPrint = "Unknown forms: "
		started = False
		#print(ordered)
		for form in ordered:
			if started:
				toPrint += ", "
			started = True
			toPrint += "{} ({})".format(form, counted[form])
		print(toPrint)
	
	if args.ambiguous:
		numAmbig = 0
		totalForms = 0
		for sentence in corpus:
			for form in sentence:
				RNC = 0
				totalForms += 1
				for analysis in form:
					if "@RNC" in analysis.tags:
						RNC += 1
				if RNC > 1:
					if not args.count:
						print(sentence.sentence)
						print(form)
						#print(' '.join(sentence.forms()))
					else:
						numAmbig += 1
		if args.count:
			print("{} of {} forms is RNC-ambiguous".format(numAmbig, totalForms))
		
