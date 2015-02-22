#!/bin/bash
#PBS -l walltime=00:20:00
#PBS -l pmem=2000mb
#PBS -r n
#PBS -l procs=4
#PBS -M kyle.mills@uoit.net

#PBS -N "BNAL_perfect_system"

cd $PBS_O_WORKDIR
echo -n "START " > datefile
date >> datefile

touch WAVECAR
touch CHGCAR

#module purge
#module load intel-2011

dir=`pwd`
ndir="${dir}_1"

mpiexec vasp5 > ./log 
