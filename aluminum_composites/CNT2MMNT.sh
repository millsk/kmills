#!/bin/bash

# This script takes the POSCAR generated from the VMD nanotube builder
# and converts it to cartesian coordinates, shifts it in the x,y plane
# and then alternates the atom coordinates.


#CHANGE THESE
atoms="N   Al"
shiftx=15
shifty=15
POSCAR="POSCAR"

head -7 $POSCAR > head.tmp
head -5 head.tmp > head1.tmp
echo "$atoms" > head2.tmp
#tail -1 head.tmp > head3.tmp

cat head1.tmp head2.tmp > head.tmp
rm head?.tmp

lattx=`awk 'NR==3 {print $1}' $POSCAR`
latty=`awk 'NR==4 {print $2}' $POSCAR`
lattz=`awk 'NR==5 {print $3}' $POSCAR`
count=`awk 'NR==6 {print $1/2}' $POSCAR`

awk -v shiftx=$shiftx -v shifty=$shifty -v lattx=$lattx -v latty=$latty -v lattz=$lattz ' NR > 7 { print ($1*lattx)+shiftx,"   ",($2*latty)+shifty,"    ",$3*lattz }' $POSCAR > tail.tmp

awk 'NR%2==0 {print $0}' tail.tmp > even.tmp
awk 'NR%2!=0 {print $0}' tail.tmp > odd.tmp

echo "$count   $count"  > count.tmp
echo "Cartesian" >> count.tmp

cat head.tmp count.tmp odd.tmp even.tmp > POSCAR_new


rm *.tmp






