import sys, re;

def longest_common_subsequence(a,b): #{
	
	ab = ''
	
	for i in range(0, len(a)): #{
		if i < len(b): #{
			if a[i] == b[i]: #{
				ab = ab + a[i];
			else: #{
				break;
			#}
		else:
			break;
		#}
	#}

	return ab;
#}

def shortest(ilist): #{

	if not ilist: #{
		return -1;
	#}

	return sorted(ilist, key=len)[0]
#}

def symbolise(tags): #{

	s = '<s n="';
	for c in tags: #{
		if c == '.':
			s = s + '"/><s n="';
		else:
			s = s + c;
	#}
	s = s + '"/>';
	return s;
#}

###############################################################################

symbols = set();
paradigms = {}; 
lexicon = {}; 

#ангар; ангарами ; pl.ins; n.m.nn 
#ангар; ангарах ; pl.prp; n.m.nn 
#ангар; ангарам ; pl.dat; n.m.nn 

lemma = '';
categ = '';
forms = [];
lcs = [];
for line in sys.stdin.readlines(): #{
	if line.count(';') < 3: #{
		print('ERROR: malformed line', file=sys.stderr);
		print('>>>', file=sys.stderr);
		print(line, file=sys.stderr);
		break;
	#}

	row = line.strip().split(';');
	lem = row[0].strip();
	tag = row[3].strip();

	if lemma != '' and (lem != lemma) or (lem == lemma and tag != categ): #{
		#print(lemma,'\t', forms);
		forms.sort();
		sig = '';
		left = shortest(lcs);
		replacer = re.compile('^' + left);
		for j in forms: #{
			if j[1] != categ: #{
				print('ERROR: broken paradigm', file=sys.stderr);
				print('>>>', file=sys.stderr);
				print(forms);
			#}
			sig = sig + j[0] + ':' + re.sub(replacer, '', j[2]) + '%';
		#}
		#print(lemma,'\t', categ, left,  sig);

		if sig not in paradigms: #{
			paradigms[sig] = {};
		#}
		if categ not in paradigms[sig]: #{
			paradigms[sig][categ] = [];
		#}
		paradigms[sig][categ].append((lemma, left));

		if (categ, lemma) not in lexicon: #{
			lexicon[(categ, lemma, left)] = [];
		#}
		lexicon[(categ, lemma, left)].append(sig);

		forms = [];
		lcs = [];
		sig = '';
		lemma = lem;
		categ = tag;
	elif lemma == '' and categ == '': #{
		lemma = lem;
		categ = tag;
	#}

	sur = row[1].strip();
	msd = row[2].strip();

	lcs.append(longest_common_subsequence(lem, sur));

	for i in tag.split('.'):
		symbols.add(i);
	for i in msd.split('.'):
		symbols.add(i);

	forms.append((msd, tag, sur));
#}

print(symbols, file=sys.stderr)
print(len(paradigms), file=sys.stderr);


print('<dictionary>');
print('  <alphabet></alphabet>');
print('  <sdefs>');

for symbol in list(symbols): #{
	print('      <sdef n="' + symbol + '"   c=""/>');
#}

print('  </sdefs>');
print('  <pardefs>');

paradigm = '';

lookup = {};

for sig in paradigms: #{
	name = paradigms[sig][list(paradigms[sig].keys())[0]][0][0];
	print('      <pardef n="' + name + '">');
	for line in sig.strip('%').split('%'):
		row = line.split(':');
		left = row[1];
		right = row[0];
		r = ''
		if right.count('.fac') or right.count('_sub') > 0 or right.count('.prb') > 0: #{
			r = 'LR';
			right = right.replace('.fac', '').replace('.use_sub','').replace('.err_sub','').replace('.prb','');
		#}
		if r != '': #{
			print('        <e r="%s"><p><l>%s</l><r>%s</r></p></e>' % (r, left, symbolise(right)));	
		else: #{
			print('        <e><p><l>%s</l><r>%s</r></p></e>' % (left, symbolise(right)));	
		#}
	print('      </pardef>');
	for cat in paradigms[sig]: #{
		subname = paradigms[sig][cat][0][0];
		print('      <pardef n="' + subname + '__' + cat.replace('.', '_') + '">');
		print('        <e><p><l></l><r>%s</r></p><par n="%s"/></e>' % (symbolise(cat), name));
		print('      </pardef>');

		lookup[(sig, cat)] = subname + '__' + cat.replace('.', '_');
	#}
#}

print('  </pardefs>');
print('  <section id="main" type="standard">');

for sig in paradigms: #{
	for cat in paradigms[sig]: #{
		for pair in paradigms[sig][cat]: #{
			print('    <e lm="%s"><p><l>%s</l><r>%s</r></p><par n="%s"/></e>' % (pair[0], pair[1], pair[0], lookup[(sig, cat)]));
		#}
	#}
#}

print('  </section>');
print('</dictionary>');
