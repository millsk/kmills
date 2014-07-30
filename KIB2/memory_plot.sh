# /bin/bash


if [ "x$@" == 'x' ]; then
   echo -e "USAGE: \n \t\t memory_plot.sh 'command to run'\n \t ie: memory_plot.sh 'python script.py'\n" 

fi
 
# Setup
datfile=`mktemp`
echo "ElapsedTime MemUsed" > $datfile
 
starttime=`date +%s.%N`
 
# Run the specified command in the background
$@ &


pp="$!" #PID of the last process
 
# While the last process is still going
while [ -n "`ps --no-headers $!`" ]
do
   bytes=`ps -o rss -p $pp --no-headers ` #| awk '{SUM += $1} END {print SUM}'`
   elapsed=$(echo $(date +%s.%N) - $starttime | bc)
   if [ $bytes ]
   then
      echo $elapsed $bytes >> $datfile
   fi
   sleep 0.005
done
cat $datfile
 
# Plot up the results with matplotlib
cat <<EOF | python
import pylab, sys, numpy
fffile = file("$datfile")
fffile.readline() # skip first line
data = numpy.loadtxt(fffile)
time,mem = data[:,0], data[:,1]/1024
pylab.plot(time,mem)
pylab.xlabel('Elapsed Time (s): Total %0.5f s' % time.max())
pylab.ylabel('Memory Used (MB): Peak %0.2f MB' % mem.max())
pylab.show()
EOF
 
rm $datfile
