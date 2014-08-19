# Errors:
##         "представительный" adj sint comp


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
	#print('<!--shortest:',ilist);
	if not ilist: #{
		return -1;
	#}
	olist = [];
	for w in ilist: #{
		if len(w) > 0: #{
			olist.append(w);
		#}
	#}
	if not olist: #{
		return '';
	#}
	return sorted(olist, key=len)[0]
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

full_paradigms = {}; 
comp_paradigms = {}; 
shor_paradigms = {}; 

lexicon = {}; 
lefts = {};

# абажурный; абажурен; shor.m.sg; adj 
# абажурный; абажурна; shor.f.sg; adj 
# абажурный; абажурная; f.an.sg.nom; adj 
# абажурный; абажурнее; comp; adj 
# абажурный; абажурней; comp; adj 
# абажурный; абажурно; shor.nt.sg; adj 
# абажурный; абажурного; m.aa.sg.acc; adj 
# абажурный; абажурного; m.an.sg.gen; adj 
# абажурный; абажурного; nt.an.sg.gen; adj 
# абажурный; абажурное; nt.an.sg.acc; adj 
# абажурный; абажурное; nt.an.sg.nom; adj 


lemma = '';
categ = '';
forms = [];

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
		sint = '';
		full = []
		comp = []
		shor = []
		lcs = {};
		lcs['full'] = [];
		lcs['comp'] = [];
		lcs['shor'] = [];
		for j in forms: #{

			if j[0].count('comp') > 0: #{
				comp.append(j);	
				sint = 'sint';
			elif j[0].count('shor') > 0: #{
				shor.append(j);	
			else: #{
				full.append(j);
			#}
		#}
		#print('!\t', lemma, ':\t', full);
		if len(full) > 0: #{
			for j in forms: #{
				if j[0] == 'm.an.sg.nom': #{
					#print('FULL:\t', lemma, j[2]);
					lemma = j[2];
				#}
			#}
		elif len(full) < 1 and len(shor) > 0: #{
			for j in forms: #{
				if j[0] == 'short.m.sg': #{
					#print('SHORT:\t', lemma, j[2]);
					lemma = j[2];
				#}
			#}
		#}
		comp.sort();
		shor.sort();
		full.sort();
		for j in forms: #{
			if j[0].count('comp') > 0: #{
				lcs['comp'].append(longest_common_subsequence(lemma, j[2]));
			elif j[0].count('shor') > 0: #{
				lcs['shor'].append(longest_common_subsequence(lemma, j[2]));
			else: #{
				lcs['full'].append(longest_common_subsequence(lemma, j[2]));
			#}
		#}

		full_sig = '';			
		full_left = '';
		if len(lcs['full']) > 0: #{
			#print('lcs[full]:\t', lcs['full']);
			full_left = shortest(lcs['full']);
			replacer = re.compile('^' + full_left);
			for j in full: #{
				full_sig = full_sig + j[0] + ':' + re.sub(replacer, '', j[2]) + '%';	
			#}
		#}
		full_sig = full_sig.strip('%');

		comp_sig = '';			
		comp_left = '';
		if sint == 'sint': #{
			#print('lcs[comp]:\t', lcs['comp']);
			comp_left = shortest(lcs['comp']);
			replacer = re.compile('^' + comp_left);
			for j in comp: #{
				comp_sig = comp_sig + j[0] + ':' + re.sub(replacer, '', j[2]) + '%';	
			#}
		#}
		comp_sig = comp_sig.strip('%');

		shor_sig = '';			
		shor_left = '';
		if len(lcs['shor']) > 0: #{
			#print('lcs[shor]:\t', lcs['shor']);
			shor_left = shortest(lcs['shor']);
			replacer = re.compile('^' + shor_left);
			for j in shor: #{
				shor_sig = shor_sig + j[0] + ':' + re.sub(replacer, '', j[2]) + '%';	
			#}
		#}
		shor_sig = shor_sig.strip('%');

#		print(lemma,'|full:\t', full_sig);
#		print(lemma,'|shor:\t', shor_sig);
#		print(lemma,'|comp:\t', comp_sig);

		if full_sig not in full_paradigms: #{
			full_paradigms[full_sig] = [];
		#}
		full_paradigms[full_sig].append(lemma);
		if comp_sig not in comp_paradigms: #{
			comp_paradigms[comp_sig] = [];
		#}

		if shor_sig not in shor_paradigms: #{
			shor_paradigms[shor_sig] = [];
		#}


		lefts[lemma] = (full_left, comp_left, shor_left);
		true_left = shortest(lefts[lemma]);
		left = lefts[lemma][0].replace(true_left, '');	

		lexicon[lemma] = (full_sig, comp_sig, shor_sig, left);

		sig = '';
		forms = [];
		full = [];
		comp = [];
		shor = [];
		lemma = lem;
		categ = tag;

	elif lemma == '' and categ == '': #{
		lemma = lem;
		categ = tag;

	#}

	sur = row[1].strip();
	msd = row[2].strip();

	for i in tag.split('.'):
		symbols.add(i);
	for i in msd.split('.'):
		symbols.add(i);

	forms.append((msd, tag, sur));
#}

print(symbols, file=sys.stderr)
print(len(full_paradigms), file=sys.stderr);
print(len(comp_paradigms), file=sys.stderr);
print(len(shor_paradigms), file=sys.stderr);


paradigms = set();
assignment = {};
for lemma in lexicon: #{

	paradigms.add(lexicon[lemma]);
	if lexicon[lemma] not in assignment: #{
		assignment[lexicon[lemma]] = [];
	#}
	assignment[lexicon[lemma]].append(lemma);
	
#}

print('<dictionary>');
print('  <alphabet></alphabet>');
print('  <sdefs>');

for symbol in list(symbols): #{
	print('      <sdef n="' + symbol + '"   c=""/>');
#}

print('  </sdefs>');
print('  <pardefs>');


for pardef in full_paradigms: #{
	name = full_paradigms[pardef][0];
	if pardef.strip() == '': #{
		continue;
	#}
	print('      <pardef n="S__' + name + '">');
	for j in pardef.split('%'): #{
		if ':' in j: #{
			left = j.split(':')[1]
			right = j.split(':')[0];
			#print('        <e><p><l>%s</l><r>%s</r></p></e>' % (left, symbolise(right)));

			r = '';
			if right.count('.fac') or right.count('_sub') > 0 or right.count('.prb') > 0: #{
				r = 'LR';
				right = right.replace('.fac', '').replace('.use_sub','').replace('.err_sub','').replace('.prb','');
			#}
			if r != '': #{
				print('        <e r="%s"><p><l>%s</l><r>%s</r></p></e>' % (r, left, symbolise(right)));	
			else: #{
				print('        <e><p><l>%s</l><r>%s</r></p></e>' % (left, symbolise(right)));	
			#}
		#}
	#}
	print('      </pardef>');
#}

for pardef in paradigms: #{
	tag = 'adj';
	if ':' in pardef[1]: #{
		tag = 'adj.sint';
	#}
	full = full_paradigms[pardef[0]][0];
	name = assignment[pardef][0];
	print('      <pardef n="' + name + '__adj">');
#	true_left = shortest(lefts[name]);
#	left = lefts[name][0].replace(true_left, '');	
	if pardef[0].strip() != '': #{
		print('        <e><p><l>%s</l><r>%s</r></p><par n="S__%s"/></e>' % (pardef[3], symbolise(tag), full));
	#}
	if ':' in pardef[1]: #{
		for j in pardef[1].split('%'): #{
			left = j.split(':')[1];
			right = j.split(':')[0];
			r = '';
			if right.count('.fac') or right.count('_sub') > 0 or right.count('.prb') > 0: #{
				r = 'LR';
				right = right.replace('.fac', '').replace('.use_sub','').replace('.err_sub','').replace('.prb','');
			#}
			if r != '': #{
				print('        <e r="%s"><p><l>%s</l><r>%s%s</r></p></e>' % (r, left, symbolise(tag), symbolise(right)));	
			else: #{
				print('        <e><p><l>%s</l><r>%s%s</r></p></e>' % (left, symbolise(tag), symbolise(right)));	
			#}
		#}
	#}
	if ':' in pardef[2]: #{
		for j in pardef[2].split('%'): #{
			left = j.split(':')[1];
			right = j.split(':')[0];
			r = '';
			if right.count('.fac') or right.count('_sub') > 0 or right.count('.prb') > 0: #{
				r = 'LR';
				right = right.replace('.fac', '').replace('.use_sub','').replace('.err_sub','').replace('.prb','');
			#}
			if r != '': #{
				print('        <e r="%s"><p><l>%s</l><r>%s%s</r></p></e>' % (r, left, symbolise(tag), symbolise(right)));	
			else: #{
				print('        <e><p><l>%s</l><r>%s%s</r></p></e>' % (left, symbolise(tag), symbolise(right)));	
			#}
		#}
	#}
	print('      </pardef>');
#}

print('  </pardefs>');
print('  <section id="main" type="standard">');

words = list(lexicon.keys());
words.sort()
for lemma in words: #{
	left = shortest(lefts[lemma]);
	sig = lexicon[lemma];
	name = assignment[sig][0];
#	print('<!--',lemma,'|||',lefts[lemma],'|||','-->');
	print('    <e lm="%s"><p><l>%s</l><r>%s</r></p><par n="%s__adj"/></e>' % (lemma, left, lemma, name));
#}

print('  </section>');
print('</dictionary>');
