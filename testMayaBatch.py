import maya.cmds as cmd
import glob


def func():
    print cmd.ls()

# we want this to execute on import
func()

# mayabatch -command "python(""import testMayaBatch"") " -file C:\Users\MikhailKorovkin\Documents\maya\projects\default\scenes\ref_ref.mb
