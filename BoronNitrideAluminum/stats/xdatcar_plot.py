#!/usr/bin/python
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import matplotlib.artist as art
import matplotlib.colors as pltcolor
from os import system,path
import itertools as it
import time
import getopt
import os
from vaspTools import XDATCAR


plot_ts_range = [0,10000]
plot_z_range = [-100,100]
plot_aluminums=False
hist_res = 2.0*27 #number of histogram bins along each axis
wrap_in=False
lattice_constant = 1.446

try:
   opts, args = getopt.getopt(sys.argv[1:], 'z:t:w',["zrange=","trange=","wrap="])
except getopt.GetoptError:
   print "ARGUMENT ERROR: invalid",opts,"given"
   sys.exit(2)
for opt, arg in opts:
   if opt in ('-z', '--zrange'):
      plot_z_range=[float(arg.split()[0]), float(arg.split()[1]) ]
      print "z range specified as",plot_z_range
   elif opt in ('-t', '--trange'):
      plot_ts_range = [float(arg.split()[0]), float(arg.split()[1]) ]
   elif opt in ('-a', '--aluminums'):
      plot_aluminums=True
   elif opt in ('-w', '--wrap'):
      wrap_in = True




xdat = XDATCAR.read('XDATCAR')
print "File read in ",xdat.readtime,"seconds"

Nitrogens = xdat.numpy_atoms('N', [0], coordformat="Cartesian" )
Borons    = xdat.numpy_atoms('B', [0], coordformat="Cartesian" )
Aluminums = xdat.numpy_atoms('Al', 'all', coordformat="Cartesian" )


fig = plt.figure(figsize=(6*1.5,4*1.5))
ax = plt.subplot2grid((1, 15), (0, 0), colspan = 12)
ax2 = plt.subplot2grid((1, 15), (0, 13), colspan = 3)

heatmap, xedges, yedges = np.histogram2d(Aluminums[:,0],Aluminums[:,1], bins=int(hist_res))
extent = [0, xdat.v[0], 0, xdat.v[1]]


ax.imshow(heatmap.T, extent=extent, cmap=plt.get_cmap('YlOrRd'), origin='lower',alpha=1.0)
if plot_aluminums: plt.scatter(Aluminums[:,0],Aluminums[:,1], c='r',s=5, zorder=150, lw=0 )
ax.scatter(Nitrogens[:,0],Nitrogens[:,1], c='g',s=15, zorder=100, alpha=0.7)
ax.scatter(Borons[:,0], Borons[:,1], c='y',s=15, zorder=100, alpha=0.7)

ax.set_xlim([extent[0],extent[1]])
ax.set_ylim([extent[2],extent[3]])


plt.figtext(0.7,0.01,str(len(Aluminums))+" total Al atoms",zorder=10000)
ax.set_title(os.getcwd().split('/')[len(os.getcwd().split('/'))-1] + "  $({0} \leq z < {1} )$ ".format(plot_z_range[0], plot_z_range[1])   )
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')

print "    --> Only plotting aluminums between z =",plot_z_range[0],"and z = ", plot_z_range[1]



heatmap, xedges, yedges = np.histogram2d(np.ones(len(Aluminums)),Aluminums[:,2], bins=(1,int(hist_res/2)))
extent = [0, 1, min(yedges), max(yedges)]

ax2.set_ylabel('$z$')
ax2.set_xticks([])
ax2.set_ylim([0,xdat.v[2] ])

ax2.imshow(heatmap.T, extent=extent, cmap=plt.get_cmap('OrRd'), origin='lower',alpha=1.0)
plt.savefig('histogram.png')


