import config

from PyQt4 import QtGui
import inspect

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys


class MyWin(QtGui.QMainWindow, QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.setObjectName("tt_Form")
        self.resize(400, 300)
        self.setWindowTitle("Form")
        self.setDockOptions(QtGui.QMainWindow.AnimatedDocks)
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.hide()
        self.setCentralWidget(self.centralwidget)
        self.tt_dockWidget = QtGui.QDockWidget(self)
        self.addDockWidget(Qt.DockWidgetArea(1), self.tt_dockWidget)
        self.tt_dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.tt_dockWidgetContents = QtGui.QWidget()
        self.tt_verticalLayout_2 = QtGui.QVBoxLayout(self.tt_dockWidgetContents)
        self.tt_pushButton = QtGui.QPushButton(self.tt_dockWidgetContents)
        self.tt_pushButton.setText("PushButton")
        self.tt_verticalLayout_2.addWidget(self.tt_pushButton)
        self.tt_dockWidget.setWidget(self.tt_dockWidgetContents)

app = QtGui.QApplication(sys.argv)
qb = MyWin()
qb.show()
sys.exit(app.exec_())