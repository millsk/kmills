#!/bin/sh 



#PBS -l nodes=10:ppn=8,walltime=47:45:00
#PBS -N "hot_1400K_undoped"
cores=80


cd $PBS_O_WORKDIR


current_directory=`pwd` > log

module purge
module load intel openmpi


mpirun -np $cores ~/bin/vasp > log 
 
