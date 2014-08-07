#!/usr/bin/python
import matplotlib.pyplot as plt
from vaspTools import XDATCAR
import mpltools.style as mplstyle
import time
import numpy as np
import os, sys
from scipy.spatial import distance as spdist
mplstyle.use('ggplot')

infilelist = sys.argv[1].split()

xdat = [ XDATCAR.read(i) for i in infilelist ]
rng = xrange(len(xdat))

lattice_constant = 1.446
bond_length = lattice_constant

r = [ xdat[i].numpynd_atoms('Al', 'all', coordformat="Cartesian" ) for i in rng ]

for iii in rng:

#Spatial Distribution (x,y)
   allN  =  np.array([])
   allB  =  np.array([])
   allNz =  np.array([])
   allBz =  np.array([])

   for t in xrange(xdat[iii].ntimesteps):
      Nitrogens = xdat[iii].numpy_atoms('N', [t], coordformat="Cartesian" )
      Borons    = xdat[iii].numpy_atoms('B', [t], coordformat="Cartesian" )
      Aluminums = xdat[iii].numpy_atoms('Al', [t], coordformat="Cartesian" )

      projN = Nitrogens; projN[:,2]=0 #project the nitrogens onto the XY plane
      projB = Borons; projB[:,2]=0    #project the borons onto the XY plane
      projA = Aluminums
      zAB = np.repeat(projA[:,2],len(projB),axis=0) #peel off the z-values, repeat so we can re-attach later
      zAN = np.repeat(projA[:,2],len(projN),axis=0) #peel off the z-values, repeat so we can re-attach later
      projA[:,2]=0  # project aluminums onto x-y plane
      distanceB = spdist.cdist(projB,projA).flatten() #calculate the distance from every Boron to every aluminum
      distanceN = spdist.cdist(projN,projA).flatten() #calculate the distance from every Nitro to every aluminum

      innt = 0.5
      #remove any data points that are further from t
      zAB = zAB[distanceB<bond_length*innt]
      distanceB = distanceB[distanceB<bond_length*innt]

      zAN = zAN[distanceN<bond_length*innt]
      distanceN = distanceN[distanceN<bond_length*innt]

      allN = np.append(allN,distanceN)
      allB = np.append(allB,distanceB)
      allNz = np.append(allNz,zAN)
      allBz = np.append(allBz,zAB)



   stretch=5
   fig = plt.figure(figsize=(6*1.5,4*1.5))
   ax = fig.add_subplot(111)

   print len(allN)
   print len(allB)

   toPlot = np.append(bond_length - allN,   -(bond_length-allB))
#   toPlot = allN
   toPlotZ = np.append(allNz,allBz)
 #  toPlotZ = allNz
   heatmapN, xedgesN,yedgesN = np.histogram2d(allN,allNz, bins=60)
   heatmapB, xedgesB, yedgesB = np.histogram2d(allB,allBz, bins=60)
   extentB = [0,lattice_constant*stretch,0,10]
   extentN = [-lattice_constant*stretch,0,0,10]

#   extent = [min(xedges),max(xedges),min(yedges),max(yedges) ]


   ax.imshow(np.fliplr(heatmapB.T),extent=extentB, cmap=plt.get_cmap('YlGnBu_r'), origin='lower',alpha=1.0)
   ax.imshow(heatmapN.T,extent=extentN, cmap=plt.get_cmap('YlGnBu_r'), origin='lower',alpha=1.0)
   ax.axvline(x=0, c='k', linewidth=10)
#   ax.scatter(allN,  allNz,  c='g',s=25, zorder=100, alpha=0.7)
#   ax.scatter(-allB, allBz, c='y',s=25, zorder=100, alpha=0.7)


   ax.grid(False)
   ax.set_xticks([-lattice_constant*stretch, 0, lattice_constant*stretch])
   ax.set_xticklabels(["B","0","N"])
   plt.figtext(0.7,0.01,str(len(toPlot))+" total Al atoms",zorder=10000)
   ax.set_title("Spatial distribution")
   ax.set_xlabel('Distance from lattice atom (Nitrogen on left)')
   ax.set_ylabel('$z$')

   plt.savefig('spatial_distribution_{0}.png'.format(infilelist[iii]) )



