#!/bin/bash

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

