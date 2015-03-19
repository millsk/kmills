#!/bin/bash
#Calculate the norm of all files in ./iota/ directory

#For a properly normalized file, it should end up being 1.


echo "Below is the norm calculated for each file in iota/ and kappa/ directory.  This should be equal to 1 (or very close to it) for a properly normalized file."
echo "______________________________"
echo "   file              norm     "

for file in `ls iota/* `
do
   echo -n  "$file \t  "
   awk ' {sum+=($4*$4 + $5*$5)} END{print sum}' < $file #| tail -1 
done


echo "______________________________"


