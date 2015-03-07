#!/bin/bash

echo='echo -e '


if [ "x$1" == "xheader" ]; then
#Dump the header
   $echo "SYSTEM\tNATOMS\tTOTEN\tE_PER_ATOM\tE_HOMO\tE_LUMO\tE_GAP\tDIAMETER"
   exit 0
fi


function  NTdiameter() {
   awk '
      BEGIN {xsum=0; ysum=0; count=0; rsum=0; rcount=0}
      NR==FNR && FNR==3 {xlatt=$1}
      NR==FNR && FNR==4 {ylatt=$2}
      NR==FNR && NF==0 {
         xcentre=xlatt*(xsum/count);
         ycentre=ylatt*(xsum/count);
         next;
         }
      NR==FNR && FNR>8 {xsum+=$1; ysum+=2; count+=1}


      NR != FNR && NF==0 {exit 1}
      NR != FNR && FNR>8 {
         rsum+=sqrt(  ($1*xlatt-xcentre)**2 + ($2*ylatt-ycentre)**2 );
         rcount+=1;
      }
      END {print 2*rsum/rcount }

   ' CONTCAR CONTCAR
}



function HOMOLUMO () {

   pcregrep -M '2\.00000.*(\n)*.*2\.00000.*(\n)*.*0\.00000.*(\n)*.*0\.00000' OUTCAR | tail -4 | head -3 | tail -2 | awk '{print $2}'

}

function energy_per_atom() {
        NATOMS=$(awk 'NR==7 {for(i=1;i<=NF;i++) t+=$i; print t; t=0}' POSCAR)
        TOTEN=$(grep TOTEN OUTCAR | tail -n 1 | awk '{print $5 }')
#        echo -e "TOTEN  \t\t NATOMS "
#        echo -e "$energy \t $atoms "
}


SYSTEMNAME=$(echo "${PWD##*/}")

diameter=$(NTdiameter)
E_HOMO=$(HOMOLUMO | head -n 1)
E_LUMO=$(HOMOLUMO | tail -n 1)
energy_per_atom
E_GAP=$(bc <<< "scale=6; $E_LUMO - $E_HOMO")
E_per_atom=$(bc <<< "scale=6; $TOTEN / $NATOMS " )


$echo "$SYSTEMNAME\t$NATOMS\t$TOTEN\t$E_per_atom\t$E_HOMO\t$E_LUMO\t$E_GAP\t$diameter"



#for d in $(ls -d *AlNNT*); do echo $d; cd $d; NTdiameter; HOMOLUMO; cd ..; echo -e "\n\n\n"; done
