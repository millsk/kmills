#!/bin/sh 
#$ -S /bin/bash 
#$ -cwd 
#$ -N kappa_kombined
#$ -l h_stack=2G
#$ -j y  
#$ -l h_vmem=8G
#$ -l h_rt=03:00:00
#$ -pe ompi* 16
#$ -R y

	
current_directory=`pwd`

module purge
module load intel openmpi/intel
mpirun ~/bin/vasp > log 
 
