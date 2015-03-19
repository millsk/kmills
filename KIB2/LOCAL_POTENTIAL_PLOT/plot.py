#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import time, sys


all_data = []

for kk,ff in enumerate([sys.argv[i+1] for i in xrange(1)]):
   readFile = ff #sys.argv[1]
   header_size=10
   f = open(readFile, 'r')
   [f.readline() for _ in range(6)] #Skip first 6 lines
   #Add up all the numbers on the 7th line.  There will be this many *more* header lines (one for each molecule)
   header_size+= int(sum([float(i) for i in f.readline().split()]))
   f.seek(0) #rewind
   junk = [f.readline() for _ in range(header_size-1)] #Read the header to get past it.  Don't do anything with it
   nx,ny,nz=[int(i) for i in f.readline().split() ] #Read the dimensions of the file
   f.seek(0) #Rewind to the beginning again
   l = []
   for i,line in enumerate(f):
      if "augmentation" in line: break
      if i >= header_size:             #Only process the data if it's not part of the header
         for d in line.split():        #Split the 5 elements on each
            l.append(float(d))         #Append them to a 1D array
   l = np.array(l)                     #Make it a numpy array
   data2 = np.reshape(l,(nx,ny,nz))    #Reshape the 1D array into a 3D array.  Numpy is magical.
   
   #if kk==1:
#      data2 = data2 / (30**3)
#      print nx*ny*nz
   f.close()

#   plt.plot(np.mean( data2, axis=(1,0)))  #Plot the normalised sum (average) of x (x+y) vs. z 
#   plt.plot(np.mean( data2, axis=(2,0)))
   plt.plot(np.mean( data2, axis=(1,2)))





#   plt.plot(data2[nx/2][ny/2][:])
#   plt.plot(data2[nx/2][:][nz/2])
#   plt.plot(data2[:][ny/2][nz/2])





print "The local potential along each of the 12 edges is: "
print np.mean(data2[2][2][:]       ), "  [2    2    : ]"
print np.mean(data2[2][:][2]       ), "  [2    :    2 ]"
print np.mean(data2[:][2][2]       ), "  [:    2    2 ]"
print np.mean(data2[nx-2][2][:]    ), "  [nx   2    : ]"
print np.mean(data2[nx-2][:][2]    ), "  [nx   :    2 ]"
print np.mean(data2[nx-2][ny-2][:] ), "  [nx   ny   : ]"
print np.mean(data2[:][ny-2][2]    ), "  [:    ny   2 ]"
print np.mean(data2[2][ny-2][:]    ), "  [2    ny   : ]"
print np.mean(data2[nx-2][:][nz-2] ), "  [nx   :    nz]"
print np.mean(data2[2][:][nz-2]    ), "  [2    :    nz]"
print np.mean(data2[:][2][nz-2]    ), "  [:    2    nz]"
print np.mean(data2[:][ny-2][nz-2] ), "  [:    ny   nz]"

#plt.ylim((-1,1))

plt.show()
plt.savefig('output.png')

























