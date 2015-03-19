
#sh generate_job.sh n m element1 element2 bond_length workstation


#Al N:      bl = 1.890
#B  N:      bl = 1.446

a1="Al"
a2="N"
bl="1.890"

for n in {2..14..2}; do
  sh generate_job.sh $n 0 $a1 $a2 $bl 1  
  sh generate_job.sh $n $n $a1 $a2 $bl 1  
  sh generate_job.sh $n $(($n/2)) $a1 $a2 $bl 1 
done
