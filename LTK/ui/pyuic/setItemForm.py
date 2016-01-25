# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:/Users/MikhailKorovkin/Documents/maya/2016/scripts/LTK/ui/qtd/setItemForm.ui'
#
# Created: Sun Jan 24 21:55:02 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_setItemForm(object):
    def setupUi(self, setItemForm):
        setItemForm.setObjectName("setItemForm")
        setItemForm.resize(400, 44)
        self.verticalLayout = QtGui.QVBoxLayout(setItemForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setItemhorizontalLayout = QtGui.QHBoxLayout()
        self.setItemhorizontalLayout.setSpacing(2)
        self.setItemhorizontalLayout.setObjectName("setItemhorizontalLayout")
        self.setItemcomboBox = QtGui.QComboBox(setItemForm)
        self.setItemcomboBox.setEditable(True)
        self.setItemcomboBox.setObjectName("setItemcomboBox")
        self.setItemhorizontalLayout.addWidget(self.setItemcomboBox)
        self.setItemAddpushButton = QtGui.QPushButton(setItemForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setItemAddpushButton.sizePolicy().hasHeightForWidth())
        self.setItemAddpushButton.setSizePolicy(sizePolicy)
        self.setItemAddpushButton.setMaximumSize(QtCore.QSize(25, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.setItemAddpushButton.setFont(font)
        self.setItemAddpushButton.setStyleSheet("")
        self.setItemAddpushButton.setObjectName("setItemAddpushButton")
        self.setItemhorizontalLayout.addWidget(self.setItemAddpushButton)
        self.setItemExludepushButton = QtGui.QPushButton(setItemForm)
        self.setItemExludepushButton.setMaximumSize(QtCore.QSize(25, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.setItemExludepushButton.setFont(font)
        self.setItemExludepushButton.setStyleSheet("")
        self.setItemExludepushButton.setObjectName("setItemExludepushButton")
        self.setItemhorizontalLayout.addWidget(self.setItemExludepushButton)
        self.setItemVispushButton = QtGui.QPushButton(setItemForm)
        self.setItemVispushButton.setMaximumSize(QtCore.QSize(25, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.setItemVispushButton.setFont(font)
        self.setItemVispushButton.setStyleSheet("")
        self.setItemVispushButton.setObjectName("setItemVispushButton")
        self.setItemhorizontalLayout.addWidget(self.setItemVispushButton)
        self.setItemSelectpushButton = QtGui.QPushButton(setItemForm)
        self.setItemSelectpushButton.setMaximumSize(QtCore.QSize(25, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.setItemSelectpushButton.setFont(font)
        self.setItemSelectpushButton.setStyleSheet("")
        self.setItemSelectpushButton.setObjectName("setItemSelectpushButton")
        self.setItemhorizontalLayout.addWidget(self.setItemSelectpushButton)
        self.verticalLayout.addLayout(self.setItemhorizontalLayout)

        self.retranslateUi(setItemForm)
        QtCore.QMetaObject.connectSlotsByName(setItemForm)

    def retranslateUi(self, setItemForm):
        setItemForm.setWindowTitle(QtGui.QApplication.translate("setItemForm", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.setItemAddpushButton.setToolTip(QtGui.QApplication.translate("setItemForm", "<html><head/><body><p><span style=\" font-weight:600;\">(click)</span> - add selected object to &quot;farRenderPlane_set&quot;</p><p><span style=\" font-weight:600;\">(shift + click)</span> - select object in &quot;farRenderPlane_set&quot;</p><p><span style=\" font-weight:600;\">(ctrl+click)</span> - hide object in &quot;farRenderPlane_set&quot;</p><p><span style=\" font-weight:600;\">(alt+click)</span> - remove object from &quot;farRenderPlane_set&quot;</p><p><br/></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.setItemAddpushButton.setText(QtGui.QApplication.translate("setItemForm", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.setItemAddpushButton.setProperty("-c", QtGui.QApplication.translate("setItemForm", "\"renderPlaneSetup farRenderPlane_set\"", None, QtGui.QApplication.UnicodeUTF8))
        self.setItemExludepushButton.setText(QtGui.QApplication.translate("setItemForm", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.setItemVispushButton.setText(QtGui.QApplication.translate("setItemForm", "H", None, QtGui.QApplication.UnicodeUTF8))
        self.setItemSelectpushButton.setText(QtGui.QApplication.translate("setItemForm", "S", None, QtGui.QApplication.UnicodeUTF8))

