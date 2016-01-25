import sys
from PyQt4 import QtGui
import ui.pyuic as ui


class QCustomQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.ui = ui.setItemForm.Ui_setItemForm()
        self.ui.setupUi(self)


class exampleQMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(exampleQMainWindow, self).__init__()
        # Create QListWidget
        self.myQListWidget = QtGui.QListWidget(self)
        for index, name, icon in [
            ('No.1', 'Meyoko', 'icon.png'),
            ('No.2', 'Nyaruko', 'icon.png'),
            ('No.3', 'Louise', 'icon.png')]:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.ui.setItemcomboBox.addItem(index)
            myQCustomQWidget.ui.setItemcomboBox.addItem(name)
            myQCustomQWidget.ui.setItemcomboBox.addItem(icon)
            # Create QListWidgetItem
            myQListWidgetItem = QtGui.QListWidgetItem(self.myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.setCentralWidget(self.myQListWidget)


app = QtGui.QApplication([])
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())