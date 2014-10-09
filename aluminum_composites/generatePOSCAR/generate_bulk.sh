#!/bin/bash

python generateBulk.py

cat packmol-input.inp packmol_input_ending.temp > packmol-input.inp.temp

./packmol_exe < packmol-input.inp.temp  > /dev/null

awk 'NR>5 && $3=="O" {print $7"\t"$8"\t"$9}' < packmol-out.pdb > aluminums.list

awk ' ( ($1-15)**2 + ($2-15)**2 > (3.20)**2) {count+=1; print $0}' aluminums.list > aluminums.list2

count=`wc -l aluminums.list2 | awk '{print $1}'`

echo $count >> POSCAR_bulk
echo "Cartesian" >> POSCAR_bulk

cat POSCAR_bulk aluminums.list2 >  POSCAR_with_bulk


#rm packmol_input_ending.temp
#rm packmol-input.inp.temp
#rm packmol-out.pdb
