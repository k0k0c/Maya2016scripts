__author__ = 'korovkin_m'
from PyQt4 import QtGui
import ui.pyuic.setItemForm as ui
import func.setsOperator as setop

class Ui_setItemFormSetup(QtGui.QWidget):
    def __init__(self, parent):
        super(Ui_setItemFormSetup, self).__init__(parent)
        self.ui = ui.Ui_setItemForm()
        self.ui.setupUi(self)