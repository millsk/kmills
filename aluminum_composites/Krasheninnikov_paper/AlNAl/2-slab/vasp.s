#!/bin/bash
#PBS -l walltime=72:00:00
#PBS -l pmem=2000mb
#PBS -r n
#PBS -l procs=112
#PBS -M kyle.mills@uoit.net

#PBS -N "slab_AlAl111_rel"

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
