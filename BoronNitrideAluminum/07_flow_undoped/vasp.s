#!/bin/sh 
#$ -S /bin/bash 
#$ -cwd 
#$ -N BNAl_flow_undoped
#$ -l h_stack=2G
#$ -j y  
#$ -l h_vmem=8G
#$ -l h_rt=12:00:00
#$ -pe ompi* 40
#$ -R y
	
current_directory=`pwd`

module purge
module load intel openmpi/intel
mpirun ~/bin/vasp > log 
 
