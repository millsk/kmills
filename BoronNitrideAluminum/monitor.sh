while [ 1==1 ]; do #Loop indefinitely
   if [[ `uptime | awk ' {print ($10+1-1>10?"1":"0")}'` == 1 ]]; then
      if [[ `top -bn1 | grep vasp | awk '{print ($9>5.0?"1":"0") }' | awk ' {sum+=$1} END {print sum}'` -gt 0 ]]
      then
      	for p in `pgrep vasp`; do
      		echo "Suspending execution of VASP process $p"
      		kill -STOP $p
      		sleep 0.5
      	done
      	sleep 30  #sleep for 30 seconds to give time tp cool down.
      else
         echo "VASP already suspended.  Waiting for load averages to drop"
      fi
   else
	   for p in `pgrep vasp`; do
   		echo "Resuming execution of VASP process $p"
   		kill -CONT $p
   		sleep 0.5
   	done
   	sleep 10
   fi
sleep 20  #Let's only check every 20s.
done
