# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '//SERVER-3D/Project/lib/setup/maya/maya_scripts_rfm4/LGT/ui/find_match_widget_ui.ui'
#
# Created: Tue Nov 10 12:52:01 2015
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_find_match_widget(object):
    def setupUi(self, find_match_widget):
        find_match_widget.setObjectName(_fromUtf8("find_match_widget"))
        find_match_widget.resize(311, 533)
        self.verticalLayout = QtGui.QVBoxLayout(find_match_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.find_match_tableWidget = QtGui.QTableWidget(find_match_widget)
        self.find_match_tableWidget.setObjectName(_fromUtf8("find_match_tableWidget"))
        self.find_match_tableWidget.setColumnCount(2)
        self.find_match_tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.find_match_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.find_match_tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.find_match_tableWidget)

        self.retranslateUi(find_match_widget)
        QtCore.QMetaObject.connectSlotsByName(find_match_widget)

    def retranslateUi(self, find_match_widget):
        find_match_widget.setWindowTitle(QtGui.QApplication.translate("find_match_widget", "Find match", None, QtGui.QApplication.UnicodeUTF8))
        item = self.find_match_tableWidget.horizontalHeaderItem(0)
        item.setText(QtGui.QApplication.translate("find_match_widget", "parent", None, QtGui.QApplication.UnicodeUTF8))
        item = self.find_match_tableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("find_match_widget", "target", None, QtGui.QApplication.UnicodeUTF8))

