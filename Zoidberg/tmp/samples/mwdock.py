import sys
from PyQt4 import QtGui
import PyQt4.Qt as Qt
from PyQt4.QtCore import *


class QSubMain(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QSubMain, self).__init__(parent)
        self.setWindowTitle("subMainwindow")
        self.toolbar = QtGui.QToolBar(self)
        self.addToolBar(self.toolbar)
        for i in range(3):
            self.tbutton = QtGui.QToolButton()
            self.toolbar.addWidget(self.tbutton)
        self.cw = QtGui.QListWidget(self)
        self.cw.hide()
        self.setCentralWidget(self.cw)

        self.subdock1 = QtGui.QDockWidget(self)
        self.subdock2 = QtGui.QDockWidget(self)
        self.subdock1.setAllowedAreas(Qt.RightDockWidgetArea)
        self.subdock2.setAllowedAreas(Qt.RightDockWidgetArea)
        self.subdock1.setWindowTitle("subdock1")
        self.subdock2.setWindowTitle("subdock2")

        self.sub1wrap = QtGui.QWidget()
        self.sub2wrap = QtGui.QWidget()

        self.sub1layout = QtGui.QVBoxLayout(self.sub1wrap)
        self.sub2layout = QtGui.QVBoxLayout(self.sub2wrap)


        self.sub1toolbar = QtGui.QToolBar()
        self.sub2toolbar = QtGui.QToolBar()


        self.textw1 = QtGui.QTextEdit("Hello AAAA!")
        self.textw2 = QtGui.QTextEdit("YYYYYYY!")

        self.sub1layout.addWidget(self.sub1toolbar)
        self.sub1layout.addWidget(self.textw1)
        self.sub2layout.addWidget(self.sub2toolbar)
        self.sub2layout.addWidget(self.textw2)


        self.addDockWidget(Qt.RightDockWidgetArea, self.subdock1)
        self.addDockWidget(Qt.RightDockWidgetArea, self.subdock2)

        self.subdock1.setWidget(self.sub1wrap)
        self.subdock2.setWidget(self.sub2wrap)

class exampleQMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(exampleQMainWindow, self).__init__()
        self.setWindowTitle("Autodesk Maya 666")
        self.submain = QSubMain(self)
        self.myQListWidget = QtGui.QListWidget(self)
        self.setCentralWidget(self.myQListWidget)
        self.dock = QtGui.QDockWidget(self)
        self.dock.setWindowTitle("maindock")
        self.dock.setWidget(self.submain)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)

app = QtGui.QApplication([])
# window = QSubMain()
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())