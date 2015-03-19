head = """undoped_BNAl
     1
     10.00000     0.000000    0.0000000
      0.000000   10.000000    0.0000000
      0.000000    0.000000    10.000000
 Al
 1000

"""

n = 20

f = open("XDATCAR_test",'w')

f.write(head)

for t in range(10):
   for i in range(10):
      for j in range(10):
         for k in range(10):
            f.write(" {0}    {1}    {2}\n".format(i/10.,j/10.,k/10.))
   f.write(" \n")




f.close()



