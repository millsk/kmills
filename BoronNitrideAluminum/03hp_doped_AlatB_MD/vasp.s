#!/bin/sh 
q='mpi'
r='2d'
o='log'
n=80
m='2g'

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/work/kmills/lib
current_directory=`pwd`

sqsub -q $q -r $r -o $o -n $n --mpp=$m  /work/kmills/bin/vasp

 
