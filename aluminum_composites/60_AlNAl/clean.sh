#!/bin/bash

mkdir protect

for file in clean.sh POSCAR POTCAR KPOINTS vasp.s INCAR plot*
do
   mv $file protect
done
rm *
mv protect/* .
rmdir protect
clear
