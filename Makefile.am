###############################################################################
## Makefile for apertium-rus
###############################################################################

RELEASE=0.1
VERSION=0.1.0
LANG1=rus
BASENAME=apertium-$(LANG1)

TARGETS_COMMON = $(LANG1).automorf.bin $(LANG1).autogen.bin $(LANG1).autopgen.bin \
	$(LANG1).automorf.att.gz $(LANG2).autogen.att.gz \
        $(LANG1).rlx.bin

###############################################################################
## Russian transducer
###############################################################################

$(LANG1).autogen.bin: $(BASENAME).$(LANG1).dix
	if [ ! -d .deps ]; then mkdir .deps; fi
	apertium-validate-dictionary $<
	lt-comp rl $< $@ $(BASENAME).$(LANG1).acx

$(LANG1).automorf.bin: $(BASENAME).$(LANG1).dix
	if [ ! -d .deps ]; then mkdir .deps; fi
	xsltproc spellrelax.xsl apertium-rus.rus.dix > .deps/apertium-rus.rus.dix
	apertium-validate-dictionary .deps/apertium-rus.rus.dix
	lt-comp lr .deps/apertium-rus.rus.dix $@ $(BASENAME).$(LANG1).acx

$(LANG1).autopgen.bin: $(BASENAME).post-$(LANG1).dix
	lt-comp lr $< $@ 

$(LANG1).autogen.att.gz: $(LANG1).autogen.bin
	lt-print $< | gzip -9 -c > $@

$(LANG1).automorf.att.gz: $(LANG1).automorf.bin
	lt-print $< | gzip -9 -c > $@

###############################################################################
## Disambiguation rules 
###############################################################################

$(LANG1).rlx.bin: $(BASENAME).$(LANG1).rlx
	cg-comp $< $@

###############################################################################
## Distribution
###############################################################################
EXTRA_DIST=$(BASENAME).$(LANG1).dix \
	   $(BASENAME).post-$(LANG1).dix \
	   $(BASENAME).$(LANG1).acx \
	   $(BASENAME).$(LANG1).rlx \
	   $(LANG1).prob \
	   spellrelax.xsl \
	   modes.xml

###############################################################################
## Installation stuff
###############################################################################
#
#   apertium_rus_libdir: This is where the compiled binaries go
#   apertium_rus_srcdir: This is where the source files go

apertium_rusdir=$(prefix)/lib/apertium/$(BASENAME)/
apertium_rus_srcdir=$(prefix)/share/apertium/$(BASENAME)/

apertium_rus_DATA=$(LANG1).automorf.bin $(LANG1).autogen.bin $(LANG1).autopgen.bin \
		    $(LANG1).automorf.att.gz $(LANG1).autogen.att.gz \
		    $(LANG1).rlx.bin

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA = $(BASENAME).pc

# Modes are not installed since they're all just "debug modes". All
# modes are created by this goal.
modes/$(LANG1)-morph.mode: modes.xml
	apertium-validate-modes modes.xml
	apertium-gen-modes modes.xml

noinst_DATA=modes/$(LANG1)-morph.mode

install-data-local:
	test -d $(DESTDIR)$(apertium_rus_srcdir) || mkdir -p $(DESTDIR)$(apertium_rus_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).dix $(DESTDIR)$(apertium_rus_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).rlx $(DESTDIR)$(apertium_rus_srcdir)

CLEANFILES = $(TARGETS_COMMON)
clean-local:
	-rm -rf .deps modes
