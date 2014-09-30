#!/usr/bin/python
mean_square_displacement=True
radial_distribution=True
out_file_type="pdf"



from scipy.spatial import distance as spdist
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
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
plot_ts_range = [150,100000]
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
   msdx = [ [(i*0.5473119623468868)/1000. for i in xrange(len(msd[f]))] for f in rng ]
   fig = plt.figure()
   ax = fig.add_subplot(111)
   ax.set_ylabel("Mean square displacement, $\\langle (r_0 - r(t))^2 \\rangle$")
   ax.set_xlabel("Time (picoseconds)")
   for i in rng:
      plt.plot(msdx[i], msd[i])
   plt.savefig('msd.{0}'.format(out_file_type))

if radial_distribution:
   #g(r) - Radial Distribution
   fig = plt.figure()
   ax = fig.add_subplot(111)
   ax.set_ylabel("Radial Distribution $g(r)$")
   ax.set_xlabel("Distance, angstroms")
   #ax.set_title("Radial Distribution")
   ax.set_xlim([0,6.0])
   ax.set_ylim([0,5.0])
   ax.axvline(x=2.6)
   for i in rng:
      gr,bins = xdat[i].radialDistribution_np(r[i],range(xdat[i].ntimesteps))
      plt.plot(bins,gr)
   plt.savefig('radialDistribution.{0}'.format(out_file_type))

lenss = []
n_z =[]
z_bins=[]
for iii in rng:
   timesteps = range(plot_ts_range[0], plot_ts_range[1] )
#Spatial Distribution (x,y)
   Nitrogens = xdat[iii].numpy_atoms('N', timesteps = [0], coordformat="Cartesian" )
   Borons    = xdat[iii].numpy_atoms('B', timesteps = [0], coordformat="Cartesian" )
   Aluminums = xdat[iii].numpy_atoms('Al', timesteps=timesteps ,coordformat="Cartesian" )
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
   fig = plt.figure(figsize=(4,4) ) #figsize=(6*1.5,4*1.5))
   ax = fig.add_subplot(111)  #subplot2grid((1, 15), (0, 0), colspan = 12)

   heatmap, xedges, yedges = np.histogram2d(Aluminums[:,0],Aluminums[:,1], bins=int(hist_res))
   extent = [0, xdat[iii].v[0], 0, xdat[iii].v[1]]
   extent = [np.min(Aluminums[:,0]),np.max(Aluminums[:,0]), np.min(Aluminums[:,1]), np.max(Aluminums[:,1]) ]


   vmin=0.0 / len(timesteps)
   vmax=300.0 / len(timesteps)
   heatmap = heatmap / float(len(timesteps))


   ax.imshow(heatmap.T, extent=extent, cmap=plt.get_cmap('OrRd'), origin='lower',alpha=1.0,vmin=vmin,vmax=vmax)

   print "Most full bin contains",np.max(heatmap),"aluminums"

   if plot_aluminums: plt.scatter(Aluminums[:,0],Aluminums[:,1], c='r',s=5, zorder=150, lw=0 )
   ax.scatter(Nitrogens[:,0],Nitrogens[:,1], c='g',s=15, zorder=100, alpha=0.5)
   ax.scatter(Borons[:,0], Borons[:,1], c='y',s=15, zorder=100, alpha=0.5)

   ax.grid(False)
   ax.set_xlim([extent[0],extent[1]])
   ax.set_ylim([extent[2],extent[3]])


#   plt.figtext(0.7,0.01,str(len(Aluminums))+" total Al atoms",zorder=10000)
#   ax.set_title("Spatial distribution in $x$ and $y$")
   ax.set_xlabel('$x$')
   ax.set_ylabel('$y$')

   plt.savefig('spatial_distribution_{0}.{1}'.format(infilelist[iii], out_file_type) )

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
   plt.savefig("zdistribution.{0}".format(out_file_type))



















import matplotlib.gridspec as gridspec




for iii in rng:
   bond_length=lattice_constant
   allN  =  np.array([])
   allB  =  np.array([])
   allNz =  np.array([])
   allBz =  np.array([])
   select_timestep = 400
#   for t in [400]:
   timesteps = xrange(plot_ts_range[0], plot_ts_range[1])
   for t in timesteps:
      if t >= xdat[iii].ntimesteps: break
      Nitrogens = xdat[iii].numpy_atoms('N', [t], coordformat="Cartesian" )
      Borons    = xdat[iii].numpy_atoms('B', [t], coordformat="Cartesian" )

      sheet_z = Nitrogens[Nitrogens[:,2] < 1.0]
      sheet_z = np.mean(sheet_z[:,2])
      sheet_zT = Nitrogens[Nitrogens[:,2] > 3.0]
      sheet_zT = np.mean(sheet_zT[:,2])

      Aluminums = xdat[iii].numpy_atoms('Al', [t], coordformat="Cartesian" )
      projN = Nitrogens; projN[:,2]=0 #project the nitrogens onto the XY plane
      projB = Borons; projB[:,2]=0    #project the borons onto the XY plane
      projA = Aluminums
      zAB = np.repeat(projA[:,2],len(projB),axis=0) #peel off the z-values, repeat so we can re-attach later
      zAN = np.repeat(projA[:,2],len(projN),axis=0) #peel off the z-values, repeat so we can re-attach later
      projA[:,2]=0  # project aluminums onto x-y plane
      distanceB = spdist.cdist(projB,projA).flatten() #calculate the distance from every Boron to every aluminum
      distanceN = spdist.cdist(projN,projA).flatten() #calculate the distance from every Nitro to every aluminum
      innt = 0.5 #half the bond length
      cutoff = bond_length*innt
      #remove any data points that are further from lattice atom than 1/2 lattice constant
      zAB = zAB[distanceB<cutoff]
      distanceB = distanceB[distanceB<cutoff]

      zAN = zAN[distanceN<cutoff]
      distanceN = distanceN[distanceN<cutoff]
      if t==select_timestep:
         selectN = distanceN
         selectB = distanceB
         selectNz = zAN
         selectBz = zAB
      allN = np.append(allN,distanceN)
      allB = np.append(allB,distanceB)
      allNz = np.append(allNz,zAN)
      allBz = np.append(allBz,zAB)

   gs1 = gridspec.GridSpec(1,2)
   gs1.update(wspace=0.0,hspace=0.0)

   fig = plt.figure(figsize=(6,4))

   axN = plt.subplot(gs1[0])
   axB = plt.subplot(gs1[1])

   heatmapN, xedgesN,yedgesN = np.histogram2d(allN, allNz, bins=(100,150))
   heatmapB, xedgesB,yedgesB = np.histogram2d(allB, allBz, bins=(100,150))
   TB = abs(xedgesN[1] - xedgesN[0]) #"thickness" of boron bins
   TN = abs(xedgesB[1] - xedgesB[0]) #thickness of nitrogen bins
   normN = len(timesteps) * np.abs(np.pi * (2.0*xedgesN * TN - TN**2)) #area of annulus of thickness TN and inner radius xedgesN
   normB = len(timesteps) * np.abs(np.pi * (2.0*xedgesB * TB - TB**2))

   extentN = [np.min(allN),np.max(allN), np.min(allNz), np.max(allNz) ]
   extentB = [np.min(allB),np.max(allB), np.min(allBz), np.max(allBz) ]

   heatmapN = np.swapaxes(np.swapaxes(heatmapN,0,1)/(normN[1:]),0,1)
   heatmapB = np.swapaxes(np.swapaxes(heatmapB,0,1)/(normB[1:]),0,1)
   absolute_max=max([np.max(heatmapN),np.max(heatmapB)]) / 25.
   absolute_min=min([np.min(heatmapN),np.min(heatmapB)])
   print absolute_max
   print absolute_min
   absolute_max = 1000.000 / len(timesteps)
   absolute_min = 0.000000 / len(timesteps)

   axN.imshow(heatmapN.T,extent=extentN,interpolation='None', cmap=plt.get_cmap('YlGnBu_r'), origin='lower',alpha=1.0, aspect='auto',vmin=absolute_min,vmax=absolute_max)
   axB.imshow(heatmapB.T,extent=extentB,interpolation='None', cmap=plt.get_cmap('YlGnBu_r'), origin='lower',alpha=1.0, aspect='auto',vmin=absolute_min,vmax=absolute_max)
#   axB.scatter(selectB,selectBz,c='r', edgecolor='r', s=20)
#   axN.scatter(selectN,selectNz,c='r', edgecolor='r', s=20)
   for ax in [axN,axB]:
      ax.set_axis_bgcolor('#081D58')
      ax.grid(False)
      ax.set_ylim([0,11])

   axB.set_xticks([cutoff,cutoff/2,0])
   axB.set_xticklabels(["1/2","1/4","B"])
   axN.set_xticks([0,cutoff/2,cutoff])
   axN.set_xticklabels(["N","1/4","1/2"])
   plt.axvline(x=cutoff,lw=3.0,c='k')
   axB.axhline(y=sheet_z,lw=3.,c='#3D5496')
   axN.axhline(y=sheet_z,lw=3.,c='#3D5496')
   axB.axhline(y=sheet_zT,lw=3.,c='#3D5496')
   axN.axhline(y=sheet_zT,lw=3.,c='#3D5496')
   axB.set_yticks([])
   axN.set_ylabel("$z$")
   axB.set_xlim([0.5*bond_length, 0])
   axN.set_xlim([0,0.5*bond_length])

   axB.spines['left'].set_visible(False)
   axN.spines['right'].set_visible(False)

   plt.annotate("BN sheet",(0.23,0.45), color='white')
   plt.savefig('sd_z_{0}.{1}'.format(infilelist[iii], out_file_type) )

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




