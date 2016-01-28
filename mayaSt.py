#init maya
import maya.standalone as mst
mst.initialize( name='python' )
import maya.cmds as cmds
import glob

def func():
    print cmds.ls(shapes=True)

filea ='C:/Users/MikhailKorovkin/Documents/maya/projects/default/scenes/ref_ref.mb'
cmds.file(filea, o=True)
func()