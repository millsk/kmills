from ase.lattice.surface import fcc111,hcp0001
from ase.lattice.hexagonal import *
from ase import io
from os import system
import math


POSCAR_string = "B  N  Al"
lattice_constant_Al = 4.050
a_lattice_constant_BN = 2.5040
c_lattice_constant_BN = 6.6612


slab = fcc111('Al',size=(7,7,3), a=lattice_constant_Al, orthogonal=False,vacuum=0.0)

bn= hcp0001('B',size=(8,8,2), a=a_lattice_constant_BN, c=0.0000001, vacuum=0.0)
cell = bn.get_cell()
#cell[2][2]=20.0

bn.translate([0,0,10])
num_each = bn.get_number_of_atoms() / 2

bn.set_atomic_numbers([5]*num_each + [7]*num_each)

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

