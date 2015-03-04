
<<<<<<< HEAD
#sh generate_job.sh n m element1 element2 bond_length workstation
=======
>>>>>>> ceaaf7719634debabde9d6fd8b1e96cb71d5cf50

#BL:  1.446 (BNNT)
#     1.446 (AlNT)

<<<<<<< HEAD
=======
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
>>>>>>> ceaaf7719634debabde9d6fd8b1e96cb71d5cf50

# (n, n/2)

sh generate_job.sh 2 1 B N 1.446 06
sh generate_job.sh 4 2 B N 1.446 06
sh generate_job.sh 6 3 B N 1.446 06
sh generate_job.sh 8 4 B N 1.446 06

sh generate_job.sh 10 5 B N 1.446 05
sh generate_job.sh 12 6 B N 1.446 05
sh generate_job.sh 14 7 B N 1.446 05


# (n, n)

sh generate_job.sh 2 2 B N 1.446 11
sh generate_job.sh 3 3 B N 1.446 11
sh generate_job.sh 4 4 B N 1.446 11
sh generate_job.sh 5 5 B N 1.446 11
sh generate_job.sh 6 6 B N 1.446 11
sh generate_job.sh 7 7 B N 1.446 11
sh generate_job.sh 8 8 B N 1.446 11

sh generate_job.sh 9 9 B N 1.446 13
sh generate_job.sh 10 10 B N 1.446 13
sh generate_job.sh 11 11 B N 1.446 13


# (n, 0)

sh generate_job.sh 2 0 B N 1.446 10
sh generate_job.sh 3 0 B N 1.446 10
sh generate_job.sh 4 0 B N 1.446 10
sh generate_job.sh 5 0 B N 1.446 10

sh generate_job.sh 6 0 B N 1.446 09
sh generate_job.sh 7 0 B N 1.446 09
sh generate_job.sh 8 0 B N 1.446 09
sh generate_job.sh 9 0 B N 1.446 09

sh generate_job.sh 10 0 B N 1.446 07
sh generate_job.sh 11 0 B N 1.446 07
sh generate_job.sh 12 0 B N 1.446 07


