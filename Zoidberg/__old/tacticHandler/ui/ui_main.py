#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ui_main.py
# Main Window interface

from PyQt4 import QtCore, QtGui

import sys

sys.path.append('\\\\SERVER-3D\\Project\\lib\\setup\\maya\\maya_scripts_rfm4\\LGT\\tacticHandler')

from globalProcs import *
import ui_open

server3d = '//server-3d/'
print(server3d)


class dockWindow(QtGui.QDockWidget):
    def __init__(self, parent=getMayaWindow()):
        super(dockWindow, self).__init__(parent)
        self.findingCBLE = self.parent().findChildren((QtGui.QDockWidget), 'dockControl1')

        self.createTitle()


        self.readSettings()

        self.formLayout()

        self.createMenu()

        self.createTabs()


    def createTitle(self):
        """
        Making Title and Version
        """
        self.setWindowTitle('TACTIC Handler ' + version())
        self.setObjectName('TACTIC Handler')

    def formLayout(self):
        """
        Main Form Layout Calls
        """
        self.mainWidget = QtGui.QWidget()
        self.mainlayout = QtGui.QVBoxLayout()
        self.mainWidget.setLayout(self.mainlayout)
        self.mainlayout.setSpacing(0)
        self.mainlayout.setContentsMargins(2, 0, 2, 3)
        self.setMinimumSize(427, 276)

    def createMenu(self):
        """
        Creating Menu Bar
        """
        self.bar = QtGui.QMenuBar(self)
        # self.mainlayout.addWidget(self.bar)
        self.config = QtGui.QMenu('Config')
        self.config.setTearOffEnabled(True)
        self.bar.addMenu(self.config)

    def createTabs(self):
        """
        Creating Tabs
        """
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.setStyleSheet('QTabWidget{background: rgb(68,68,68);}')
        self.hidderCheckbox = QtGui.QCheckBox('case')
        self.hidderCheckbox.setStyleSheet(
            "QCheckBox::indicator:unchecked{ image: url(%sProject/lib/setup/maya/maya_scripts_rfm4/SSM/resources/stylesheet-branch-closed-scaled.png); width: 11px; height: 11px;} QCheckBox::indicator:checked{ image: url(%sProject/lib/setup/maya/maya_scripts_rfm4/SSM/resources/stylesheet-branch-open-scaled.png); width: 11px; height: 11px;} QCheckBox{font-weight: bold;}" % (
                server3d, server3d))
        self.mainlayout.addWidget(self.hidderCheckbox)
        self.mainlayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.mainlayout.addWidget(self.buttonBox)
        # self.openUI = ui_open.Window()
        self.tabWidget.addTab(self.openUI, 'Open')
        self.setWidget(self.mainWidget)

    def readSettings(self):
        """
        Reading Settings
        """
        settings = QtCore.QSettings('Exam', 'TACTIC Handling Tool')
        settings.beginGroup('MainWindow')

        if settings.value('isFloating', False).toBool():
            self.setFloating(True)
        else:
            self.setFloating(False)

        posArea = settings.value('dockWidgetArea', "2").toInt()
        self.parent().addDockWidget(posArea[0], self)

        posTabifi = settings.value('tabifiedDockWidgets', "1").toInt()
        if posTabifi: self.parent().tabifyDockWidget(self.findingCBLE[0], self)

        pos = settings.value('posMayaApp', QtCore.QPoint(200, 200)).toPoint()
        self.move(pos)
        size = settings.value('sizeMayaApp', QtCore.QSize(400, 400)).toSize()
        self.resize(size)
        settings.endGroup()

    def writeSettings(self):
        """
        Writing Settings
        """
        settings = QtCore.QSettings('Exam', 'TACTIC Handling Tool')
        settings.beginGroup('MainWindow')
        settings.setValue('tabWidget', self.tabWidget.currentIndex())
        settings.setValue('dockWidgetArea', self.parent().dockWidgetArea(self))
        settings.setValue('isFloating', self.isFloating())
        settings.setValue('tabifiedDockWidgets', len(self.parent().tabifiedDockWidgets(self)))
        settings.setValue('posMayaApp', self.pos())
        settings.setValue('sizeMayaApp', self.size())
        settings.endGroup()
        for i in range(0, self.tabWidget.count()):
            if hasattr(self.tabWidget.widget(i), 'writeSettings'):
                self.tabWidget.widget(i).writeSettings()
        self.deleteLater()

    def closeEvent(self, event):
        # event.ignore()
        event.accept()
        self.writeSettings()


# implementation


def startup():
    mainWindowInstances = getMayaWindow().findChildren(QtGui.QDockWidget, 'TACTIC Handler')
    for mainWindowInstance in mainWindowInstances:
        mainWindowInstance.close()
        print('TACTIC Handler is already running! Restarting...')
    # print(mainWindowInstances)
    # mainWindowInstances[0].close()
    mainWindow = dockWindow()
    mainWindow.show()