#!/bin/bash

user=kmills
ws=mcs$1
local_dir=$2
echo $3
remote_binary=/home/kmills/bin/vasp
remote_dir='~/computations/'


if [[ ! "x"$3 == "x" ]]; then
   proc=$3
else
   proc=8
fi

echo="echo   --->  "


$echo "Copying files"
scp -r $local_dir $user@$ws:$remote_dir 


niceness=''
if [[ ! "x"$ws == "xmcs11" ]]; then
   niceness=' nice -19 '
fi


#$echo "setting NPAR=2 in INCAR"
ssh $user@$ws  "cd $remote_dir/$local_dir "

$echo "Logging in to remote machine $ws as $user "
ssh $user@$ws "sh -c '
$echo changing to $remote_dir/$local_dir;
cd $remote_dir/$local_dir && 
nohup mpirun -n 1 $remote_binary >> log 2>&1 &
sleep 0.5
'"


$echo "Starting VASP on $ws"







