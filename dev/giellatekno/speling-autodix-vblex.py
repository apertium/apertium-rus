import sys, re;

# What is this script for:
# 
# The idea of this script is to create a Russian verb lexicon from 
# a full-form list. The lexicon should attempt to avoid duplication
# of paradigms as much as possible by reusing paradigm fragments.
#
# How this script is supposed to work:
#
# 1) We take a full form list and work out all the combinations of suffixes
#    for a given tense/mood/participle, e.g. find all the suffixes for 
#    present tense. 
#
# .) We find the shortest longest common subsequence for the <l> part of the 
#    entry.
#
# .) We group these combinations of suffixes into paradigms, which we will
#    use as building blocks to make the main paradigms.
# 
# .) We print out all the individual paradigms for the combinations, and then
#    the paradigms for the groups of combinations (the actual paradigms).
#
# .) Finally we print out the lexicon entries, attaching a main paradigm to 
#    each one.
#
# Simplified xample:
#
# любить; люби; imp.p2.sg; vblex.impf.iv 
# любить; любил; past.m.sg; vblex.impf.iv 
# любить; любила; past.f.sg; vblex.impf.iv 
# любить; любили; past.mfn.pl; vblex.impf.iv 
# любить; любило; past.nt.sg; vblex.impf.iv 
# любить; любим; pres.p1.pl; vblex.impf.iv 
# любить; любит; pres.p3.sg; vblex.impf.iv 
# любить; любите; imp.p2.pl; vblex.impf.iv 
# любить; любите; pres.p2.pl; vblex.impf.iv 
# любить; любить; inf; vblex.impf.iv 
# любить; любишь; pres.p2.sg; vblex.impf.iv 
# любить; люблю; pres.p1.sg; vblex.impf.iv 
# любить; любят; pres.p3.pl; vblex.impf.iv 
# терпеть; терпел; past.m.sg; vblex.impf.iv 
# терпеть; терпела; past.f.sg; vblex.impf.iv 
# терпеть; терпели; past.mfn.pl; vblex.impf.iv 
# терпеть; терпело; past.nt.sg; vblex.impf.iv 
# терпеть; терпеть; inf; vblex.impf.iv 
# терпеть; терпи; imp.p2.sg; vblex.impf.iv 
# терпеть; терпим; pres.p1.pl; vblex.impf.iv 
# терпеть; терпит; pres.p3.sg; vblex.impf.iv 
# терпеть; терпите; imp.p2.pl; vblex.impf.iv 
# терпеть; терпите; pres.p2.pl; vblex.impf.iv 
# терпеть; терпишь; pres.p2.sg; vblex.impf.iv 
# терпеть; терплю; pres.p1.sg; vblex.impf.iv 
# терпеть; терпят; pres.p3.pl; vblex.impf.iv 
#
# We create the sub-paradigms:
# 
# lemma   stem    sub-paradigm:
# -----------------------------------------------------------------------------
# любить   любить   (inf:)
# любить   люб      (imp.p2.sg:и, imp.p2.pl:ите)
# любить   люби     (past.m.sg:л, past.f.sg:ла, past.nt.sg:ло, past.mfn.pl:ли)
# любить   люб      (pres.p1.sg:лю, pres.p2.sg:ишь, pres.p3.sg:ит, pres.p1.pl:им, pres.p2.pl:ите, pres.p3.pl:ят)
# терпеть  терпеть  (inf:)
# терпеть  терп     (imp.p2.sg:и, imp.p2.pl:ите)
# терпеть  терпе    (past.m.sg:л, past.f.sg:ла, past.nt.sg:ло, past.mfn.pl:ли)
# терпеть  терп     (pres.p1.sg:лю, pres.p2.sg:ишь, pres.p3.sg:ит, pres.p1.pl:им, pres.p2.pl:ите, pres.p3.pl:ят)
# говорить говорить (inf:)
# говорить говор      (imp.p2.sg:и, imp.p2.pl:ите)
# говорить говори     (past.m.sg:л, past.f.sg:ла, past.nt.sg:ло, past.mfn.pl:ли)
# говорить говор      (pres.p1.sg:ю, pres.p2.sg:ишь, pres.p3.sg:ит, pres.p1.pl:им, pres.p2.pl:ите, pres.p3.pl:ят)
#
# The shortest stem is taken for the 'root' (the part that will come in <l>):
#
# (терпеть, терп, vblex.impf.iv)
# (любить, люб, vblex.impf.iv)
# 
# For each of the items we make a paradigm by combining the sub-paradigms with 
# the difference between the stem for that paradigm and the shortest stem:
#
# par1: (imp.p2.sg:и, imp.p2.pl:ите)
# par2: (past.m.sg:л, past.f.sg:ла, past.nt.sg:ло, past.mfn.pl:ли)
# par3: (pres.p1.sg:лю, pres.p2.sg:ишь, pres.p3.sg:ит, pres.p1.pl:им, pres.p2.pl:ите, pres.p3.pl:ят)
# par4: (pres.p1.sg:ю, pres.p2.sg:ишь, pres.p3.sg:ит, pres.p1.pl:им, pres.p2.pl:ите, pres.p3.pl:ят)
#
# любить   = ø + par1
#            и + par2
#            ø + par3
# 
# терпеть  = ø + par1
#            е + par2 
#            ø + par3
#
# говорить = ø + par1
#            и + par2
#            ø + par4
# 
# The point of all this is to economise lines, if we were to make 
# full-form paradigms for all words in this example we would end up 
# with 39 lines. By compressing the paradigms this way we end up with
# only 30 lines. The more paradigms we add, the more we compress.

###############################################################################

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

lexicon = {};  # lexicon[('аблактировать', 'vblex.impf.iv')]['pres+fut'] = [];

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
		if (lemma, categ) not in lexicon: #{
			lexicon[lemma, categ] = {};
		#}
		forms.sort();
#		print(lemma,'\t', forms);

		for j in forms: #{
			if j[0].count('pres') > 0 or j[0].count('fut') > 0: #{
				if 'pres+fut' not in lexicon[(lemma, categ)]: #{
					lexicon[(lemma, categ)]['pres+fut'] = [];
				#}
				lexicon[(lemma, categ)]['pres+fut'].append((j[0], j[2]));
			#}
			if j[0].count('past') > 0: #{
				if 'past' not in lexicon[(lemma, categ)]: #{
					lexicon[(lemma, categ)]['past'] = [];
				#}
				lexicon[(lemma, categ)]['past'].append((j[0], j[2]));
			#}
			if j[0].count('imp') > 0: #{
				if 'imp' not in lexicon[(lemma, categ)]: #{
					lexicon[(lemma, categ)]['imp'] = [];
				#}
				lexicon[(lemma, categ)]['imp'].append((j[0], j[2]));
			#}
			if j[0].count('inf') > 0: #{
				if 'inf' not in lexicon[(lemma, categ)]: #{
					lexicon[(lemma, categ)]['inf'] = [];
				#}
				lexicon[(lemma, categ)]['inf'].append((j[0], j[2]));
			#}
			if j[0].count('adv') > 0: #{
				if 'adv' not in lexicon[(lemma, categ)]: #{
					lexicon[(lemma, categ)]['adv'] = [];
				#}
				lexicon[(lemma, categ)]['adv'].append((j[0], j[2]));
			#}



		#}
		# pprs.actv
		# pp.actv
		# pprs.pasv
		# pp.pasv
		# pprs.adv
		# pp.adv
		# past
		# pres
		# inf
		# imp 
		# fut 
		# ся-type

		sig = '';
		forms = [];
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

print('<dictionary>')
print('  <alphabet></alphabet>');
print('  <sdefs>');
for sym in list(symbols): #{
	print('    <sdef n="%s"/>' % (sym));
#}
print('  </sdefs>');

paradigms = set();
lefts = {}; # lefts[(аблактировать, vblex.impf.iv)] = ['', '', '', '', ...];
broken = 0;
total = 0;
new_lexicon = {};
#       left, inf, pres+fut, past, imp, adv, pprs.actv, pprs.pasv, pp.actv, pp.pasv)
idx = {'left': 0, 'inf': 1, 'pres+fut': 2, 'past': 3, 'imp': 4, 'adv': 5};

for pair in lexicon: #{
	if len(lexicon[pair].keys()) < 4: #{
		print('ERROR: broken lexicon entry:', pair, file=sys.stderr);
		print('>', file=sys.stderr);
		print(lexicon[pair], file=sys.stderr);
		broken = broken + 1;
		continue;
	#}
	#               left, inf, pres+fut, past, imp, adv, pprs.actv, pprs.pasv, pp.actv, pp.pasv)
	new_paradigm = ['', '', '', '', '', '', '', '', '', ''];
	new_lefts =    ['', '', '', '', '', '', '', '', '', ''];
	for sub in ['inf', 'pres+fut', 'past', 'imp', 'adv']: #{
		if sub not in lexicon[pair]: #{
			new_paradigm[idx[sub]] = '';
			continue;
		#}
		lexicon[pair][sub].sort();
#		print(pair, sub, lexicon[pair][sub]);
		local_lefts = [];
		sig = '';
		for j in lexicon[pair][sub]: #{
			local_lefts.append(longest_common_subsequence(pair[0], j[1]));
		#}
		local_left = shortest(local_lefts);
		replacer = re.compile('^' + local_left);
		for j in lexicon[pair][sub]: #{
			sig = sig + j[0] + ':' + re.sub(replacer, '', j[1]) + '%';	
		#}
		sig = sig.strip('%');
		new_paradigm[idx[sub]] = sig;
		new_lefts[idx[sub]] = local_left;
	#}
	shortest_left = shortest(new_lefts);
	replacer = re.compile('^' + shortest_left);
	for sub in ['inf', 'pres+fut', 'past', 'imp', 'adv']: #{
		if new_paradigm[idx[sub]] == '': #{
			continue;
		#}
		new_lefts[idx[sub]] = re.sub(replacer, '', new_lefts[idx[sub]]);
	#}
	lefts[pair] = new_lefts;
	full_paradigm = '|'.join(new_paradigm);
	paradigms.add(full_paradigm);
	#print(new_paradigm);
	if full_paradigm not in new_lexicon: #{
		new_lexicon[full_paradigm] = [];
	#}
	new_lexicon[full_paradigm].append((pair[0], pair[1], shortest_left));
	total = total + 1;
#}



print('<pardefs>');

total_paradigms = 0;
sub_paradigms = {'pres+fut': [], 'past': [], 'imp': [], 'adv': []};
for sub in ['pres+fut', 'past', 'imp', 'adv']: #{

	for paradigm in paradigms: #{

		row = paradigm.split('|');
		if row[idx[sub]] in sub_paradigms[sub]: #{
			continue;
		else: #{
			sub_paradigms[sub].append(row[idx[sub]]);	
		#}
		if row[idx[sub]] == '': #{
			continue;
		#}
		print('    <pardef n="%s">' % (row[idx[sub]]));
		for entry in row[idx[sub]].split('%'): #{
			if ':' not in entry: #{
				print('ERROR:', paradigm, file=sys.stderr);
				print(sub, entry, file=sys.stderr);
				continue;
			#}
			l = entry.split(':')[1];
			r = entry.split(':')[0];
			if r.count('use_obs') > 0: #{
				etype = '<e r="LR">';
				r = r.replace('.use_obs', '');
			elif r.count('prb') > 0: #{
				etype = '<e r="RL">';
				r = r.replace('.prb', '');
			else: #{
				etype = '<e>';
			#}
			print('      %s<p><l>%s</l><r>%s</r></p></e>' % (etype, l, symbolise(r))); 
		#}
		print('    </pardef>');
		total_paradigms = total_paradigms + 1;
	#}
#}

all_paradigms = {};

lookup = {};

for paradigm in new_lexicon: #{

	for entry in new_lexicon[paradigm]: #{
		infinitiviser = re.compile('^' + entry[2]);
		infin = re.sub(infinitiviser, '', entry[0]);
		sig = 'inf:' + infin + '!';
		for part in ['pres+fut', 'past', 'imp']: #{
			sig = sig + lefts[(entry[0], entry[1])][2] + '!' + paradigm.split('|')[2];
		#}
		if sig in all_paradigms: #{
			lookup[entry] = all_paradigms[sig];
			continue;
		else: #{
			all_paradigms[sig] = entry[0].replace(entry[2], entry[2] + '/');
		#}
		print('    <pardef n="%s">' % (all_paradigms[sig]));
		print('      <e><p><l>%s</l><r>%s<s n="inf"/></r></p></e>' % (infin, ''));
		print('      <e><p><l>%s</l><r>%s</r></p><par n="%s"/></e>' % (lefts[(entry[0], entry[1])][2], '', paradigm.split('|')[2]));
		print('      <e><p><l>%s</l><r>%s</r></p><par n="%s"/></e>' % (lefts[(entry[0], entry[1])][3], '', paradigm.split('|')[3]));
		if paradigm.split('|')[4] != '': #{
			print('      <e><p><l>%s</l><r>%s</r></p><par n="%s"/></e>' % (lefts[(entry[0], entry[1])][4], '', paradigm.split('|')[4]));
		#}
		if paradigm.split('|')[5] != '': #{
			print('      <e><p><l>%s</l><r>%s</r></p><par n="%s"/></e>' % (lefts[(entry[0], entry[1])][5], '', paradigm.split('|')[5]));
		print('    </pardef>');
		total_paradigms = total_paradigms + 1;
	#}
#}

print('  </pardefs>');
print('  <section id="main" type="standard">');
for paradigm in new_lexicon: #{

	for entry in new_lexicon[paradigm]: #{
		if entry not in lookup: #{
			print('ERROR:', entry, file=sys.stderr);
			continue;
		#}
		print('    <e lm="%s"><p><l>%s</l><r>%s</r></p><par n="%s"/></e>' % (entry[0], entry[2], entry[0]+symbolise(entry[1]), lookup[entry]));
	#}
#}
print('  </section>');
print('</dictionary>');
print('<!--');
print(len(paradigms));
print(len(new_lexicon));
print(len(lefts));
print(broken, total);
print(total_paradigms);
print('-->');
