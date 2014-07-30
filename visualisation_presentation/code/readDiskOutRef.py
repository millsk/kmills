from paraview.simple import *
path = '/Users/razoumov/Dropbox/visualization/data/other/'
reader = ExodusIIReader(FileName=path+'disk_out_ref.ex2')
Show()
Render()
