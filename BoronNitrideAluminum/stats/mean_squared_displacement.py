#!/usr/bin/python
import matplotlib.pyplot as plt
from vaspTools import XDATCAR
import mpltools.style as mplstyle

mplstyle.use('ggplot')



xdat = XDATCAR.read('XDATCAR_big')




#r = xdat.numpynd_atoms('Al', 'all',   coordformat="Cartesian" )
#xdat.animate_xy_projection(r,True)

r = xdat.numpynd_atoms(['O'], 'all', coordformat="Cartesian" )
msd = xdat.msd(r)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_ylabel("Mean square displacement, $\\langle (r_0 - r(t))^2 \\rangle$")
ax.set_xlabel("Time, $t$  $\\left(\\times 0.543$fs\\right\)")
ax.set_title(xdat.comment)
plt.plot(msd)
plt.savefig('msd.png')


