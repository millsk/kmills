#!/bin/bash


user=kmills
local_dir=$2
remote_binary=/home/kmills/bin/vasp
remote_dir='~/BNAl/'





if [[ "x"$1 == "xgpc" ]] ; then
   cluster='login.scinet.utoronto.ca'
elif  [[ "x"$1 == "xmahone" ]] ; then
   cluster='mahone.ace-net.ca'
elif [[ "x"$1 == "xfundy" ]]; then
   cluster='fundy.ace-net.ca'

fi



echo "Copying files"
scp -r $local_dir $user@$cluster:$remote_dir 


if [[ "x"$cluster == "xgpc" ]]; then
   ssh $user@$cluster -t 'ssh gpc02'
else 
   ssh -X $user@$cluster
fi


