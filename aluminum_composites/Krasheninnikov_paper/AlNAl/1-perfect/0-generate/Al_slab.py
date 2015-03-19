from ase.lattice.surface import fcc111,hcp0001
from ase.lattice.hexagonal import *
from ase import io
from os import system
import math


POSCAR_string = "N  Al"
lattice_constant_Al = 4.0495
a_lattice_constant_BN = 3.111


#Code to optimize the dimensions (find the lowest common multiple with acceptable (<1%) stress)
#rr = range(2,20)

#for i1 in rr:
#   for j1 in rr:
#      for i2 in rr:
#         for j2 in rr:
#            slab = fcc111('Al',size=(j1,j2,3), a=lattice_constant_Al, orthogonal=False,vacuum=0.0)
#
#            bn= hcp0001('B',size=(i1,i2,2), a=a_lattice_constant_BN, c=0.0000001, vacuum=0.0)
#
#            x = [ bn.get_cell()[0][0], slab.get_cell()[0][0] ]
#            pdx = 2.*abs( x[0] - x[1]) / (x[0] + x[1] )
#
#            yx = [ bn.get_cell()[1][0], slab.get_cell()[1][0] ]
#            yy = [ bn.get_cell()[1][1], slab.get_cell()[1][1] ]
#            pdyx = 2.*abs( yx[0] - yx[1]) / (yx[0] + yx[1] )
#            pdyy = 2.*abs( yy[0] - yy[1]) / (yy[0] + yy[1] )
#
#            if (pdx < 0.02 and pdyx < 0.02 and pdyy < 0.02):
#               print "AlN: ({i1},{i2})\tAl: ({j1},{j2})\t {pdx}\t{pdyx}\t{pdyy}".format(i1=i1*2,i2=i2,j1=j1,j2=j2,pdx=pdx*100,pdyx=pdyx*100,pdyy=pdyy*100)



slab = fcc111('Al',size=(12,12,3), a=lattice_constant_Al, orthogonal=False,vacuum=0.0)
bn= hcp0001('B',size=(11,11,2), a=a_lattice_constant_BN, c=0.0000001, vacuum=0.0)
cell = bn.get_cell()


bn.translate([0,0,10])
num_each = bn.get_number_of_atoms() / 2

bn.set_atomic_numbers([7]*num_each + [13]*num_each)

bn.extend(slab)
bn.set_cell(cell)
bn.center(vacuum=10, axis=2)
bn.translate([0,0,-10])

io.write('POSCAR',bn)

system('sed -i "s|Cartesian|Selective Dynamics\\nCartesian|g" POSCAR')
system('head -5 POSCAR > POSCAR_new')
system('echo " {0} " >> POSCAR_new'.format(POSCAR_string))
system('head -8 POSCAR | tail -3 >> POSCAR_new')
system("awk 'NR>8{if($3==0) print $0,\" F F F \";else if($3!=0)print $0,\" T T T \" ; }' POSCAR >> POSCAR_new")
system("mv POSCAR_new POSCAR")

