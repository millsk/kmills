#!/usr/bin/python
import numpy as np
from operator import itemgetter
import sys

chgcar = True #True: Make a CHGCAR file. False: Make a cube file

#=================================================================
#======= OPTIONS =================================================
#=================================================================
number_of_atoms = 2              #Total number of atoms
data_origin = [0, 0, 0]          #Point where coordinates are relative to
atom_species = [1,3]             #1 for hydrogen,  3 for Lithium, 12 for carbon, etc.
atom_coordinates = [[8.620,7.0,7.0],[7.0,7.0,7.0]] #coordinates of each atom specified above
x_len = [14.000,0.000,0.000]  #Cell x-axis vector
y_len = [0.000,14.000,0.000]  #Cell y-axis vector
z_len = [0.000,0.000,14.000]  #Cell z-axis vector
#=================================================================
#=================================================================
#=================================================================





#Get name of file from input argument
rFile = sys.argv[1]
f = open(rFile.split(".")[0] + ".cube","w") #open output file with same name as input file

#Make a new list containing the species and the coordinates together
atom_info = [[atom_species[i],atom_coordinates[i][0],atom_coordinates[i][1],atom_coordinates[i][2]] for i in range(len(atom_species))]

#List of atomic symbols (add to the list if using atom(s) higher than Zr.
ptable=["","H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl",
"Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se",
"Br","Kr","Rb","Sr","Y","Zr"] #...

#Open the input file, read into lines
lines = [line.strip() for line in open(rFile)]
#Read data into array
temp = np.array([line.split() for line in lines ])

#If we want a CHGCAR file, then resort the data array with the z-index moving fastest as
#that's the format for CHGCAR (cube files have the x-index moving fastest
if chgcar:
   temp = sorted(temp, key=itemgetter(2,1,0,3))
   temp = np.array(temp)

#Split up the array into columns to use separately

x = temp[:,0].astype(np.float)
y = temp[:,1].astype(np.float)
z = temp[:,2].astype(np.float)
psi = temp[:,3].astype(np.float)


#START WRITING THE FILE:

#First two lines are arbitrary comments (one line for CHGCAR)
f.write("COMMENT LINE 1\n")
if not chgcar:
   f.write("COMMENT LINE 2\n")

#Let's check to make sure we didn't make a typo and forget to input some information at the top.  If so, give a warning (but continue
#to write the file.
if (len(atom_species) != number_of_atoms):
   print "WARNING: atom_species list different length than number_of_atoms!"
if (len(atom_coordinates) != number_of_atoms):
   print "WARNING: atom_coordinates list different length than number_of_atoms!"

if not chgcar:
   # Number of atoms, position of origin
   #   ie:  " 1  0.000000 0.000000 0.000000"
   f.write("{0:12.0f}{1:12.8f}{2:12.8f}{3:12.8f}\n".format(number_of_atoms,data_origin[0],data_origin[1],data_origin[2]))
else:
#Write the scaling factor.  I'll hard-code a 1.000 because that's all I've ever seen this as.
   f.write("{0:12.12f}\n".format(1.0))

#Number of unique x,y,z values (ie: number of data points (voxels) in x,y,z directions)
nx = len(set(x))
ny = len(set(y))
nz = len(set(z))

#Normalise the  axis vectors
x_vector =  [i/nx for i in x_len ]
y_vector =  [i/ny for i in y_len ]
z_vector =  [i/nz for i in z_len ]

if not chgcar:
   #the number of voxels along each axis (x, y, z) followed by the normalised axis vector
   f.write("{0:12.0f}{1:12.8f}{2:12.8f}{3:12.8f}\n".format(nx,x_vector[0],x_vector[1],x_vector[2]))
   f.write("{0:12.0f}{1:12.8f}{2:12.8f}{3:12.8f}\n".format(ny,y_vector[0],y_vector[1],y_vector[2]))
   f.write("{0:12.0f}{1:12.8f}{2:12.8f}{3:12.8f}\n".format(nz,z_vector[0],z_vector[1],z_vector[2]))
else:
   #The non-normalised axis vectors, x first, then y and then z
   f.write("{0:12.6f}{1:12.6f}{2:12.6f}\n".format(x_len[0],x_len[1],x_len[2]))
   f.write("{0:12.6f}{1:12.6f}{2:12.6f}\n".format(y_len[0],y_len[1],y_len[2]))
   f.write("{0:12.6f}{1:12.6f}{2:12.6f}\n".format(z_len[0],z_len[1],z_len[2]))

#If it's a cube file, then output the atom information:
if not chgcar:
   for a in range(number_of_atoms):
      #atomic number of atom, (charge of the atom = 0.0), x, y, z of atom
      f.write("{0:12.0f}{1:12.8f}{2:12.8f}{3:12.8f}{4:12.8f}\n".format(atom_species[a], 0, atom_coordinates[a][0],atom_coordinates[a][1],atom_coordinates[a][2] ))

if chgcar:
   coordinates = [] #Empty list to hold coordinates of individual atoms (might not be in the same order as the manually specified atom_coordinates list.
   l1=l2=coords=""  #Empty strings to hold the atom species line and the number (count) of each atom line
   for a in set(atom_species): #For each distinct type of atom
      l1="{0}  {1}".format(l1,ptable[a])  #Add the atomic symbol to the line
      l2="{0}  {1}".format(l2,atom_species.count(a))  #add the "count" of that atom to the next line
      for i in range(number_of_atoms):  #Now add the coordinates for each atom
         if (a==atom_info[i][0]):       #but we must add them in the same order that the types are specified
            coordinates.append([atom_info[i][1],atom_info[i][2],atom_info[i][3]])
   #Write out all the data
   f.write("{0}\n".format(l1))
   f.write("{0}\n".format(l2))
   f.write("Cartesian \n")
   for a in range(number_of_atoms):
      f.write("{0:12.6f}{1:12.6f}{2:12.6f}\n".format(coordinates[a][0],coordinates[a][1],coordinates[a][2]))
   f.write("\n")
   f.write("{0:6.0f}{1:6.0f}{2:6.0f}\n".format(nx,ny,nz))

#Now write out all the volumetric data.  It's stored in variable #Psi in the order it should be written .
for i in xrange(len(z)):
   f.write("%14.8e   " % psi[i] )
   if i%5 == 4: f.write("\n") # Put a line break every 5 data points

f.close() #Close the file

