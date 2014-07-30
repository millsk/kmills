#!/usr/bin/python
import numpy as np
import numpy.linalg as la
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
   #print "{0} norm: {1}".format(filename_iota, norm

   psisquared = np.real(innerproduct)**2 + np.imag(innerproduct)**2
   psisquare_rounded = round(psisquared*100,0)
   star= ('*' if psisquared>0.1 else '')
   if psisquare_rounded > 10 or not only_show_significant:
      print "    {0}{1:9.6f}\t{2:4.0f}% \t{3}{4}".format(path2.ljust(15),innerproduct, psisquare_rounded, star, '' )


def make_fill_blank(aFile):
   size = 2*max_dim + 5
   blank = np.zeros((size,size,size), dtype=np.complex_)
   for i in aFile:
      blank[int(i[0])][int(i[1])][int(i[2])] = np.complex(i[3],i[4])
   return blank

def lap(message=""):
   global stime
   print str(round(time.time() - stime,3)) + "\t" + message
   stime = time.time()


#Load all files into memory:

stime = time.time()

iota1_collection = []
iota2_collection = []
kappa_collection = []
kappa_name_list = sorted(os.listdir('kappa'))
iota1_name_list = sorted(os.listdir('iota1'))
iota2_name_list = sorted(os.listdir('iota2'))


for kappa in kappa_name_list:
   kappa_collection.append(read_file('kappa/'+kappa))
   lap("Reading (kappa) file " + kappa)
for iota1 in iota1_name_list:
   iota1_collection.append(read_file('iota1/' + iota1))
   lap("Reading (iota1) file " + iota1)
for iota2 in iota2_name_list:
   iota2_collection.append(read_file('iota2/' + iota2))
   lap("Reading (iota2) file " + iota2)

max_dim = []
for dataFile in iota1_collection + iota2_collection + kappa_collection:
   max_dim.append(max([np.max(np.abs(dataFile[:,i])) for i in(0,1,2)]))
max_dim = max(max_dim)
lap("Finding maximum dimension")

kappa_collection = [np.add(s, [max_dim, max_dim, max_dim, 0, 0]) for s in kappa_collection]
iota1_collection = [np.add(s, [max_dim, max_dim, max_dim, 0, 0]) for s in iota1_collection]
iota2_collection = [np.add(s, [max_dim, max_dim, max_dim, 0, 0]) for s in iota2_collection]
lap("Adding scalar to bring origin to (0,0,0)")

kappa_collection = [ make_fill_blank(s) for s in kappa_collection ]
iota1_collection = [ make_fill_blank(s) for s in iota1_collection ]
iota2_collection = [ make_fill_blank(s) for s in iota2_collection ]
lap("Creating and filling blank arrays")

kappa_collection = [ s.flatten() for s in kappa_collection ]
iota1_collection = [ s.flatten() for s in iota1_collection ]
iota2_collection = [ s.flatten() for s in iota2_collection ]
lap("Flattening arrays")

#a = [ np.inner(np.conjugate(s),s) for s in iota1_collection ]  #  <1|1>
#b = [ np.inner(np.conjugate(s[0]),s[1]) for s in zip(iota1_collection,iota2_collection)]  #  <1|2>
#c = [ np.inner(np.conjugate(s[0]),s[1]) for s in zip(iota2_collection,iota1_collection)]  #  <2|1>
#d = [ np.inner(np.conjugate(s),s) for s in iota2_collection ]  #  <2|2>
#e = [ np.inner(np.conjugate(s[0]),s[1]) for s in zip(iota1_collection,kappa_collection)]  #  <1|k>
#f = [ np.inner(np.conjugate(s[0]),s[1]) for s in zip(iota2_collection,kappa_collection)]  #  <2|k>
#lap("Computing inner products")

for ki,k in enumerate(kappa_collection):
#   print kappa_name_list[ki]
   print "--------------------------------------------"
   for i1i,i1 in enumerate(iota1_collection):
#      print "   ",iota1_name_list[i1i]
      for i2i,i2 in enumerate(iota2_collection):
         aa = np.inner(np.conjugate(i1),i1)
         bb = np.inner(np.conjugate(i1),i2)
         cc = np.inner(np.conjugate(i2),i1)
         dd = np.inner(np.conjugate(i2),i2)
         ee = np.inner(np.conjugate(i1),k)
         ff = np.inner(np.conjugate(i2),k)
#         print "aa = ",aa
#         print "bb = ",bb
#         print "cc = ",cc
#         print "dd = ",dd

         coef =  np.array( [ [ aa,bb ],[cc,dd] ] )
         vect = np.array( [ [ee],[ff]])
         sol = la.solve(coef,vect)
         norm = [la.norm(sol[0]),la.norm(sol[1])]
#         norm = [np.real(sol[0])[0],np.real(sol[1])[0]]


         print "      {kappa} = {0:3.0f}*{1}  +  {2:3.0f}*{3}".format(100*abs(norm[0]),iota1_name_list[i1i], 100*abs(norm[1]),iota2_name_list[i2i],kappa=kappa_name_list[ki])

