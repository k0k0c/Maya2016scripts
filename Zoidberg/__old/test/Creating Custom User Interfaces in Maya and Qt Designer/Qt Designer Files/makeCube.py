#QT Interface makeCube script for Maya
#Written by Tim Callaway
from PyQt4 import QtGui, QtCore, uic
from pymel.core import *
import pymel.core as pm
import maya.mel as mel

# Path to the designer UI file
ui_filename = 'c:/dtQt/makeCube.ui'
form_class, base_class = uic.loadUiType(ui_filename)

# Interface Class
class makeCube(base_class, form_class):
        def __init__(self):
                super(base_class, self).__init__()
                self.setupUi(self)
                self.setObjectName('makeCube')
                self.setDockNestingEnabled(True)
                self.connectInterface()

        def connectInterface(self):
                QtCore.QObject.connect(self.cubeButton, QtCore.SIGNAL("clicked()"),self.makeCubeWin)

        def makeCubeWin(self):
                mel.eval('global proc makeCube(){CreatePolygonCube;}')
                mel.eval('makeCube')

                
def main():
        global ui
        ui=makeCube()
        ui.show()

if __name__ == "__main__":
        main()
