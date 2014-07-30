#!/usr/bin/python
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
from matplotlib import gridspec
import numpy as np
import random
from math import sin,floor,ceil
import random


label_bands = False
label_energies = False
break_scale = False



label_bands = True
label_energies = True
names = ["BH3","BH3CO","CO"]  #["iota1","kappa","iota2"]
EL_i1 =  [ -0.91242861, -0.57497642, -0.57360914, -0.25917972,-0.26909601E-01, 0.11054361, 0.12006583, 0.13843865, 0.14035367, 0.16337160, 0.18230320, 0.20231441, 0.22762577, 0.24628221, 0.29266316, 0.30435686, 0.30977583, 0.31585082, 0.31689089, 0.33191280  ]

EL_i2 =  [  -1.8800086, -1.0235572,-0.70123567, -0.70117671, -0.66271558, -0.26939202, -0.26912525, -0.15145932E-01, 0.11272668, 0.14742937, 0.14917424, 0.15062107, 0.15643238, 0.18752024, 0.26467760, 0.28350233, 0.30181310, 0.30639639, 0.32556276, 0.32619498  ]

EL_k = [ -1.9137163, -1.1597127, -0.90880734, -0.74865645, -0.74249999, -0.70705667, -0.55242227, -0.49828972, -0.41934670, -0.28503199, -0.62391860E-02, 0.11898545, 0.13748200, 0.14398215, 0.15731183, 0.15890522, 0.19177280, 0.21329397, 0.23754250, 0.27110115 ]

EL_k  = [ i * 13.605 for i in EL_k ]
EL_i2 = [ i * 13.605 for i in EL_i2 ]
EL_i1 = [ i * 13.605 for i in EL_i1 ]




def percent_updown(num, percent=1., relative_to=0):
   if relative_to==0: relative_to=num
   return num + percent*abs(relative_to)

def dup_remove(seq):
   seen = set()
   seen_add = seen.add
   return [ x for x in seq if x not in seen and not seen_add(x)]


b = [ [7,9],[15,17],[21,23] ]  #x coordinates of columns of level bars

#EL_i1 = dup_remove(EL_i1)
#EL_i2 = dup_remove(EL_i2)
#EL_k = dup_remove(EL_k)

iota1 = [[(b[0][0],i),(b[0][1],i)] for i in EL_i1 ]
iota2 = [[(b[2][0],i),(b[2][1],i)] for i in EL_i2 ]
kappa = [[(b[1][0],i),(b[1][1],i)] for i in EL_k  ]

#The gray lines that span the whole plot
span = [[(0,i),(b[2][1] + 2,i)] for i in EL_i1] + [[(0,i),(b[2][1] + 2,i)] for i in EL_i2] + [[(0,i),(b[2][1]+2,i)] for i in EL_k]

lst = EL_i1 + EL_i2 + EL_k
arr = np.array(lst)
first_differences = np.zeros(arr.shape)
first_differences[1:] = arr[1:] - arr[:-1]
first_differences = list(first_differences)
largest_difference = first_differences.index(min(first_differences))
break_at  = 0.50 * ( lst[largest_difference] + lst[largest_difference + 1])
break_at = min([ i if i>break_at else 10000 for i in lst])
num_above_break = sum(i>=break_at for i in lst)
num_below_break = sum(i<break_at for i in lst)
above_below_ratio = float(num_below_break) / float(num_above_break)


fig = plt.figure(figsize = (8.5,11))
if break_scale:
   gs = gridspec.GridSpec(2,1, height_ratios=[1,above_below_ratio])
   ax1 = fig.add_subplot(gs[0])
   ax2 = fig.add_subplot(gs[1])
   temp = [ax1,ax2]
else: 
   ax1 = fig.add_subplot(1,1,1)
   temp = [ax1]


for ax in temp:
   lc2 = mc.LineCollection(span, color='#e9e9e9', linewidths=0.5)
   iota1_lines = mc.LineCollection(iota1, color='#DD5555', linewidths=1)
   iota2_lines = mc.LineCollection(iota2, color='#5555DD', linewidths=1)
   kappa_lines = mc.LineCollection(kappa, color='#DD55DD', linewidths=1)

   ax.add_collection(lc2)
   ax.add_collection(iota1_lines)
   ax.add_collection(iota2_lines)
   ax.add_collection(kappa_lines)
   ax.margins(0.0)
   ax.axis('off')
   ax.set_xlim(0,25)


for n,name in enumerate(names):
   ax1.annotate(name, xy=(float(b[n][0] + b[n][1]) / 2.0, percent_updown(ax1.get_ylim()[1], -0.05) ), horizontalalignment='center')


if break_scale:
   #find the maximum value that is LESS THAN the breaking point:
   temp = max([ i if i<break_at else -10000 for i in lst])
   ax1.set_ylim(break_at,max(lst) + 0.1*abs(break_at))
   ax2.set_ylim(min(lst) - 0.1*abs(min(lst)),temp +0.1*abs(temp))

   break_line_y = ax2.get_ylim()[1]
   ax2.axhline(y=break_line_y, linestyle='-.', lw=2, color='k')
   ax2.annotate("below this break not to scale", xy=(22,percent_updown(break_line_y, -0.03, ax2.get_ylim()[0] - ax2.get_ylim()[1])), size=6)

rangee = abs( max(EL_i1+EL_i2+EL_k) - min(EL_i1+EL_i2+EL_k))

sorted_lst = sorted(lst)

for y,x,band in zip(
   lst,
   [b[0][0]]*len(EL_i1) + [b[2][0]]*len(EL_i2) +[b[1][0]]*len(EL_k),
   [i+1 for i in range(len(EL_i1))] + [i+1 for i in range(len(EL_i2))] + [i+1 for i in range(len(EL_k))]):
   sign = -1 if sorted_lst.index(y)%2 ==0 else 1
   if label_bands:
      ax1.annotate(band,xy=(2*sign*(-1) + x+1,y))
      if break_scale:   ax2.annotate(band,xy=(2*sign*(-1) + x+1,y))
   if label_energies:
      ax1.annotate(round(y,2),xy=(12.6 + sign*11.5, y))
      if break_scale:   ax2.annotate(y,xy=(12.6 + 11.5*sign, y))


plt.savefig("{0}_molecular_orbitals.pdf".format(names[1]))

