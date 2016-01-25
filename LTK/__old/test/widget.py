from PyQt4 import QtGui, QtCore


class QLineEditWErrState(QtGui.QLineEdit):

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.timeout = 800
        self.errorCss = 'background-color: antiquewhite'
        self._orig_css = self.styleSheet()

    def setErrorState(self):
        self.emit(QtCore.SIGNAL("errorStateSet()"))
        self.setStyleSheet(self.error_css)
        QtCore.QTimer.singleShot(self.timeout, self.resetErrorState)

    def resetErrorState(self):
        self.setStyleSheet(self._orig_css)
        self.emit(QtCore.SIGNAL("errorStateReseted()"))