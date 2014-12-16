import math
import random
from ase.lattice.surface import fcc111
from ase.lattice.hexagonal import *
from ase.lattice import *
from ase import io
import numpy as np
from ase.visualize import view
import os
#BORON NITRIDE:
scaling = 1.446      #bondlength

lattice_constant_Al = 4.050
a_lattice_constant_BN = 2.5040
c_lattice_constant_BN = 6.6612




bn = surface.hcp0001('B', size=(8,8,2), a=a_lattice_constant_BN, c=0.0000001, vacuum=10.0, orthogonal=True)
bn.translate([0,0,10.0])

num_each = len(bn.get_positions())/2
bn.set_atomic_numbers([5]*num_each + [7]*num_each )


#ALUMINUM


al = fcc111('Al',size=(7,8,3), a=lattice_constant_Al, orthogonal=True, vacuum=10.0)

#bn = Hexagonal('B',size=(8,8,1), latticeconstant = {'a':1.446, 'c':1.446})
#bn = fcc111('B',size=(8,8,1), a=1.5*a_lattice_constant_BN, vacuum=6.0,orthogonal=True)

#Need to somehow get orthographic coordinates for bn sheet

#bn = Hexagonal(symbol='B', size=(8,8,1), latticeconstant={'a':a_lattice_constant_BN, 'c': c_lattice_constant_BN})

print "Al cell:"
print al.get_cell()
print al.get_number_of_atoms()

print "BN cell:"
print bn.get_cell()
print bn.get_number_of_atoms()




bn.write('bn.xyz',format='xyz')
al.write('al.xyz',format='xyz')

os.system("cat bn.xyz al.xyz > total.xyz")

total = io.read("total.xyz")

io.write('POSCAR',total)


#io.write('POSCAR_B',b)
#io.write('POSCAR_BN',bn)
#io.write('POSCAR_Al',al)
