from ase.lattice.surface import fcc111,hcp0001
from ase.lattice.hexagonal import *
from ase import io
import math

lattice_constant_Al = 4.050
a_lattice_constant_BN = 2.5040
c_lattice_constant_BN = 6.6612

slab = fcc111('Al',size=(7,7,3), a=lattice_constant_Al, orthogonal=False,vacuum=20.0)
bn= hcp0001('B',size=(8,8,2), a=a_lattice_constant_BN, c=0.0000001, vacuum=20.0)
bn.translate([0,0,-5])

num_each = bn.get_number_of_atoms() / 2

bn.set_atomic_numbers([5]*num_each + [7]*num_each)




bn.extend(slab)


io.write('POSCAR',bn)
