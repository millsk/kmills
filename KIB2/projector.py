#!/usr/bin/python
#Seems to be working, but overlap does exist
import numpy as np
import sys
import time
import resource
import os, os.path
btime = time.time() #beginning time of the script
debug=False #True
star=''
num_files_read=0
read_time=0
only_show_significant = True

first_iteration=True

if len(sys.argv)==1:
   file_load_method = 'np'
else:
   file_load_method = sys.argv[1]

def debug_write(data,identity):
   if debug:
      f = open("debug/debug" + identity, "w")
      for i,x in enumerate(data):
         for j,y in enumerate(x):
            for k,z in enumerate(y):
               f.write("{0:10.0f}\t{1:10.0f}\t{2:10.0f}\t{3:10.6f}\n".format(i,j,k,data[i][j][k]))
      f.close()

def read_file(path):
   global num_files_read
   global read_time
   global read_method
   stime = time.time()
   if file_load_method == 'np':
      file1 = np.loadtxt(path)
      read_method='numpy.loadtxt()'
   else:
      read_method='iterative read (line by line)'
      f = open(path,'r')
      l = []
      for line in f:
         l.append([float(k) for k in line.split()])
      f.close()
      file1 = np.array(l)
   num_files_read+=1
   read_time+=(time.time() - stime)
   return file1

def compare_to_file(path2,file1):
   global maxlen
   global first_iteration
   global blank1
   global flat1
   file2 = read_file(path2)
   if first_iteration:
      blank1 = make_fill_blank(file1)
      flat1 = blank1.flatten()
      first_iteration = False
   file2=np.add(file2,[max_dim,max_dim,max_dim,0,0])
   len2 = [int(np.max(file2[:,i]) - np.min(file2[:,i])) + 1 for i in (0,1,2)]
   maxlen = [  max(  [len1[i], len2[i] ]   ) for i in (0,1,2)]
   blank2 = make_fill_blank(file2)
   debug_write(blank1,filename_iota + "_" + filename_kappa + "IOTA")
   debug_write(blank2,filename_iota + "_" + filename_kappa + "KAPPA")
   #Make a zeros 3d array and fill it with contents of file2
   flat2 = blank2.flatten()
   innerproduct = np.inner(np.conjugate(flat1),flat2)
   #norm = np.inner(np.conjugate(flat1),flat1)
   #print "{0} norm: {1}".format(filename_iota, norm)


   psisquared = np.real(innerproduct)**2 + np.imag(innerproduct)**2
   psisquare_rounded = round(psisquared*100,0)
   star= ('*' if psisquared>0.1 else '')
   if psisquare_rounded > 10 or not only_show_significant:
      print "    {0}{1:9.6f}\t{2:4.0f}% \t{3}{4}".format(path2.ljust(15),innerproduct, psisquare_rounded, star, '' )


def make_fill_blank(aFile):
   #print "MaxLen: {0}".format(maxlen)
   size = 2*max_dim + 5
   blank = np.zeros((size,size,size), dtype=np.complex_)
   for i in aFile:
      x,y,z,re,im = i
      blank[int(x)][int(y)][int(z)] = np.complex(re,im)
#   print blank.shape
   return blank

#BEGINNING OF MAIN PROGRAM
#Get a list of all files in iota directory
paths1 = sorted(os.listdir('iota'))
#Get list of all files in ./kappa directory
paths2 = sorted(os.listdir('kappa'))


for filename_iota in paths2:
   first_iteration=True
   file1 = read_file('kappa/'+filename_iota)
   ###############
   #Prepare the first file:
   ###############
   max_dim = max([np.max(np.abs(file1[:,i])) for i in(0,1,2)]  )   #Get maximum absolute value of grid points (must add it later so that we don't have negative indices)
   file1=np.add(file1,[max_dim,max_dim,max_dim,0,0])
   #Get the dimensions of the input file
   len1 = [int(np.max(file1[:,i]) - np.min(file1[:,i]))+1 for i in (0,1,2)]
   #Note:  We need to fill a zeroes array with the entries as there are missing G-vectors in the output from WaveTransPlot2. Any zero-valued
   #G vectors are missing, so we must not just dot the n-th entry in file1 with the n-th entry of file2 as they will not necessarily
   #be the same point.
   #Place the data into the blank zeros array
   print "\nProjection of kappa/{0} onto...".format(filename_iota)
#   print "\t File \t Re[Psi] + iImag[Psi] \t Psi**2 Big? \t legacy_Psi**2"
   for filename_kappa in paths1:
      compare_to_file('iota/'+filename_kappa,file1)
#   print "Total time: {0}s".format(time.time() - btime)i


print """
-------------------------------------------------------------------------"""
if only_show_significant: print "NOTE: Only significant projections (>10%) are shown"
print """{numfiles} files read.  Average read time per file: {average}s
using {method}
-------------------------------------------------------------------------
""".format(numfiles=num_files_read, average=read_time / num_files_read, method=read_method)
