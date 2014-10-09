#!/bin/bash

# This script takes the POSCAR generated from the VMD nanotube builder
# and converts it to cartesian coordinates, shifts it in the x,y plane
# and then alternates the atom coordinates.


#CHANGE THESE
bond_length=1.89
atoms="Si   C"
shiftx=15
shifty=15
POSCAR="POSCAR"




lattx=`awk 'NR==3 {print $1}' $POSCAR`
latty=`awk 'NR==4 {print $2}' $POSCAR`
lattz=`awk 'NR==5 {print $3}' $POSCAR`
count=`awk 'NR==6 {print $1/2}' $POSCAR`





head -2 $POSCAR > head1.tmp

echo "" | awk -v bl=$bond_length -v l=$lattx '{print "  ",l*bl/1.42,  "     0.00000000   0.00000000"}' >> head1.tmp
echo "" | awk -v bl=$bond_length -v l=$latty '{print "   0.00000000  ",l*bl/1.42,  "   0.00000000"}' >> head1.tmp
echo "" | awk -v bl=$bond_length -v l=$lattz '{print "   0.00000000   0.00000000  " ,l*bl/1.42}' >> head1.tmp

echo " $atoms" >> head1.tmp
echo " $count   $count" >> head1.tmp
echo "Cartesian" >> head1.tmp

awk -v bl=$bond_length -v shiftx=$shiftx -v shifty=$shifty -v lattx=$lattx -v latty=$latty -v lattz=$lattz ' NR > 7 { print (($1*lattx)+shiftx)*bl/1.42,"   ",(($2*latty)+shifty)*bl/1.42,"    ",$3*lattz*bl/1.42 }' $POSCAR > tail.tmp



awk 'NR%2==0 {print $0}' tail.tmp > even.tmp
awk 'NR%2!=0 {print $0}' tail.tmp > odd.tmp


cat head1.tmp odd.tmp even.tmp > POSCAR_new


rm *.tmp






