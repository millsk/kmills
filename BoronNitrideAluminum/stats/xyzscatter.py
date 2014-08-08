#!/usr/bin/python
import matplotlib.pyplot as plt
from vaspTools import XDATCAR
import mpltools.style as mplstyle
import time
import numpy as np
import os, sys
from scipy.spatial import distance as spdist
from matplotlib.colors import LogNorm
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


      innt = 1.0
      cutoff = bond_length*innt
      #remove any data points that are further from lattice atom than 1/2 lattice constant
      zAB = zAB[distanceB<cutoff]
      distanceB = distanceB[distanceB<cutoff]

      zAN = zAN[distanceN<cutoff]
      distanceN = distanceN[distanceN<cutoff]

      allN = np.append(allN,distanceN)
      allB = np.append(allB,distanceB)
      allNz = np.append(allNz,zAN)
      allBz = np.append(allBz,zAB)


   stretch=5
   fig = plt.figure(figsize=(6*1.5,4*1.5))
   ax = fig.add_subplot(111)


   heatmapN, xedgesN,yedgesN = np.histogram2d(allN, allNz, bins=100)
   heatmapB, xedgesB,yedgesB = np.histogram2d(allB, allBz, bins=100)

   TB = abs(xedgesN[1] - xedgesN[0]) #"thickness" of boron bins
   TN = abs(xedgesB[1] - xedgesB[0]) #thickness of nitrogen bins
   normN = np.abs(np.pi * (2.0*xedgesN * TN - TN**2)) #area of annulus of thickness TN and inner radius xedgesN
   normB = np.abs(np.pi * (2.0*xedgesB * TB - TB**2))
   extentN = [0 ,bond_length,0,10]
   extentB = [-bond_length,0,0,10]

   heatmapN = np.swapaxes(np.swapaxes(heatmapN,0,1)/(normN[:-1]),0,1)
   heatmapB = np.swapaxes(np.swapaxes(heatmapB,0,1)/(normB[:-1]),0,1)
   ax.imshow(heatmapN.T,extent=extentN, cmap=plt.get_cmap('YlGnBu'), origin='lower',alpha=1.0, aspect='auto')
   ax.imshow(heatmapB.T,extent=extentB, cmap=plt.get_cmap('YlGnBu_r'), origin='lower',alpha=1.0, aspect='auto')





   ax.grid(False)
#   ax.set_xlim([0,1])
#   ax.set_xticks([-lattice_constant*stretch, 0, lattice_constant*stretch])
#   ax.set_xticklabels(["lv/2","B  N","lv/2"])

   plt.figtext(0.7,0.01,str(len(allBz))+" total Al atoms",zorder=10000)
   ax.set_title("Spatial distribution")
   ax.set_xlabel('Distance from lattice atom (Nitrogen on left)')
   ax.set_ylabel('$z$')

   plt.savefig('spatial_distribution_{0}.png'.format(infilelist[iii]) )



