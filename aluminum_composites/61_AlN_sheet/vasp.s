#!/bin/sh 
#$ -S /bin/bash 
#$ -cwd 
#$ -N undoped_MD
#$ -l h_stack=2G
#$ -j y  
#$ -l h_vmem=8G
#$ -l h_rt=47:00:00
#$ -pe ompi* 80
#$ -R y
	
current_directory=`pwd`

module purge
module load intel openmpi/intel
mpirun ~/bin/vasp > log 
 
