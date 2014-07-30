#!/usr/bin/python
from os import system


for i in range(25,300,20):
   distance = i/1000.0

   system("cp -r system_XXXX/ system_{0}/".format(distance))
   system("sed -i 's|!!!zcoord!!!|{0}|g'  system_{1}/*".format(distance,distance))
   system("sed -i 's|!!!tag!!!|{0}|g'  system_{1}/*".format(distance,distance))









