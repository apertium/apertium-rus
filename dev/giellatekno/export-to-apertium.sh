echo "[ А | Б | В | Г | Д | Е | Ё | Ж | З | И | Й | К | Л | М | Н | О | П | Р | С | Т | У | Ф | Х | Ц | Ч | Ш | Щ | Ъ | Ы | Ь | Э | Ю | Я | а | б | в | г | д | е | ё | ж | з | и | й | к | л | м | н | о | п | р | с | т | у | ф | х | ц | ч | ш | щ | ъ | ы | ь | э | ю | я | ¹ | ² | ³ | ⁻ | %- ]* %<n%> ?*" | hfst-regexp2fst -S -o /tmp/regex
hfst-compose-intersect -1 analyser-mt-apertium-desc.und.hfst -2 /tmp/regex | hfst-fst2strings > /tmp/russian-nouns
cat /tmp/russian-nouns | sed 's/<n><prop><sem_pat>/<np><pat>/g' | sed 's/<n><prop><sem_ant>/<np><ant>/g' |sed 's/<n><prop><cog>/<np><cog>/g' | sed 's/<n><prop><f>/<np><al><f>/g' | sed 's/<n><prop><m>/<np><al><m>/g' | sed 's/<n><prop>/<np>/g' > /tmp/russian-nouns.1
mv /tmp/russian-nouns.1 /tmp/russian-nouns
cat /tmp/russian-nouns | grep '<np>' > /tmp/russian-nouns-prop
cat /tmp/russian-nouns | grep '<n>' > /tmp/russian-nouns-common
cat /tmp/russian-nouns-common  | sed 's/+Err\/Sub/<use_sub>/g' | sed 's/<n><\(mfn\|nt\|m\|f\)><\(nn\|an\|aa\)>/; & ; /g'  | sed 's/:/ ; /g' | sed 's/></./g' | sed 's/[<>]//g' | awk -F';' '{print $2";"$1";"$4";"$3}' | sed 's/^  *//g' | sed 's/;/; /g' | sed 's/  */ /g' | awk -F';' '{print $1";"$4";"$2";"$3}' | LC_ALL=C sort -u | awk -F';' '{print $1";"$3";"$4";"$2}' > /tmp/russian-nouns-common.speling
cat /tmp/russian-nouns-common.speling | python3 speling-autodix-n.py > /tmp/russian-nouns-common.dix

echo "[ А | Б | В | Г | Д | Е | Ё | Ж | З | И | Й | К | Л | М | Н | О | П | Р | С | Т | У | Ф | Х | Ц | Ч | Ш | Щ | Ъ | Ы | Ь | Э | Ю | Я | а | б | в | г | д | е | ё | ж | з | и | й | к | л | м | н | о | п | р | с | т | у | ф | х | ц | ч | ш | щ | ъ | ы | ь | э | ю | я | ¹ | ² | ³ | ⁻ | %- ]* %<adj%> ?*" | hfst-regexp2fst -S -o /tmp/regex
hfst-compose-intersect -1 analyser-mt-apertium-desc.und.hfst -2 /tmp/regex | hfst-fst2strings > /tmp/russian-adjectives
cat /tmp/russian-adjectives | sed 's/<\(sg\|pl\)><\(gen\|prp\|dat\|ins\|nom\|loc\)>\(<fac>\|<prb>\|<use_sub>\|<err_sub>\)\?/<an>&/g' | sed 's/\(<nt>\|<f>\)\(<sg><acc>\)/\1<an>\2/g'  | sed 's/<nt><sg><pred>/<short><nt><sg>/g' | sed 's/<m><sg><pred>/<short><m><sg>/g' | sed 's/<f><sg><pred>/<short><f><sg>/g' | sed 's/<mfn><pl><pred>/<short><mfn><pl>/g' | sed 's/<comp><pred>/<comp>/g' > /tmp/russian-adjectives.1 
mv /tmp/russian-adjectives.1 /tmp/russian-adjectives
cat /tmp/russian-adjectives | sed 's/<adj>/; <adj> ; /g' | sed 's/:/; /g' | awk -F';' '{print $2"; "$1"; "$4"; "$3}' |  sed 's/></./g' | sed 's/[<>]//g' | LC_ALL=C sort -u  | sed 's/  */ /g' | sed 's/^ *//g' > /tmp/russian-adjectives.speling
cat /tmp/russian-adjectives.speling | python3 speling-autodix-adj.py > /tmp/russian-adjectives.dix
cat /tmp/russian-adjectives.dix | sed 's/<e r="LR">.*<s n="adj"\/>\(<s n="sint"\/>\)\?<s n="short"\/><s n="nt"\/><s n="sg"\/>.*/&\n        @@@&@@@/g' | sed 's/<s n="short"\/><s n="nt"\/><s n="sg"\/><\/r><\/p><\/e>@@@/<s n="cmp"\/><\/r><\/p><\/e>/g' | sed 's/@@@<e r="LR">/<e>/g' | sed 's/@@@<e>/<e>/g'  > /tmp/russian-adjectives.dix.1
mv /tmp/russian-adjectives.dix.1 /tmp/russian-adjectives.dix

echo "[ А | Б | В | Г | Д | Е | Ё | Ж | З | И | Й | К | Л | М | Н | О | П | Р | С | Т | У | Ф | Х | Ц | Ч | Ш | Щ | Ъ | Ы | Ь | Э | Ю | Я | а | б | в | г | д | е | ё | ж | з | и | й | к | л | м | н | о | п | р | с | т | у | ф | х | ц | ч | ш | щ | ъ | ы | ь | э | ю | я | ¹ | ² | ³ | ⁻ | %- ]* %<vblex%> ?*" | hfst-regexp2fst -S -o /tmp/regex
hfst-compose-intersect -1 analyser-mt-apertium-desc.und.hfst -2 /tmp/regex | hfst-fst2strings > /tmp/russian-verbs
