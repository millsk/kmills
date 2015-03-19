#!/bin/bash


rm  LOCPOT* WAVECAR* C/* O/* CO/*

for dir in Li H LiH; do
   rm -r ${dir}
   for file in WAVECAR LOCPOT; do
      scp kmills@fundy.ace-net.ca:~/scratch/vasp3/lithiumhydride/${dir}/${file} ${file}_$dir 
   done

a="$dir"

 mkdir -p ${a}
 echo ${a}
 cp WAVECAR_$a WAVECAR &&
 ../WaveTrans2 &&
 mv GCOEFF* $a/ &&
 mv ENERGIES.txt ${a}/E_${a}.txt &&
 cd ${a} &&
 rename "s.GCOEFF.${a}.g" * &&
 cd ..
 
 done

