length=0.5
n=$1
m=$2
bondlength=$5
atomtype1=$3
atomtype2=$4
shiftx=15
shifty=15

jobdir='jobs/'
potcar_dir='/home/kmills/work/kmills/POTCAR'

system_name="${n}-${m}_${atomtype1}${atomtype2}NT"

echo "Generating $system_name"

mkdir $jobdir
mkdir ${jobdir}${system_name}
cd ${jobdir}${system_name}
#Copy over all the files we need, change system name in INCAR
cp ../../template/INCAR .
sed -i "s/!!SYSTEMNAME!!/$system_name/g" INCAR
cp ../../template/KPOINTS .
cp ../../template/clean.sh .
cp ../../template/plot.sh .
cp ../../template/vasp.s .
cp ../../template/vasp.bugaboo.s .
cp ../../template/vdw_kernel.bindat .
sed -i "s/!!SYSTEMNAME!!/$system_name/g" vasp.s
sed -i "s/!!SYSTEMNAME!!/$system_name/g" vasp.bugaboo.s

#Make the POTCAR
cat $potcar_dir/$atomtype1/POTCAR $potcar_dir/$atomtype2/POTCAR > POTCAR

#Make the VMD Script
echo "
nanotube -l $length -n $n -m $m -cc $bondlength 
wait 1
animate write POSCAR {temp_vmdPOSCAR} beg 0 end 0 skip 1 0
exit
" > temp_vmd.tcl
#Run the VMD script
vmd -e temp_vmd.tcl





bond_length=$bondlength
atoms="$atomtype1   $atomtype2"
POSCAR="temp_vmdPOSCAR"
echo "doing stuff"

lattx=`awk 'NR==3 {print $1}' $POSCAR`
latty=`awk 'NR==4 {print $2}' $POSCAR`
lattz=`awk 'NR==5 {print $3}' $POSCAR`
count=`awk 'NR==6 {print $1/2}' $POSCAR`




head -2 $POSCAR > head1.tmp

echo "" | awk -v bl=$bond_length -v l=$lattx '{print "  ",l*bl/1.42,  "     0.00000000   0.00000000"}' >> head1.tmp
echo "" | awk -v bl=$bond_length -v l=$latty '{print "   0.00000000  ",l*bl/1.42,  "   0.00000000"}' >> head1.tmp
echo "" | awk -v bl=$bond_length -v l=$lattz '{print "   0.00000000   0.00000000  " ,l*bl/1.42}' >> head1.tmp

echo " $atoms" >> head1.tmp
echo " $count   $count" >> head1.tmp
echo "Cartesian" >> head1.tmp

awk -v bl=$bond_length -v shiftx=$shiftx -v shifty=$shifty -v lattx=$lattx -v latty=$latty -v lattz=$lattz ' NR > 7 { print (($1*lattx)+shiftx)*bl/1.42,"   ",(($2*latty)+shifty)*bl/1.42,"    ",$3*lattz*bl/1.42 }' $POSCAR > tail.tmp



awk 'NR%2==0 {print $0}' tail.tmp > even.tmp
awk 'NR%2!=0 {print $0}' tail.tmp > odd.tmp

cat head1.tmp odd.tmp even.tmp > POSCAR



max=`awk 'BEGIN {max = 0} NR>8 {if ($1>max) max=$1} END {print max}' POSCAR`


awk 'NR<3 {print $0}' POSCAR > NN
awk -v max=$max 'NR==3 {print max+10,"  ",$2,"  ",$3} ' POSCAR >> NN
awk -v max=$max 'NR==4 {print $1,"  ",max+10,"  ",$3} ' POSCAR >> NN
awk 'NR > 4 {print $0}' POSCAR >> NN

cp NN POSCAR




rm *.tmp
rm NN
rm temp_vmd.tcl
rm temp_vmdPOSCAR
cd ../..
echo "iteration done"$(pwd)

echo ' for d in $(ls -d *); do cd $d; qsub vasp.s; cd ..; done ' > $jobdir/qsub.sh

#bash deploy_orcinus.sh $6 $system_name 

