#!/usr/bin/perl -w
use utf8 ;

while (<>)

{
s/а́/а/g ;
s/е́/е/g ;
s/и́/и/g ;
s/о́/о/g ;
s/у́/ы/g ;
s/я́/я/g ;
s/ё/е/g ;
s/ы́/ы/g ;
s/ю́/ю/g ;

print ;
}
