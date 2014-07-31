#!/bin/sh 
#$ -S /bin/bash 
#$ -cwd 
#$ -N BNAl_AlatB_relaxation
#$ -l h_stack=2G
#$ -j y  
#$ -l h_vmem=8G
#$ -l h_rt=24:00:00
#$ -pe ompi* 80
#$ -R y

	
current_directory=`pwd`

module purge
module load intel openmpi/intel
mpirun ~/bin/vasp > log 
 
