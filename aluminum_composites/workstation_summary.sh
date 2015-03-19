#!/bin/bash
user=kmills
remote_binary=/home/kmills/bin/vasp
remote_dir='~/BNAl/'

workstations="01 02 03 04 05 06 07 08 10 11 12 13 15 16 17 18"

   
if [[ "x"$1 == "xexplicit" ]]; then
   workstations="$2"
fi

for i in $workstations; do
   if [[ "x"$1 == "xremote" ]]; then
      ssh=" ssh -p 22$i $user@clean.science.uoit.ca "
   else
      ssh=" ssh $user@mcs$i "
   fi
   echo -e "\n
----------------------------------
 WORKSTATION mcs$i
----------------------------------"
   $ssh  '
   for pid in `pgrep vasp`; do
      echo "   "`pwdx $pid`
      path=`pwdx $pid | sed "s|$pid:||g"    `
   done

   cd $path
   echo "Completed timesteps: `grep pressure OUTCAR | wc -l`"
   echo "Contents of ~/BNAl are:"
   ls ~/BNAl/
   

   '


   if [[ "x"$1 == "xs" ]]; then
      mkdir -p "local_workstations/mcs$i"
      rsync -avz --ignore-errors --info=progress2 --exclude "*.tga" --exclude "*.ppm" --exclude "DOSCAR" --exclude "OSZICAR" --exclude="WAVECAR" --exclude="CHG*" -L -e ssh $user@mcs$i:/home/kmills/BNAl/ ./local_workstations/mcs$i
   fi




done







