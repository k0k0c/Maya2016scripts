#! /usr/bin/env python
# -*- coding: utf-8 -*-

# ui_open.py
# Opening Window interface

from PyQt4 import QtCore, QtGui
from globalProcs import *


class openTab(QtGui.QWidget):
    def __init__(self, parent=getMayaWindow()):
        super(Window, self).__init__(parent)
        self.mainLayout = QtGui.QVBoxLayout()
        self.setProperty("index", "Open")
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

    def load(self):
        self.tabWidget = QtGui.QTabWidget()
        self.mainLayout.addWidget(self.tabWidget)

        self.readSettings()
        self.tabWidget.tabBar().currentChanged.connect(self.currentWidgetSlot)

    def currentWidgetSlot(self, wi):
        if wi not in self.loaded:
            self.tabWidget.widget(wi).load()
            self.loaded.append(wi)
