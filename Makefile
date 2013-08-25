all:
	if [ ! -d .deps ]; then mkdir .deps; fi
	apertium-validate-dictionary apertium-rus.rus.dix
	lt-comp rl apertium-rus.rus.dix rus.autogen.bin apertium-rus.rus.acx
	xsltproc spellrelax.xsl apertium-rus.rus.dix > .deps/apertium-rus.rus.dix
	apertium-validate-dictionary .deps/apertium-rus.rus.dix
	lt-comp lr .deps/apertium-rus.rus.dix rus.automorf.bin apertium-rus.rus.acx
	lt-comp lr apertium-rus.post-rus.dix rus.autopgen.bin 

clean:
	rm -rf .deps/ rus.automorf.bin rus.autogen.bin
