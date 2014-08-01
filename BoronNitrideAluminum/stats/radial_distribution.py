#!/usr/bin/python
import matplotlib.pyplot as plt
from vaspTools import XDATCAR
import mpltools.style as mplstyle
import time
import numpy as np
mplstyle.use('ggplot')

xdat = XDATCAR.read('XDATCAR_test')
#r = xdat.numpynd_atoms('Al', 'all',   coordformat="Cartesian" )
#xdat.animate_xy_projection(r,True)
r = xdat.numpynd_atoms('Al', 'all', coordformat="Cartesian" )
stime = time.time()
gr,bins = xdat.radialDistribution_np(r,range(2,300))
print "Time=", time.time()-stime
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylabel("Radial Distribution $g(r)$")
ax.set_xlabel("Distance, angstroms")
ax.set_title(xdat.comment)

print np.shape(bins)
print np.shape(gr)


plt.plot(bins,gr)
plt.savefig('radialDistribution.png')


