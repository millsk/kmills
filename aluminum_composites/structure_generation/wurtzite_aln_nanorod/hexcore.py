#!/usr/bin/python
import numpy as np
import ase.io.vasp
from scipy.spatial.distance import pdist
from math import pi
import math
import sys


filename = "POSCAR_bulk"

size = int(sys.argv[1])  #distance from center to node of polygon
polygon_sides = 6  #hexagon


poscar = ase.io.vasp.read_vasp(filename)

for i in dir(poscar):
   print i

cell = poscar.get_cell()

#the lattice vectors
a1 = np.array(cell[0])
a2 = np.array(cell[1])
a3 = np.array(cell[2])

#The center of the cell is the half way point of each lattice vector, added together.
center = (a1+a2)/2.
print center

center = center[:2]
print center
o = np.array(poscar._get_positions())[:,:2]
print o

closest_dist = 9999999999.

for atom in o:
   if np.linalg.norm((atom-center)) < closest_dist:
      closest = atom
      closest_dist = np.linalg.norm((atom-center))


print "the closest atom to the center is at ",closest,", a distance of ",closest_dist,"away."
node = (closest - center) * 1.05 * closest_dist * size

nodes = []


theta = 2*pi / polygon_sides

print "Hexagon vertices:"
for n in range(polygon_sides):
   rot_matr = np.matrix( [ [ math.cos(n*theta), -math.sin(n*theta)],[ math.sin(n*theta), math.cos(n*theta) ] ] )
   new = np.array([node[0],node[1]]) * rot_matr + [center[0],center[1]]
   print new
   nodes = nodes + [[ new.item(0), new.item(1) ]]
#   nodes = np.concatenate( nodes,  new[0]  ) 
#nodes = np.append(nodes, rot_matr*node)


def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside






del poscar[ [ atom.index for atom in poscar if not point_in_poly(atom.position[0],atom.position[1],nodes) ]]


print len(poscar._get_positions())," atoms left"


#for i,atom in enumerate(poscar._get_positions()):
#   if not(point_in_poly(atom[0],atom[1],nodes)):
#      print i,atom
#      #del poscar[i]


ase.io.write('POSCAR_{0}'.format(size),poscar,format='vasp')






