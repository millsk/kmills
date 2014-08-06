#!/usr/bin/python
import matplotlib.pyplot as plt
from vaspTools import XDATCAR
import mpltools.style as mplstyle
import time
import numpy as np
import os
mplstyle.use('ggplot')
xdat = XDATCAR.read('XDATCAR')


####################################
#HISTOGRAM OPTIONS
plot_ts_range = [0,10000]
plot_z_range = [-100,100]
plot_aluminums=False
hist_res = 27*3 #number of histogram bins along each axis
wrap_in=True
lattice_constant = 1.446
#####################################

#MSD
r = xdat.numpynd_atoms('Al', 'all', coordformat="Cartesian" )
msd = xdat.msd(r)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylabel("Mean square displacement, $\\langle (r_0 - r(t))^2 \\rangle$")
ax.set_xlabel("Time, $t$  $(\\times 0.543\\mathrm{fs})$")
ax.set_title("Mean squared displacement of Aluminum")
plt.plot(msd)
plt.savefig('msd.png')


#g(r) - Radial Distribution
gr,bins = xdat.radialDistribution_np(r,range(xdat.ntimesteps))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylabel("Radial Distribution $g(r)$")
ax.set_xlabel("Distance, angstroms")
ax.set_title(xdat.comment)
plt.plot(bins,gr)
ax.set_xlim([0,6.0])
ax.set_ylim([0,5.0])
ax.axvline(x=2.6)
plt.savefig('radialDistribution.png')



#Spatial Distribution (x,y)
Nitrogens = xdat.numpy_atoms('N', [0], coordformat="Cartesian" )
Borons    = xdat.numpy_atoms('B', [0], coordformat="Cartesian" )
Aluminums = xdat.numpy_atoms('Al', 'all', coordformat="Cartesian" )


if wrap_in:
   print "Wrapping..."
   temp = Aluminums
   for dx in range(1,int(round(xdat.v[0] / (3*lattice_constant),0))):
      temp = np.vstack((temp, np.add(Aluminums,[lattice_constant*dx*3,0,0])))
   Aluminums = temp
   temp = Aluminums
   for dy in range(1,int(round(xdat.v[1] / (np.sqrt(3)*lattice_constant),0))):
      temp = np.vstack((temp, np.add(Aluminums,[0,lattice_constant*dy*np.sqrt(3),0])))
   Aluminums = temp
   Aluminums[Aluminums[:,0]>xdat.v[0]]-=[xdat.v[0],0,0]
   Aluminums[Aluminums[:,1]>xdat.v[1]]-=[0,xdat.v[1],0]



fig = plt.figure() #figsize=(6*1.5,4*1.5))
ax = fig.add_subplot(111)  #subplot2grid((1, 15), (0, 0), colspan = 12)

heatmap, xedges, yedges = np.histogram2d(Aluminums[:,0],Aluminums[:,1], bins=int(hist_res))
extent = [0, xdat.v[0], 0, xdat.v[1]]


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

plt.savefig('spatial_distribution.png')

print "    --> Only plotting aluminums between z =",plot_z_range[0],"and z = ", plot_z_range[1]

fig = plt.figure()
ax = fig.add_subplot(111)
n_z,bins = np.histogram(Aluminums[:,2], bins=500, density=True)
extent = [0, 1, min(yedges), max(yedges)]
ax.set_title("Aluminum Distribution, $z$-axis")
ax.set_xlabel("$z$ position")
ax.set_ylabel("Probability")

plt.plot(bins[1:],n_z/len(Aluminums[:,2]))

plt.savefig('zdistribution.png')


