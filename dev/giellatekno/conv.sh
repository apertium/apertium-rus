RUS=/home/fran/source/giellatekno/langs/rus

pushd $RUS/tools/mt/apertium

make analyser-mt-apertium-desc.tmp.hfst
hfst-fst2txt analyser-mt-apertium-desc.tmp.hfst |\
  sed 's/а́/а/g' | sed 's/о́/о/g' |\
  sed 's/а̀/а/g' |  sed 's/ѐ/е/g' |  sed 's/ѝ/и/g' |  sed 's/о̀/о/g' |\
  sed 's/у̀/у/g' |  sed 's/ы̀/ы/g' |  sed 's/э̀/э/g' |  sed 's/ю̀/ю/g' |\
  sed 's/я̀/я/g' |  sed 's/ё̀/ё/g' |\
  sed 's/и́/и/g' | sed 's/у́/у/g' | sed 's/ю́/ю/g' | sed 's/ы́/ы/g' | sed 's/е́/е/g' |\
  sed 's/а́/а/g' | sed 's/о́/о/g' | sed 's/я́/я/g' | sed 's/э́/э/g' | sed 's/ //g' |\
  sed 's/<cs>/<cnjsub>/g' | sed 's/<cc>/<cnjcoo>/g' | sed 's/<sem_alt>/<al>/g' | sed 's/<sem_sur>/<cog>/g' |\
  sed 's/<pcle>/<part>/g' | sed 's/<inan>/<nn>/g' | sed 's/<anim>/<aa>/g' | sed 's/<indef>/<ind>/g' |\
  sed 's/<a>/<adj>/g' | sed 's/<interj>/<ij>/g' | sed 's/<neu>/<nt>/g' |\
  sed 's/<msc>/<m>/g' | sed 's/<fem>/<f>/g' | sed 's/<interr>/<itg>/g' |\
  sed 's/<pst>/<past>/g' | sed 's/<v>/<vblex>/g' | sed 's/<pstpss>/<pp><pasv>/g' |\
  sed 's/<prsact>/<pprs><actv>/g' | sed 's/<pobj>/<pprep>/g' |\
  sed 's/<prs>/<pres>/g' |\
  sed 's/<refl>/<ref>/g' |\
  sed 's/+Use\/Ant/<use_ant>/g' |\
  sed 's/<pron>/<prn>/g' | sed 's/<loc2>/<loc>/g' | sed 's/+Err\/Sub/<use_sub>/g' | sed 's/<loc>/<prp>/g' | sed 's/<cmpar>/<comp>/g' |\
  sed 's/<gen2>/<par>/g' | sed 's/+CLB/<sent>/g'  |\
 hfst-txt2fst | hfst-invert -o analyser-mt-apertium-desc.und.hfst

hfst-fst2fst -O analyser-mt-apertium-desc.und.hfst -o analyser-mt-apertium-desc.und.ohfst

popd

#  sed 's/<gen2>/<par>/g' | sed 's/+CLB/<sent>/g' | awk -F'\t' ' OFS="\t" {print $0; if($4 == "ё") { $4="е"; print $0; } }' |
