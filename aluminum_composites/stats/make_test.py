


f = open('XDATCAR_test_msd','w')



f.write("""moving_aluminums_for_test_msd
            1
     30.352000    0.000000    0.000000
      0.000000   30.027273    0.000000
      0.000000    0.000000   30.639317
   Al
   3
""")


for i in xrange(100):
   dx = i/100.0

   f.write("""Direct configuration=     1
{0}  0.55555773  0.50000057
{1}  0.55555182  0.25000001
{2}  0.55559269  0.75095959
""".format(dx,dx,dx))




f.close()







