#**********************************************
# User Interface creation for Maya
# Written by Us!
from PyQt4 import QtGui, QtCore, uic
import maya.cmds as cmds
import pymel.core as pm
from pymel import *



# Path to the designer UI file*******************************
ui_filename = 'c:/dtQT/makeCube.ui'
form_class, base_class = uic.loadUiType(ui_filename)


#Interface Class**********************************************
class makeCube(base_class, form_class):
        def __init__(self):
                super(base_class, self).__init__()
                self.setupUi(self)
                self.setObjectName('makeCube')
                self.setDockNestingEnabled(True)
                self.connectInterface()


        def connectInterface(self):
            QtCore.QObject.connect(self.makeCube, QtCore.SIGNAL("clicked()"),self.makeCubeWin)

        def makeCubeWin(self):
                print "1212"
#main*********************************************************
def main():
        global ui
        ui=makeCube() 
        ui.show()

        

main()

