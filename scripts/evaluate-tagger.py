import sys;

skipUnknown = True;
testFunc = False;

# ^власти/власть<n><f><nn><sg><dat><@P←>$	^власти/власть<n><f><nn><sg><gen>/власть<n><f><nn><sg><dat>/власть<n><f><nn><sg><prp>/власть<n><f><nn><pl><acc>/власть<n><f><nn><pl><nom>$	^власти/власть<n><f><nn><sg><dat>$

def readings(w): #{
	readings = [];
	reading = '';
	seen = False;
	for c in w: #{
		if c == '/' and seen == False: #{
			seen = True;
			continue;
		elif (c == '/' or c == '$') and seen: #{
			readings.append(reading);
			reading = '';
			continue;
		#}
		if seen: #{
			reading = reading + c;
		#}
	#}
	return readings;
#}

def reading_lemma(r): #{
	return r.split('<')[0];
#}

def reading_pos(r): #{
	return '<' + r.split('<')[1].split('>')[0] + '>';
#}

def reading_msd(r): #{
	msd = '';
	seen = False;
	for c in r: #{
		if c == '<': #{
			seen = True;
		#}
		if c == '@': #{
			seen = False;
			break;
		#}
		if seen: #{
			msd = msd + c;
		#}
	#}
	if msd[-1] == '<': #{
		msd = msd[0:-1];
	#}
	return msd;
#}

def reading_func(r): #{
	func = '';
	seen = False;
	for c in r: #{

		if c == '@': #{
			seen = True;
		#}
		if c == '>': #{
			seen = False;
		#}
		if seen: #{
			func = func + c;
		#}
	#}
	return '<' + func + '>';
#}

src_f = open(sys.argv[1]);
ref_f = open(sys.argv[2]);
tst_f = open(sys.argv[3]);

# Sanity check

src_l = len(src_f.readlines()); 
ref_l = len(src_f.readlines()); 
tst_l = len(src_f.readlines()); 

lines = -1; 

if src_l != ref_l != tst_l: #{
	print(src_l, ref_l, tst_l, file=sys.stderr);
else: #{
	lines = src_l;
#}

src_f.close();
ref_f.close();
tst_f.close();

src_f = open(sys.argv[1]);
ref_f = open(sys.argv[2]);
tst_f = open(sys.argv[3]);

n_unknown = 0;

n_ref_readings = 0;
n_src_readings = 0;
n_tst_readings = 0;

n_tst_lema_correct = 0;
n_tst_pos_correct = 0;
n_tst_lemapos_correct = 0;
n_tst_msd_correct = 0;
n_tst_lemamsd_correct = 0;
n_tst_func_correct = 0;

n_bas_lema_correct = 0;
n_bas_pos_correct = 0;
n_bas_lemapos_correct = 0;
n_bas_msd_correct = 0;
n_bas_lemamsd_correct = 0;
n_bas_func_correct = 0;

for line in range(0, lines): #{

	src_w = src_f.readline();
	ref_w = ref_f.readline();
	tst_w = tst_f.readline();

#	print(src_w);
#	print(ref_w);
#	print(tst_w);

	if src_w.count('¶') > 0: #{
		continue;
	#}

	tst_readings = [];
	tst_lema = '';
	tst_pos = '';
	tst_func = '';
	tst_msd = '';
	src_readings = [];
	src_lema = '';
	src_pos = '';
	src_func = '';
	src_msd = '';


	if tst_w.count('/*') < 1 and tst_w[0] == '^': #{
		tst_readings = readings(tst_w);
		tst_lema = reading_lemma(tst_readings[0]);
		tst_pos = reading_pos(tst_readings[0]);
		tst_func = reading_func(tst_readings[0]);
		tst_msd = reading_msd(tst_readings[0]);

		src_readings = readings(src_w);
		src_lema = reading_lemma(src_readings[0]);
		src_pos = reading_pos(src_readings[0]);
		src_func = reading_func(src_readings[0]);
		src_msd = reading_msd(src_readings[0]);

		n_src_readings = n_src_readings + len(src_readings);
		n_tst_readings = n_tst_readings + len(tst_readings);
	#}

	if tst_w.count('/*') > 0 and skipUnknown == True: #{
		print('-\t', tst_lema, tst_msd);
		n_unknown = n_unknown + 1;
		continue;	
	#}

	ref_readings = readings(ref_w);
	ref_lema = reading_lemma(ref_readings[0]);
	ref_pos = reading_pos(ref_readings[0]);
	ref_func = reading_func(ref_readings[0]);
	ref_msd = reading_msd(ref_readings[0]);

	n_ref_readings = n_ref_readings + 1;

	if tst_lema == ref_lema and tst_msd == ref_msd: #{
		print('=\t', tst_lema, tst_msd);
	else: #{
		print('ref:', ref_readings, file=sys.stderr);
		print('-\t', ref_lema, ref_msd);
		print('tst:', tst_readings, file=sys.stderr);
		print('+\t', tst_lema, tst_msd);
	#}
	
	if src_lema == ref_lema: n_bas_lema_correct = n_bas_lema_correct + 1;
	if src_lema == ref_lema and src_pos == ref_pos: n_bas_lemapos_correct = n_bas_lemapos_correct + 1;
	if src_lema == ref_lema and src_msd == ref_msd: n_bas_lemamsd_correct = n_bas_lemamsd_correct + 1;
	if src_pos == ref_pos: n_bas_pos_correct = n_bas_pos_correct + 1;
	if src_msd == ref_msd: n_bas_msd_correct = n_bas_msd_correct + 1;
	
	if tst_lema == ref_lema: n_tst_lema_correct = n_tst_lema_correct + 1;
	if tst_lema == ref_lema and tst_pos == ref_pos: n_tst_lemapos_correct = n_tst_lemapos_correct + 1;
	if tst_lema == ref_lema and tst_msd == ref_msd: n_tst_lemamsd_correct = n_tst_lemamsd_correct + 1;
	if tst_pos == ref_pos: n_tst_pos_correct = n_tst_pos_correct + 1;
	if tst_msd == ref_msd: n_tst_msd_correct = n_tst_msd_correct + 1;
	if tst_func == ref_func: n_tst_func_correct = n_tst_func_correct + 1;

	print("");
#}

# Accuracy = number of correct analyses / number of analyses in ref;


# Lemma accuracy
# POS accuracy
# MSD accuracy
# Func accuracy

print('unknown:\t', n_unknown,'(', (float(n_unknown)/float(n_ref_readings))*100.0,')');

print('src_ambig:\t', float(n_src_readings)/float(n_ref_readings));
print('tst_ambig:\t', float(n_tst_readings)/float(n_ref_readings));

print('');

p_bas_lema_correct = float(n_bas_lema_correct)/float(n_ref_readings)*100.0;
p_bas_pos_correct = float(n_bas_pos_correct)/float(n_ref_readings)*100.0;
p_bas_lemapos_correct = float(n_bas_lemapos_correct)/float(n_ref_readings)*100.0;
p_bas_msd_correct = float(n_bas_msd_correct)/float(n_ref_readings)*100.0;
p_bas_lemamsd_correct = float(n_bas_lemamsd_correct)/float(n_ref_readings)*100.0;
p_bas_func_correct = float(n_bas_func_correct)/float(n_ref_readings)*100.0;

print('lem:\t',p_bas_lema_correct);
print('pos:\t',p_bas_pos_correct);
print('lem+pos:\t',p_bas_lemapos_correct);
print('msd:\t',p_bas_msd_correct);
print('lem+msd:\t',p_bas_lemamsd_correct);
print('func:\t',p_bas_func_correct);

print('');

p_tst_lema_correct = float(n_tst_lema_correct)/float(n_ref_readings)*100.0;
p_tst_pos_correct = float(n_tst_pos_correct)/float(n_ref_readings)*100.0;
p_tst_lemapos_correct = float(n_tst_lemapos_correct)/float(n_ref_readings)*100.0;
p_tst_msd_correct = float(n_tst_msd_correct)/float(n_ref_readings)*100.0;
p_tst_lemamsd_correct = float(n_tst_lemamsd_correct)/float(n_ref_readings)*100.0;
p_tst_func_correct = float(n_tst_func_correct)/float(n_ref_readings)*100.0;

print('lem:\t',p_tst_lema_correct, '(', p_tst_lema_correct-p_bas_lema_correct, ')');
print('pos:\t',p_tst_pos_correct, '(', p_tst_pos_correct-p_bas_pos_correct, ')');
print('lem+pos:\t',p_tst_lemapos_correct, '(', p_tst_lemapos_correct-p_bas_lemapos_correct, ')');
print('msd:\t',p_tst_msd_correct, '(', p_tst_msd_correct-p_bas_msd_correct, ')');
print('lem+msd:\t',p_tst_lemamsd_correct, '(', p_tst_lemamsd_correct-p_bas_lemamsd_correct, ')');
print('func:\t',p_tst_func_correct, '(', p_tst_func_correct-p_bas_func_correct, ')');


