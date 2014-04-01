DATE=`date`
TOKENS=`cat $1 | grep '\/' | wc -l`
UNKNOWN=`cat $1 | grep '\*' | wc -l`;
ANALYSES=`cat $1 | grep '\/' | cut -f2- -d'/' | sed 's/\//\n/g' | wc -l`
FUNCTAGS=`cat $1 | grep '@' | wc -l`;
FUNCCOV=`echo \($FUNCTAGS/$TOKENS\)\*100 | bc -l | sed 's/\(\.[0-9][0-9]\)\(.*\)/\1/g'`;
COVERAGE=`echo \(\($TOKENS-$UNKNOWN\)/$TOKENS\)\*100 | bc -l | sed 's/\(\.[0-9][0-9]\)\(.*\)/\1/g'`;
AMBIG=`echo $ANALYSES/$TOKENS | bc -l |  sed 's/\(\.[0-9][0-9]\)\(.*\)/\1/g'`;
echo -e "$DATE\t$1\t$TOKENS\t$UNKNOWN\t$COVERAGE\t$ANALYSES\t$AMBIG\t$FUNCTAGS\t$FUNCCOV" 
