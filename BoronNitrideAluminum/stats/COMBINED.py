#!/usr/bin/python

mean_square_displacement=True
radial_distribution=True

import matplotlib.pyplot as plt
from vaspTools import XDATCAR
import mpltools.style as mplstyle
import time
import numpy as np
import os, sys
mplstyle.use('ggplot')

infilelist = sys.argv[1].split()

xdat = [ XDATCAR.read(i) for i in infilelist ]
rng = xrange(len(xdat))

####################################
#HISTOGRAM OPTIONS
plot_ts_range = [200,100000]
plot_z_range = [-1000,1000]
plot_aluminums=False
hist_res = 28*3 #number of histogram bins along each axis
wrap_in=False #copy all aluminums periodically in space (data garbage if lattice not symmetric)
lattice_constant = 1.446
#####################################

r = [ xdat[i].numpynd_atoms('Al', 'all', coordformat="Cartesian" ) for i in rng ]

if mean_square_displacement:
   #MSD
   msd = [ xdat[i].msd(r[i]) for i in rng ]
   fig = plt.figure()
   ax = fig.add_subplot(111)
   ax.set_ylabel("Mean square displacement, $\\langle (r_0 - r(t))^2 \\rangle$")
   ax.set_xlabel("Time, $t$  $(\\times 0.543\\mathrm{fs})$")
   ax.set_title("Mean squared displacement of Aluminum")
   for i in rng:
      plt.plot(msd[i])
   plt.savefig('msd.png')

if radial_distribution:
   #g(r) - Radial Distribution
   fig = plt.figure()
   ax = fig.add_subplot(111)
   ax.set_ylabel("Radial Distribution $g(r)$")
   ax.set_xlabel("Distance, angstroms")
   ax.set_title("Radial Distribution")
   ax.set_xlim([0,6.0])
   ax.set_ylim([0,5.0])
   ax.axvline(x=2.6)
   for i in rng:
      gr,bins = xdat[i].radialDistribution_np(r[i],range(xdat[i].ntimesteps))
      plt.plot(bins,gr)
   plt.savefig('radialDistribution.png')

lenss = []
n_z =[]
z_bins=[]
for iii in rng:

#Spatial Distribution (x,y)
   Nitrogens = xdat[iii].numpy_atoms('N', timesteps = [0], coordformat="Cartesian" )
   Borons    = xdat[iii].numpy_atoms('B', timesteps = [0], coordformat="Cartesian" )
   Aluminums = xdat[iii].numpy_atoms('Al', range(plot_ts_range[0], plot_ts_range[1] ) ,coordformat="Cartesian" )
   if wrap_in:
      temp = Aluminums
      for dx in range(1,int(round(xdat[iii].v[0] / (3*lattice_constant),0))):
         temp = np.vstack((temp, np.add(Aluminums,[lattice_constant*dx*3,0,0])))
      Aluminums = temp
      temp = Aluminums
      for dy in range(1,int(round(xdat[iii].v[1] / (np.sqrt(3)*lattice_constant),0))):
         temp = np.vstack((temp, np.add(Aluminums,[0,lattice_constant*dy*np.sqrt(3),0])))
      Aluminums = temp
      Aluminums[Aluminums[:,0]>xdat[iii].v[0]]-=[xdat[iii].v[0],0,0]
      Aluminums[Aluminums[:,1]>xdat[iii].v[1]]-=[0,xdat[iii].v[1],0]


   Aluminums = Aluminums[(Aluminums[:,2]>plot_z_range[0]) & (Aluminums[:,2]<plot_z_range[1]   )]
   fig = plt.figure() #figsize=(6*1.5,4*1.5))
   ax = fig.add_subplot(111)  #subplot2grid((1, 15), (0, 0), colspan = 12)

   heatmap, xedges, yedges = np.histogram2d(Aluminums[:,0],Aluminums[:,1], bins=int(hist_res))
   extent = [0, xdat[iii].v[0], 0, xdat[iii].v[1]]


   ax.imshow(heatmap.T, extent=extent, cmap=plt.get_cmap('YlOrRd'), origin='lower',alpha=1.0)
   if plot_aluminums: plt.scatter(Aluminums[:,0],Aluminums[:,1], c='r',s=5, zorder=150, lw=0 )
   ax.scatter(Nitrogens[:,0],Nitrogens[:,1], c='g',s=25, zorder=100, alpha=0.7)
   ax.scatter(Borons[:,0], Borons[:,1], c='y',s=25, zorder=100, alpha=0.7)

   ax.grid(False)
   ax.set_xlim([extent[0],extent[1]])
   ax.set_ylim([extent[2],extent[3]])


   plt.figtext(0.7,0.01,str(len(Aluminums))+" total Al atoms",zorder=10000)
   ax.set_title("Spatial distribution in $x$ and $y$")
   ax.set_xlabel('$x$')
   ax.set_ylabel('$y$')

   plt.savefig('spatial_distribution_{0}.png'.format(infilelist[iii]) )

   print "    --> Only plotting aluminums between z =",plot_z_range[0],"and z = ", plot_z_range[1]


   #Store the z-distribution information for plotting on a combined plot later
   t1,t2 = np.histogram(Aluminums[:,2], bins=100, density=True)
   n_z.append(t1)
   z_bins.append(t2)
   lenss.append(len(Aluminums[:,2]) )


fig = plt.figure()
ax = fig.add_subplot(111)

extent = [0, 1, min(yedges), max(yedges)]
ax.set_title("Aluminum Distribution, $z$-axis")
ax.set_xlabel("$z$ position")
ax.set_ylabel("Probability")


for i in rng:
   plt.plot(z_bins[i][1:],n_z[i]/lenss[i] )
   plt.savefig("zdistribution.png")



import string
names = [ string.replace(infilelist[i], '_', '\\_') for i in rng ]

print names

#Make a legend
import pylab
fig = pylab.figure()
figlegend = pylab.figure(figsize=(3,2))
ax = fig.add_subplot(111)
f = (range(10), pylab.randn(10)) * len(infilelist)
lines = ax.plot(f)
figlegend.legend(lines, names, 'center')
figlegend.savefig('legend.png')




