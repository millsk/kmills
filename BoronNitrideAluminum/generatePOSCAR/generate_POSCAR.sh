#!/bin/bash

python generatePOSCAR.py

cat packmol-input.inp packmol_input_ending.temp > packmol-input.inp.temp

./packmol_exe < packmol-input.inp.temp  > /dev/null

awk 'NR>5 && $3=="O" {print $7"\t"$8"\t"$9}' < packmol-out.pdb > aluminums.list

cat POSCAR aluminums.list >  POSCAR_new

#rm POSCAR aluminums.list packmol-out.pdb

