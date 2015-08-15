#!/bin/bash

CORPUSDIR=~/q/ap/gt/ruscorpora_1M/texts

for testname in `cat tests.dat`; do
	filename=${testname}.xhtml
	echo $filename
	./rnc2cg.py -v 0 -m guess -i -o ${CORPUSDIR}/${filename}
	echo
done;

for i in *.filtered; do echo $i; ./analyse.py -d -u $i; echo""; done;
