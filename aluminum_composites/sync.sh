#!/bin/sh

cd /home/kyle/Work/kmills/BoronNitrideAluminum/

rsync=' rsync -avz --ignore-errors --info=progress2 ' 

$rsync --exclude "OUTCAR" --exclude "DOSCAR" --exclude "OSZICAR" --exclude="WAVECAR" --exclude="CHG*" -L -e ssh kmills@fundy.ace-net.ca:/home/kmills/scratch/vasp3/BNAl/ . 

$rsync --exclude "OUTCAR" --exclude "DOSCAR" --exclude "OSZICAR" --exclude="CHG*" --exclude="WAVECAR" -L -e ssh kmills@mahone.ace-net.ca:/home/kmills/scratch/vasp3/BNAl/ .

$rsync --exclude "OUTCAR" --exclude "DOSCAR" --exclude "OSZICAR" --exclude "CHG*" --exclude="TMPCAR*" --exclude="WAVECAR" -L -e ssh kmills@orca.sharcnet.ca:/home/kmills/BNAl/ .
