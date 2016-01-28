__author__ = 'korovkin_m'
from PyQt4 import QtGui, QtCore

class QMainWindowWrapper(QtGui.QWidget):
    def __init__(self, parent=None):
        super(QMainWindowWrapper, self).__init__(parent)
        self.setWindowTitle("widget")
        self.mainwindow = QtGui.QMainWindow()
        self.mainwindow.setWindowTitle("mainw")

        self.toolbar = QtGui.QToolBar()
        self.toolbar_button = QtGui.QToolButton()
        self.toolbar.addWidget(self.toolbar_button)
        self.mainwindow.addToolBar(self.toolbar)

        self.layout_QWidget = QtGui.QVBoxLayout(self)
        self.layout_QWidget.addWidget(self.mainwindow)