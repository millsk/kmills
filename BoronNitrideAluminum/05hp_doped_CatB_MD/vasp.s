#!/bin/sh 

name='CatB_MD'
q='mpi'
r='7d'
o='log'
n=80
m='2g'
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/work/kmills/lib


current_directory=`pwd`

#module purge
#module load intel openmpi/intel
sqsub -j "$name" -q $q -r $r -o $o -n $n --mpp=$m  /work/kmills/bin/vasp
 
