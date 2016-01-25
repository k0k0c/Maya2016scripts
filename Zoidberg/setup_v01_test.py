# coding=utf-8
# import config
from PyQt4 import QtGui
import inspect
import collections
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import maya.mel as mel
# import func.ltk_func as func
# import func.maya_func as maya
# import func.ui_to_py as ui_to_py
# import func.setsOperator as sets

# reload(func)
# reload(maya)
# reload(ui_to_py)
# reload(sets)

import ui.pyuic as ui

reload(ui)

def printClick():
    print "Cklicked!"
# a = QTabBar.connect(SIGNAL("tabBarClicked(int)", lambda: printClick()))

class MQDockWidget(QDockWidget):
    def mousePressEvent(self, *args, **kwargs): # real signature unknown
        print "Mouse press event"

    def hideEvent(self, *args, **kwargs): # real signature unknown
        print "Hide event"

    def showEvent(self, *args, **kwargs): # real signature unknown
        print "Show event"

class Ui_ltk_setup(MQDockWidget, QWidget):
    """
    Структура:

    |_Maya
        |_QDockWidget (self)
            |_QWidget
                |_QVBoxLayout
                    |_QDockWidget_01 (tabify)
                    |   |_QMainWindow
                    |      |_QList (centralWidget)
                    |       |_QDockWidget_01
                    |       |_...
                    |       |_QDockWidget_xx
                    |_...
                    |_QDockWidget_xx (tabify)
                        |_QMainWindow
                           |_QList (centralWidget)
                            |_QDockWidget_01
                            |_...
                            |_QDockWidget_xx


    """

    def __init__(self):
        super(Ui_ltk_setup, self).__init__()
        self.setObjectName("Zoidberg")
        self.setWindowTitle("------=Zoidberg=-----")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.dockWidgetContents = QtGui.QWidget()
        self.setWidget(self.dockWidgetContents)
        self.mainQL = QVBoxLayout(self.dockWidgetContents)
        self.mainQL.setMargin(0)
        self.mainQMW = QMainWindow()
        self.mainQL.addWidget(self.mainQMW)
        # self.mainQMW.

        self.tabList = ("Lighting", "Rendering", "Modeling")
        self.dockList = ("copy", "paste", "eggs", "delete", "move")
        self.existTabs = []
        self.existDock = {}
        self.createTab(self.tabList)
        self.addDock(self.tabList[0], self.dockList)
        self.tabbar = self.mainQMW.findChildren(QTabBar)
        self.tabbar[0].setExpanding(True)
        # self.tabbar[0].setChangeCurrentOnDrag(True)
        self.tabbar[0].setMovable(True)
        self.tabbar[0].connect(self, SIGNAL("tabBarClicked(int)"), lambda: printClick())
        # print self.tabbar[0].receivers(SIGNAL("tabBarClicked(-1)"))
        # print self.tabbar[0].senderSignalIndex()

    def createTab(self, tablist):
        for tab in tablist:
            tabQMW= QMainWindow()
            tabQMW.setObjectName(tab + "_mv")
            tabQMW.setDockOptions(QMainWindow.AnimatedDocks)
            if tabQMW not in self.existTabs:
                self.existTabs.append(tabQMW)
            tabCW = QListWidget(tabQMW)
            tabCW.hide()
            tabQMW.setCentralWidget(tabCW)
            tabTopQDW = MQDockWidget()
            tabTopQDW.setWindowTitle(tab)
            tabTopQDW.setObjectName(tab + "_tab")
            existFirstTopTab = self.mainQMW.findChildren(MQDockWidget, tablist[0] + "_tab")
            self.mainQMW.addDockWidget(Qt.RightDockWidgetArea, tabTopQDW)
            if existFirstTopTab:
                self.mainQMW.tabifyDockWidget(existFirstTopTab[0], tabTopQDW)
            tabTopQDW.setWidget(tabQMW)
            self.mainQMW.setTabPosition(Qt.RightDockWidgetArea, QTabWidget.North)

    def addDock(self, tablist, dockList):
        for tab in self.existTabs:
            if tab.objectName() == tablist + "_mv":
                for dockName in dockList:
                    dock = MQDockWidget(tab)
                    dock.setFeatures(
                        QtGui.QDockWidget.DockWidgetFloatable |
                        QtGui.QDockWidget.DockWidgetMovable |
                        QtGui.QDockWidget.DockWidgetClosable)
                    dock.setObjectName(dockName + "_QDockWidget")
                    dock.setWindowTitle(dockName)
                    self.existDock.setdefault(tab, []).append(dock)
                    tab.addDockWidget(Qt.RightDockWidgetArea, dock)

    def closeEvent(self, QCloseEvent):
        self.deleteLater()
        QCloseEvent.accept()

    @staticmethod
    def startup():
        LTK = func.getMayaWindow().findChildren(QtGui.QDockWidget, "Zoidberg")
        if len(LTK) > 1:
            for i in range(len(LTK) - 1):
                LTK[i - 1].close()
        LTK = LTK[0]
        if func.getMayaWindow().tabifiedDockWidgets(LTK):
            func.getMayaWindow().tabifyDockWidget(func.getMayaWindow().tabifiedDockWidgets(LTK)[0], LTK)
        LTK.show()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([])
    window = Ui_ltk_setup()
    window.show()
    sys.exit(app.exec_())

