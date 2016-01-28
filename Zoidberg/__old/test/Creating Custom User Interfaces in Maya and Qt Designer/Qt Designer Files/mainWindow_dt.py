#QT Interface Main script for Maya
#Written by Tim Callaway
from PyQt4 import QtGui, QtCore, uic
from pymel.core import *
import pymel.core as pm
import maya.mel as mel

# Path to the designer UI file
ui_filename = 'c:/dtQt/mainWindow_dt.ui'
form_class, base_class = uic.loadUiType(ui_filename)

# Interface Class
class mainWindow_dt(base_class, form_class):
        def __init__(self):
                super(base_class, self).__init__()
                self.setupUi(self)
                self.setObjectName('mainWindow_dt')
                self.setDockNestingEnabled(True)
                self.connectInterface()

        def connectInterface(self):
                QtCore.QObject.connect(self.jointPath, QtCore.SIGNAL("clicked()"),self.jointPath_dt)
                QtCore.QObject.connect(self.sphere, QtCore.SIGNAL("clicked()"),self.makeSphere)

        def jointPath_dt(self):
                import sys
                Dir = 'c:/dtT'
                if Dir not in sys.path:   
                    sys.path.append(Dir)
                try: reload(jointPath_dt)
                except: import jointPath_dt
                jointPath_dt.main()



        def makeSphere(self):
                mel.eval('global proc makeSphere(){CreatePolygonSphere;}')
                mel.eval('makeSphere()')
                
def main():
        global ui
        ui=mainWindow_dt()
        ui.label.setPixmap( QtGui.QPixmap('C:/dtQT/logo.png') )
        ui.show()
        
        if dockControl('ui_dock', q=1, ex=1):
                deleteUI('ui_dock')
        floatingLayout = paneLayout(configuration='single', width=400)
        allowedAreas = ('right')
        docControl = dockControl('ui_dock', area = allowedAreas, content=floatingLayout, label='mainWindow_dt')
        control('mainWindow_dt', e=True, p=floatingLayout)
        
if __name__ == "__main__":
        main()


