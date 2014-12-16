from ase.lattice.surface import fcc111
from ase.lattice.hexagonal import *
from ase import io
import math

lattice_constant_Al = 4.050
a_lattice_constant_BN = 2.5040
c_lattice_constant_BN = 6.6612

slab = fcc111('Al',size=(7,6,3), a=lattice_constant_Al, orthogonal=True)

#bn = Hexagonal('B',size=(8,8,1), latticeconstant = {'a':1.446, 'c':1.446})
#bn = fcc111('B',size=(8,8,1), a=1.5*a_lattice_constant_BN, vacuum=6.0,orthogonal=True)

#Need to somehow get orthographic coordinates for bn sheet

bn = Graphene(symbol='B', size=(8,8,3), latticeconstant={'a':a_lattice_constant_BN, 'c': c_lattice_constant_BN})


io.write('POSCAR_BN',bn,format='xyz')
io.write('POSCAR_Al',slab,format='xyz')



io.write('POSCAR_BN',bn)
io.write('POSCAR_Al',slab)
