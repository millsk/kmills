import math
import random

number_of_Aluminums=200  #How many Al atoms to place
density = 2.35000#liquid Aluminum density, g/cm**3
atomic_mass = 26.981539  #atomic mass Al, g/mol.

Aluminum_z_boundary = [0.0,9.824192047]

#How much to pad the top and bottom (exclusion volume)
padding_z = [0,0]  #2.9 is the distance from a single Aluminum to the boron-nitride surface after relaxation
padding_xy = 1.0


size_x = 30.0 #13.42
size_y = 30.0 #13.42
size_z = 12.5099420547490006


#print "Cell size",size_x,"x",size_y,"x",size_z, "angstroms"
#print "Aluminum box size",occ_size_x,"x",occ_size_y,"x",occ_size_z, "angstroms"
occ_size_x = size_x-padding_xy
occ_size_y = size_y-padding_xy

number_of_Aluminums = size_z*occ_size_x*occ_size_y * 1.0e-24 * density *6.0221413e23 / atomic_mass

print "there will be ",number_of_Aluminums," aluminum atoms in the cell in order to make it a density of ",density,"."

number_of_Aluminums = int(number_of_Aluminums)

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

f = open("POSCAR_bulk", 'w')

f.write("""BoronNitride
   1.00000000000000
   {0}     0.0      0.0
   0.0     {1}      0.0
   0.0      0.0     {2}
  Al
""".format(size_x,size_y,size_z))




f.close()
