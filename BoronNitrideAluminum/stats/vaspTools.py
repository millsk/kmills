#!/usr/bin/python
import time
import numpy as np
from matplotlib import pyplot as plt
from timeit import timeit

class io:
   def task(self, message):
      print  message
   def status(self, message):
      print "   --> ",message
   def warning(self,message):
      print "WARNING:\t",message
screen=io()

#Read in an XDATCAR
class XDATCAR:
   class read:
      def __init__(self,filename):
         screen.task("File read")
         stime = time.time()
         screen.status("Opening file")
         temp = open(filename,'r')
         f = [line.split() for line in temp]
         temp.close()
         self.comment = f.pop(0)[0] #first line is a comment; get rid of it.
         self.scaling_factor = f.pop(0) #Second line is scaling factor
         self.v = [ float(f[0][0]), float(f[1][1]), float(f[2][2]) ]  #lattice vector.
         [f.pop(0) for _ in (1,2,3) ]
         self.list_atoms = f.pop(0)
         self.count_atoms = [int(i) for i in f.pop(0) ]
         self.total_atoms = int(sum(self.count_atoms))
         self.ntimesteps = sum( [  1 if (i==[] or i[0]=='Direct') else 0 for i in f ])
         self.atom_array = [ [] for _ in range(len(self.count_atoms)) ]
         self.timestep_array = [ [ [] for _ in range(len(self.count_atoms)) ] for _ in range(self.ntimesteps) ]
         f.pop(0)
         count = 0
         pointer=0
         screen.status("Filling lists")
         for timestep in xrange(self.ntimesteps): #For timestep in remaining timesteps 
            for atom_type,atom_count in enumerate(self.count_atoms):
               for atom_index in range(atom_count):
                  if (not len(f[pointer])==0) and 0==sum( [1 if 'Direct' in i else 0 for i in f[pointer]]):
#                     self.atom_array[atom_type].append([float(i) for i in f[pointer] ])
                     self.timestep_array[timestep][atom_type].append([float(i) for i in f[pointer] ])
                  pointer+=1
            pointer+=1
         self.readtime = time.time() - stime
         self.lattice_x = self.v[0]
         self.lattice_y = self.v[1]
         self.lattice_z = self.v[2]
         self.unwrapped_coords = "not unwrapped"
         f = "nothing"

      def get_atom_index(self,symbol):
         return self.list_atoms.index(symbol)


      def get_atom_count(self, index):
         return self.count_atoms[index]


      def numpy_atoms(self, atom_type=0, timesteps=[0], indices='default', coordformat='C'):
         #returns a numpy array
         if isinstance(atom_type,basestring):
            atom_type=self.get_atom_index(atom_type)
         if indices=='default':
            indices=range(self.count_atoms[atom_type])
         if timesteps[0]=='A' or timesteps[0]=='a':
            timesteps = range(self.ntimesteps)
         return_list = []
         for t in timesteps:
            for i in indices:
               return_list.append(self.timestep_array[t][atom_type][i])
         return_list = np.array(return_list)
         if coordformat[0]=='C':
            return_list = return_list * self.v
         return return_list


      def numpynd_atoms(self, atom_type=0, timesteps=[0], indices='default', coordformat='C'):
         #returns a numpy array
         if isinstance(atom_type,basestring):
            atom_type=self.get_atom_index(atom_type)
         if indices=='default':
            indices=range(self.count_atoms[atom_type])
         if timesteps[0]=='A' or timesteps[0]=='a':
            timesteps = range(self.ntimesteps)
         stime = time.time()
         array = np.zeros(shape=(len(timesteps),len(indices),3))
         screen.task("Filling multidimensional array")
         for t in xrange(len(timesteps)):
            for i in xrange(len(indices)):
               array[t,i] = self.timestep_array[timesteps[t]][atom_type][indices[i]]
         if coordformat[0]=='C':
            array = array*self.v
         return array


      def unwrap_legacy(self, a): #slow but I'm sure it works
      #     usage something like:  
      #        xdat.unwrap(xdat.numpynd_atoms('Al', 'all', coordformat="Cartesian" ))
      #     Also creates an attribute with the unwrapped coordinates for later reference without recalculation
         stime=time.time()
         screen.task("Unwrapping coordinates")
         delta = np.array([10]); count = 0
         lattice = np.zeros(np.shape(a));  lattice[:,:]=self.v
         while len(delta[np.abs(delta) > 1.0])>0:
            timeshift=np.insert(a,0,a[0],axis=0)[:-1]
            delta = timeshift - a
            a = np.where(delta<-lattice/2.0,a-lattice,np.where(delta>lattice/2.0,a+lattice,a))
         self.unwrap_time = time.time()-stime
         self.unwrapped_coords = a
         return a

      def unwrap(self, a):
      #     usage something like:  
      #        xdat.unwrap(xdat.numpynd_atoms('Al', 'all', coordformat="Cartesian" ))
      #     Also creates an attribute with the unwrapped coordinates for later reference without recalculation
         if not self.unwrapped_coords == "not unwrapped":
            return self.unwrapped_coords
         stime=time.time()
         screen.task("Unwrapping coordinates")
         dr = np.diff(a, axis=0)  #Calculate the derivative of the position. Large spikes mean they wrap
         zeros = np.zeros(np.shape(dr))
         dr=new=np.where(np.abs(dr)<0.5,zeros,np.where(dr<0,zeros+1,zeros-1))
         screen.status("Shifting derivative mask over time")
         for i in xrange(1,len(a) + 100):
            rolled = np.roll(dr,i,axis=0)
            rolled[0:i]=0
            temp = rolled+new
            if i%100==0:
                #I don't need to compare 1M element arrays each time. C
               #Comparison will be slower than doing a few extra iterations 
               if np.array_equal(new, temp): break
            new = temp
         dr = new*self.v
         a = dr + a[1:]
         """ #Just a sanity check...dont need it.
         x = []
         y = []
         for i,data in enumerate(a):
            x.append(i)
            y.append(data[73][0]) #I know that atom 73 of test file needs wrapped
            print data[73]
         self.simpleplot(x,y)
         """
         self.unwrap_time = time.time()-stime
         self.unwrapped_coords = a
         screen.status("Unwrapped in "+str(self.unwrap_time)+"s")
         return a

      def msd(self, a):
         r = self.unwrap(a) #unwrap the coordinates
         screen.task("Calculating mean-square displacement")
         delta_r = r-r[0] #(r[0]-COM[0])-(r-COM)
         distance = np.sum(delta_r**2,axis=2)
         return np.mean(distance,axis=1)

      def periodic_copy(self,a):
         print np.shape(a)
         screen.task("Copying atoms to adjacent cells (PBC)")
         a = np.hstack((a,a+[self.lattice_x,0,0],a-[self.lattice_x,0,0]))
         a = np.hstack((a,a+[0,self.lattice_y,0],a-[0,self.lattice_y,0]))
         a = np.hstack((a,a+[0,0,self.lattice_z],a-[0,0,self.lattice_z]))
         return a

      def radialDistribution(self, a, tt):
         r = []
         xh = self.v[0] / 2.0
         yh = self.v[1] / 2.0
         zh = self.v[2] / 2.0
         for t in tt:
            print "Time={0}".format(t)
            for atom1 in a[t]:
               for atom2 in a[t]:
                  distance_x = abs(atom2[0] - atom1[0])
                  distance_y = abs(atom2[1] - atom1[1])
                  distance_z = abs(atom2[2] - atom1[2])
                  if distance_x > self.v[0] / 2.0: distance_x = self.v[0] - distance_x
                  if distance_y > self.v[1] / 2.0: distance_y = self.v[1] - distance_y
                  if distance_z > self.v[2] / 2.0: distance_z = self.v[2] - distance_z
                  r.append(distance_x**2 + distance_y**2 + distance_z**2)
         print min(r)
         print np.sqrt(max(r))
         r = np.array(r)
         r = np.sqrt(r)
         r = r[ np.nonzero(r)]
         print r
         gr,bins = np.histogram(r,100)
         gr = gr/float(len(r))
         return gr,bins





      def writeOut(self,fname,a):
         f = open(fname,'w')
         for timestep in a:
            for atom in timestep:
               for coordinate in atom:
                  f.write(str(coordinate) + "  ")
               f.write("\n")
            f.write("\n")
         f.close()

      def animate_xy_projection(self, a, unwrap=0, projection_axis=2):
         def axis_pad(lim = [0,1,0,1],percent=0.1):
            x = [ lim[0], lim[1] ]
            y = [ lim[2], lim[3] ]
            dx = abs(x[1] - x[0])*percent
            dy = abs(y[1] - y[0])*percent
            return [ x[0]-dx, x[1]+dx], [ y[0]-dy, y[1]+dy]
         axes = [0,1,2]; axes_label=['x','y','z']
         axes.pop(axes.index(projection_axis))
         if len(axes)==3:
            screen.warning("Invalid projection axis specified.\n\n USAGE: [animate_projection(a,unwrap=<True|False>, projection_axis=<0|1|2>) .\n Defaulting to 2 (ie: z).")
         if unwrap==1:
            atoms = self.unwrap(a)
         else:
            atoms = a
         xlim,ylim = axis_pad([np.min(atoms[:,:,0]),np.max(atoms[:,:,0]),np.min(atoms[:,:,1]),np.max(atoms[:,:,1])])
         fig = plt.figure()
         ax = fig.add_subplot(111)
         plt.ion()
         screen.task("Plotting frames")
         for t in range(0,len(atoms),10):
            ax.cla()
            ax.set_ylim(ylim)
            ax.set_xlim(xlim)
            plt.scatter(atoms[t][:,axes[0]],atoms[t][:,axes[1]])
            plt.draw()

      def simpleplot(self,x,y):
         fig = plt.figure()
         ax = fig.add_subplot(111)
         plt.plot(x,y)
         screen.task("PNG written to simpleplot.png")
         plt.savefig('simpleplot.png')





