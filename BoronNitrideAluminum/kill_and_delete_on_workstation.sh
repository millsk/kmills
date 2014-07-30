#!/bin/bash


user=kmills
ws=mcs$1
if [[ "x$2" == "xKILL" ]] ; then

remote_binary=/home/kmills/bin/vasp
remote_dir='~/BNAl/'




echo "Logging in to remote machine $ws as $user "
ssh $user@$ws "sh -c '


echo killing all running vasp processes
killall vasp
cd ~/BNAl/
echo Removing all directories in ~/BNAl

rm -r *
cd 

'

"


fi



