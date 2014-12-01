#!/bin/bash

user=kmills
ws=orcinus.westgrid.ca
unused=$1
local_dir=$2
remote_binary=/home/kmills/bin/vasp
remote_dir='/home/kmills/BNAl/NT_Characterization/'
echo="echo "

scp -r $local_dir $user@$ws:$remote_dir 


$echo "Logging in to remote machine $ws as $user "

ssh $user@$ws "sh -c '
$echo changing to $remote_dir/$local_dir;
cd $remote_dir/$local_dir && 
qsub vasp.s &
sleep 0.5 
qstat -u kmills
'"


$echo "Starting VASP on $ws"







