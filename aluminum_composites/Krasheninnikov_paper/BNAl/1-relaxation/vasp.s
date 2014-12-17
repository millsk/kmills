#!/bin/bash
#PBS -l walltime=72:00:00
#PBS -l pmem=8000mb
#PBS -r n
#PBS -l procs=4
#PBS -M kyle.mills@uoit.net

#PBS -N "BNAl(111)_rel"

cd $PBS_O_WORKDIR
echo -n "START " > datefile
date >> datefile

touch WAVECAR
touch CHGCAR

module purge
module load intel-2011

dir=`pwd`
ndir="${dir}_1"

mpiexec /global/software/VASP5/vasp-5.3.3/vasp > ./log 
