
count=0


for file in `ls $1*.pov`; do

infile=$file

outfile=`echo $infile | sed 's|.pov|.tga|'`

count=$(( $count + 1)) 


if [ ! -f "${outfile}.tga" ]; then

   echo -n "\n$infile --> $outfile  "

   sed -i "1N;$!N;s/background {  color rgb <1.00, 1.00, 1.00> }/;P;D" $infile > /dev/null 2>&1
   sed -i 's|finish { ambient 0.000 diffuse|finish { reflection {0.04, 0.4} ambient 0.000 diffuse|g' $infile > /dev/null 2>&1
   povray -W$2 -H$3 -I$infile -o$outfile -D +X +A +FT  > /dev/null 2>&1  &  

   echo "x$(($count % 4))"


   #don't spawn any new renders if there are already 4 running
   
   while [ `pgrep povray | wc -l` -gt 3 ]; do
      sleep 0.1
      echo -n "."
   done

fi

done 




