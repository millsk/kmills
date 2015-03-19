#!/bin/bash


function NTDiameter() {

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


HOMO=$(pcregrep -M "2.00000(\n|.){1}.*0.0000" OUTCAR | tail -2 | head -1 | awk '{print $2}' )
LUMO=$(pcregrep -M "2.00000(\n|.){1}.*0.0000" OUTCAR | tail -2 | tail -1 | awk '{print $2}' )


TOTEN=$(grep TOTEN OUTCAR | tail -1 | awk '{print $5}')

NATOMS=$(grep -o 'NIONS.*' OUTCAR | awk '{print $3}')
EPERATOM=$(bc <<< "scale=5;   $TOTEN/$NATOMS")

EGAP=$(bc -l <<< "$LUMO - $HOMO" )

DIAMETER=$(NTDiameter)



#echo "NATOMS,TOTEN,E_PER_ATOM,E_HOMO,E_LUMO,DIAMETER"
echo -e "$NATOMS\t$TOTEN\t$EPERATOM\t$HOMO\t$LUMO\t$EGAP\t$DIAMETER"




