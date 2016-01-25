# coding=utf-8
import Zoidberg.config
from PySide import QtGui
import inspect
import collections
from PySide.QtGui import *
from PySide.QtCore import *
import maya.mel as mel
import func.ltk_func as func
import func.maya_func as maya
import func.ui_to_py as ui_to_py
import func.setsOperator as sets
import func.ui_referenceEditor as refEdit

reload(func)
reload(maya)
reload(ui_to_py)
reload(sets)
reload(refEdit)

import ui.pyuic as ui

reload(ui)



def printClick():
    print "Cklicked!"
# a = QTabBar.connect(SIGNAL("tabBarClicked(int)", lambda: printClick()))

class Zoidberg_form(QDockWidget, QWidget):
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

    def __init__(self, parent=func.getMayaWindow()):
        super(Zoidberg_form, self).__init__(parent)
        self.maya_dock = self.parent().findChildren((QtGui.QDockWidget), 'dockControl1')
        self.setObjectName("Zoidberg")
        self.setWindowTitle("------=Zoidberg=-----")
        self.mainWindow = parent
        self.mainWindow.tabifyDockWidget(self.maya_dock[-1], self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.refEdit = refEdit.referenceEditor(self)
        self.refEdit.load()

        self.dockWidgetContents = QtGui.QWidget()
        self.setWidget(self.dockWidgetContents)
        self.mainQL = QVBoxLayout(self.dockWidgetContents)
        self.mainQL.setContentsMargins(0, 0, 0, 0)
        self.mainQMW = QMainWindow()
        self.mainQL.addWidget(self.mainQMW)
        # self.mainQMW.

        self.tabList = ("Lighting", "Rendering", "Modeling")
        self.dockList = ("reference", "paste", "eggs", "delete", "move")
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
            tabTopQDW = QDockWidget()
            tabTopQDW.setWindowTitle(tab)
            tabTopQDW.setObjectName(tab + "_tab")
            existFirstTopTab = self.mainQMW.findChildren(QDockWidget, tablist[0] + "_tab")
            self.mainQMW.addDockWidget(Qt.RightDockWidgetArea, tabTopQDW)
            if existFirstTopTab:
                self.mainQMW.tabifyDockWidget(existFirstTopTab[0], tabTopQDW)
            tabTopQDW.setWidget(tabQMW)
            self.mainQMW.setTabPosition(Qt.RightDockWidgetArea, QTabWidget.North)

    def addDock(self, tablist, dockList):
        for tab in self.existTabs:
            if tab.objectName() == tablist + "_mv":
                for dockName in dockList:
                    dock = QDockWidget(tab)
                    dock.setFeatures(
                        QtGui.QDockWidget.DockWidgetFloatable |
                        QtGui.QDockWidget.DockWidgetMovable |
                        QtGui.QDockWidget.DockWidgetClosable)
                    dock.setObjectName(dockName + "_QDockWidget")
                    dock.setWindowTitle(dockName)
                    self.existDock.setdefault(tab, []).append(dock)
                    tab.addDockWidget(Qt.RightDockWidgetArea, dock)
                    if dockName == "reference":
                        dock.setWidget(self.refEdit)

    def closeEvent(self, QCloseEvent):
        self.deleteLater()
        QCloseEvent.accept()

    @staticmethod
    def startup():
        Zoidberg = func.getMayaWindow().findChildren(QtGui.QDockWidget, "Zoidberg")
        if len(Zoidberg) > 1:
            for i in range(len(Zoidberg) - 1):
                Zoidberg[i - 1].close()
        Zoidberg = Zoidberg[0]
        if func.getMayaWindow().tabifiedDockWidgets(Zoidberg):
            func.getMayaWindow().tabifyDockWidget(func.getMayaWindow().tabifiedDockWidgets(Zoidberg)[0], Zoidberg)
        Zoidberg.show()


def startup():
    ui_to_py.init()
    Zoidberg = Zoidberg_form()
    Zoidberg.startup()
