#!/bin/bash

mkdir protect

for file in clean.sh POSCAR POTCAR KPOINTS vasp.s INCAR plot* vdw_kernel.bindat
do
   mv $file protect
done
rm *
mv protect/* .
rmdir protect
clear
