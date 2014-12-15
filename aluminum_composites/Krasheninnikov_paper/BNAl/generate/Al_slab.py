from ase.lattice.surface import fcc111
from ase.lattice.hexagonal import Graphene
from ase import io
import math

lattice_constant_Al = 4.050
a_lattice_constant_BN = 2.5040
c_lattice_constant_BN = 6.6612

slab = fcc111('Al',size=(7,7,3), a=lattice_constant_Al)

#bn = Hexagonal('B',size=(8,8,1), latticeconstant={'a':1.446, 'c':1.446})
#bn = fcc111('B',size=(8,8,1), a=a_lattice_constant_BN, vacuum=6.0)
bn = Graphene(symbol='B', size=(8,8,1), latticeconstant={'a':a_lattice_constant_BN, 'c': c_lattice_constant_BN})
print "BN: Num atoms: ",bn.get_number_of_atoms()
#bn.set_chemical_symbols( [ 'B' if i%2==0 else 'N' for i in range(bn.get_number_of_atoms()) ]   )

positions = bn.get_positions()

new_positions=[]
maxx = -10000000
maxy = -10000000
for i in range(len(positions)):
   new_positions.append([-positions[i][1], -positions[i][0],positions[i][2]])
   if positions[i][0] > maxx: maxx = positions[i][0]
   if positions[i][1] > maxy: maxy = positions[i][1]

new_positions = [ [-positions[i][1], -positions[i][0],positions[i][2]] for i in range(len(positions)) ]

bn.set_positions(new_positions)

bn.rotate('z',math.pi/2)
print maxx, maxy

bn.translate([maxx,maxy,0])


io.write('POSCAR_BN',bn)
io.write('POSCAR_Al',slab)
