import math
import random

number_of_Aluminums=500  #How many Al atoms to place
density = 2.35000#liquid Aluminum density, g/cm**3
atomic_mass = 26.981539  #atomic mass Al, g/mol.

Aluminum_z_boundary = [0.0,9.824192047]

#How much to pad the top and bottom (exclusion volume)
padding_z = [0,0]  #2.9 is the distance from a single Aluminum to the boron-nitride surface after relaxation
padding_xy = 1.0


#THESE ARE APPROXIMATE AND WILL BE ADJUSTED
#IN ORDER TO FIT THE BORON NITRIDE LATTICE
size_x = 25.0 #13.42
size_y = 25.0 #13.42
size_z = 40.0 #15.42

scaling = 1.446      #bondlength


nx = int(math.floor((size_x/((3./2.)*scaling))))
ny = int(math.floor((size_y/(math.sqrt(3)*scaling))))

if not nx%2==0: nx+=1
if not ny%2==0: ny+=1


size_x = nx * scaling * (3./2.)
size_y = ny * math.sqrt(3) * scaling

#The occupied size, that is, the dimensions of the "box" containing aluminum atoms
occ_size_x = size_x - padding_xy
occ_size_y = size_y - padding_xy

#print "Cell size",size_x,"x",size_y,"x",size_z, "angstroms"
#print "Aluminum box size",occ_size_x,"x",occ_size_y,"x",occ_size_z, "angstroms"

occ_size_z = number_of_Aluminums*atomic_mass / (occ_size_x*occ_size_y * 1.0e-24 * density * 6.0221413e23)

size_z = occ_size_z + padding_z[0] + padding_z[1]


print "For ",number_of_Aluminums,"atoms, the z-dimension of the cell should be",size_z

print "Then the density will be", number_of_Aluminums*atomic_mass / (occ_size_x*occ_size_y * 1.0e-24 * occ_size_z * 6.0221413e23)



f2=open("packmol_input_ending.temp","w")
f2.write("""  number {numAl}
  inside box {0} {1} {2} {3} {4} {5}
end structure

""".format(
padding_xy,
padding_xy,
padding_z[0],
size_x, #-padding_xy,
size_y, #-padding_xy,
size_z-padding_z[1],
numAl=number_of_Aluminums)
)

f2.close()

Ns = []
for i in range(nx):
   for j in range(ny):
      if i%2==0:
         dy=0
      else:
         dy=math.sqrt(3) / 2.0
      coord = [scaling*i*(3./2.),(dy+j*math.sqrt(3))*scaling, 0 ]
      Ns.append(coord)


f = open("POSCAR", 'w')

max_x = max( el[0] for el in Ns )
max_y = max( el[1] for el in Ns )

f.write("""BoronNitride
   1.00000000000000
   {0}     0.0      0.0
   0.0     {1}      0.0
   0.0      0.0     {2}
  B  N Al
""".format(size_x,size_y,size_z))



count = len(Ns)
f.write(" {0}  {1}  {2} \n".format(count,count,number_of_Aluminums))

f.write("Cartesian \n")

for data in Ns:
    f.write("{0}\t{1}\t{2} \n".format(data[0], data[1], data[2]))
for data in Ns:
   f.write("{0}\t{1}\t{2} \n".format(data[0]+1.0*scaling, data[1], data[2]))

f.close()
