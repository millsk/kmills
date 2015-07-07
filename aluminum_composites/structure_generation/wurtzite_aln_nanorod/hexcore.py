#!/usr/bin/python
import numpy as np
import ase.io.vasp
from scipy.spatial.distance import pdist
from math import pi
import math
import sys


filename = "bulk.dat"

#size = int(sys.argv[1])  #distance from center to node of polygon
polygon_sides = 6  #hexagon


#define outer/inner diameters.  They will be changed slightly 
outer_diameter = 330.
inner_diameter = 0.







poscar = ase.io.vasp.read_vasp(filename)

cell = poscar.get_cell()

#the lattice vectors
a1 = np.array(cell[0])
a2 = np.array(cell[1])
a3 = np.array(cell[2])

#The center of the cell is the half way point of each lattice vector, added together.
center = (a1+a2)/2.
print "Center of cell: ",center
center = center[:2]

#original list of atoms (all, before removal)
o = np.array(poscar._get_positions())[:,:2]

#Find the closest atom to the center.  This is the "hexagon size"
closest_dist = 9999999999.
for atom in o:
   if np.linalg.norm((atom-center)) < closest_dist:
      closest = atom
      closest_dist = np.linalg.norm((atom-center))
print "the closest atom to the center is at ",closest,", a distance of ",closest_dist,"away."

size_outer = int((outer_diameter/2.0) / closest_dist)/math.sqrt(3)
size_inner = int((inner_diameter/2.0) / closest_dist)/math.sqrt(3)
print size_outer



outer_node = (closest - center) * 1.05 * closest_dist * size_outer

print "outer node is a distance away from center of: ",np.linalg.norm((outer_node-center))

#inner_node = (closest - center) * 1.05 * closest_dist * int((inner_diameter/2.0)/closest_dist)

inner_node = (closest - center) * 1.05 * closest_dist * size_inner

print  "outer_node,inner_node:  ", outer_node,inner_node


def build_polygon(tcenter,tnode,tpolygon_sides):
  print "build_polygon() called with params: ", tcenter, tnode, tpolygon_sides, "."
  #Build the polygon mask:
  nodes = []
  theta = 2*pi / tpolygon_sides
  print "Hexagon vertices:"
  for n in range(tpolygon_sides):  #for each vertex... 
     rot_matr = np.matrix( [ [ math.cos(n*theta), -math.sin(n*theta)],[ math.sin(n*theta), math.cos(n*theta) ] ] )
     new = np.array([tnode[0],tnode[1]]) * rot_matr + [tcenter[0],tcenter[1]]
     print new
     nodes = nodes + [[ new.item(0), new.item(1) ]]
  return nodes




#Function to determine if point lies inside polygon
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



outside_border = build_polygon(center,outer_node,polygon_sides)
inside_border = build_polygon(center,inner_node,polygon_sides)

del poscar[ [ atom.index for atom in poscar if not point_in_poly(atom.position[0],atom.position[1],outside_border) ]]
del poscar[ [ atom.index for atom in poscar if point_in_poly(atom.position[0],atom.position[1],inside_border) ]]



print len(poscar._get_positions())," atoms left"


#for i,atom in enumerate(poscar._get_positions()):
#   if not(point_in_poly(atom[0],atom[1],nodes)):
#      print i,atom
#      #del poscar[i]


ase.io.write('POSCAR_{0}'.format(outer_diameter),poscar,format='vasp')






