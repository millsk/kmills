#!/bin/sh 
#$ -S /bin/bash 
#$ -cwd 
#$ -N BNAl_relaxation_doped_CatB
#$ -l h_stack=2G
#$ -j y  
#$ -l h_vmem=8G
#$ -l h_rt=08:00:00
#$ -pe ompi* 80
#$ -R y
	
current_directory=`pwd`

module purge
module load intel openmpi/intel
mpirun ~/bin/vasp > log 
 
