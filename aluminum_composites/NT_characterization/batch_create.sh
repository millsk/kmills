


#Al N:      bl = 1.890
#B  N:      bl = 1.446


for n in {2..14..2}; do
  sh generate_job.sh $n 0 B N 1.446 1  
  sh generate_job.sh $n $n B N 1.446 1  
  sh generate_job.sh $n $(($n/2)) B N 1.446 1 
done






