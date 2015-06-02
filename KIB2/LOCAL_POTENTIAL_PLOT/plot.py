#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import time, sys

all_data = []

readFile = sys.argv[1]
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
data2 = np.reshape(l,(nz,ny,nx))    #Reshape the 1D array into a 3D array.  Numpy is magical.
f.close()

printline = "print x,np.mean(data2[x,:,:])"

index = sys.argv[2]


outx = open("outx","w")
outy = open("outy","w")
outz = open("outz","w")


if (index==0 or index=='x' or True):
   for x in xrange(nx):
      outx.write(str(x) + "   " + str(np.mean(data2[:,:,x])) + "\n")

if (index==1 or index=='y' or True):
   for y in xrange(ny):
      outy.write(str(y) + "   " + str(np.mean(data2[:,y,:])) + "\n")

if (index==2 or index=='z' or True):
   for z in xrange(nz):
      outz.write(str(z) + "   " + str(np.mean(data2[z,:,:])) + "\n")




