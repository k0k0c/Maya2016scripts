# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:/Users/MikhailKorovkin/Documents/maya/2016/scripts/LTK/ui/qtd/transferAttrUv_QWidget.ui'
#
# Created: Sun Jan 24 21:55:02 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_transferAttrUv_QWidget(object):
    def setupUi(self, transferAttrUv_QWidget):
        transferAttrUv_QWidget.setObjectName("transferAttrUv_QWidget")
        transferAttrUv_QWidget.resize(299, 124)
        self.horizontalLayout = QtGui.QHBoxLayout(transferAttrUv_QWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.actionsCheckBox_verticalLayout = QtGui.QVBoxLayout()
        self.actionsCheckBox_verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.actionsCheckBox_verticalLayout.setObjectName("actionsCheckBox_verticalLayout")
        self.actions_groupBox = QtGui.QGroupBox(transferAttrUv_QWidget)
        self.actions_groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.actions_groupBox.setObjectName("actions_groupBox")
        self.actions_verticalLayout = QtGui.QVBoxLayout(self.actions_groupBox)
        self.actions_verticalLayout.setSpacing(0)
        self.actions_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.actions_verticalLayout.setObjectName("actions_verticalLayout")
        self.actions_gridWidget = QtGui.QWidget(self.actions_groupBox)
        self.actions_gridWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.actions_gridWidget.setObjectName("actions_gridWidget")
        self.actions_gridLayout = QtGui.QGridLayout(self.actions_gridWidget)
        self.actions_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.actions_gridLayout.setSpacing(0)
        self.actions_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.actions_gridLayout.setObjectName("actions_gridLayout")
        self.copy_uv_checkBox = QtGui.QCheckBox(self.actions_gridWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_uv_checkBox.sizePolicy().hasHeightForWidth())
        self.copy_uv_checkBox.setSizePolicy(sizePolicy)
        self.copy_uv_checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.copy_uv_checkBox.setChecked(True)
        self.copy_uv_checkBox.setObjectName("copy_uv_checkBox")
        self.actions_gridLayout.addWidget(self.copy_uv_checkBox, 0, 0, 1, 1)
        self.delete_history_checkBox = QtGui.QCheckBox(self.actions_gridWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_history_checkBox.sizePolicy().hasHeightForWidth())
        self.delete_history_checkBox.setSizePolicy(sizePolicy)
        self.delete_history_checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.delete_history_checkBox.setChecked(True)
        self.delete_history_checkBox.setObjectName("delete_history_checkBox")
        self.actions_gridLayout.addWidget(self.delete_history_checkBox, 3, 0, 1, 1)
        self.unlock_tr_checkBox = QtGui.QCheckBox(self.actions_gridWidget)
        self.unlock_tr_checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.unlock_tr_checkBox.setChecked(True)
        self.unlock_tr_checkBox.setObjectName("unlock_tr_checkBox")
        self.actions_gridLayout.addWidget(self.unlock_tr_checkBox, 5, 1, 1, 1)
        self.delete_color_sets_checkBox = QtGui.QCheckBox(self.actions_gridWidget)
        self.delete_color_sets_checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.delete_color_sets_checkBox.setChecked(True)
        self.delete_color_sets_checkBox.setObjectName("delete_color_sets_checkBox")
        self.actions_gridLayout.addWidget(self.delete_color_sets_checkBox, 3, 1, 1, 1)
        self.create_sets_checkBox = QtGui.QCheckBox(self.actions_gridWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.create_sets_checkBox.sizePolicy().hasHeightForWidth())
        self.create_sets_checkBox.setSizePolicy(sizePolicy)
        self.create_sets_checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.create_sets_checkBox.setChecked(True)
        self.create_sets_checkBox.setObjectName("create_sets_checkBox")
        self.actions_gridLayout.addWidget(self.create_sets_checkBox, 5, 0, 1, 1)
        self.copy_attr_checkBox = QtGui.QCheckBox(self.actions_gridWidget)
        self.copy_attr_checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.copy_attr_checkBox.setChecked(True)
        self.copy_attr_checkBox.setObjectName("copy_attr_checkBox")
        self.actions_gridLayout.addWidget(self.copy_attr_checkBox, 0, 1, 1, 1)
        self.actions_verticalLayout.addWidget(self.actions_gridWidget)
        self.actionsCheckBox_verticalLayout.addWidget(self.actions_groupBox)
        self.searchingMethod_groupBox = QtGui.QGroupBox(transferAttrUv_QWidget)
        self.searchingMethod_groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.searchingMethod_groupBox.setObjectName("searchingMethod_groupBox")
        self.hboxlayout = QtGui.QHBoxLayout(self.searchingMethod_groupBox)
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.search_by_topology_checkBox = QtGui.QCheckBox(self.searchingMethod_groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_by_topology_checkBox.sizePolicy().hasHeightForWidth())
        self.search_by_topology_checkBox.setSizePolicy(sizePolicy)
        self.search_by_topology_checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.search_by_topology_checkBox.setChecked(True)
        self.search_by_topology_checkBox.setObjectName("search_by_topology_checkBox")
        self.hboxlayout.addWidget(self.search_by_topology_checkBox)
        self.search_by_shape_checkBox = QtGui.QCheckBox(self.searchingMethod_groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_by_shape_checkBox.sizePolicy().hasHeightForWidth())
        self.search_by_shape_checkBox.setSizePolicy(sizePolicy)
        self.search_by_shape_checkBox.setMinimumSize(QtCore.QSize(0, 0))
        self.search_by_shape_checkBox.setChecked(True)
        self.search_by_shape_checkBox.setObjectName("search_by_shape_checkBox")
        self.hboxlayout.addWidget(self.search_by_shape_checkBox)
        self.actionsCheckBox_verticalLayout.addWidget(self.searchingMethod_groupBox)
        self.horizontalLayout.addLayout(self.actionsCheckBox_verticalLayout)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.render_char_build_button = QtGui.QPushButton(transferAttrUv_QWidget)
        self.render_char_build_button.setObjectName("render_char_build_button")
        self.verticalLayout.addWidget(self.render_char_build_button)
        self.print_match_pushButton = QtGui.QPushButton(transferAttrUv_QWidget)
        self.print_match_pushButton.setObjectName("print_match_pushButton")
        self.verticalLayout.addWidget(self.print_match_pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(transferAttrUv_QWidget)
        QtCore.QMetaObject.connectSlotsByName(transferAttrUv_QWidget)

    def retranslateUi(self, transferAttrUv_QWidget):
        transferAttrUv_QWidget.setWindowTitle(QtGui.QApplication.translate("transferAttrUv_QWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.actions_groupBox.setTitle(QtGui.QApplication.translate("transferAttrUv_QWidget", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.copy_uv_checkBox.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "Copy UV", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_history_checkBox.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "Delete history", None, QtGui.QApplication.UnicodeUTF8))
        self.unlock_tr_checkBox.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "Unlock transfrom", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_color_sets_checkBox.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "Delete color sets", None, QtGui.QApplication.UnicodeUTF8))
        self.create_sets_checkBox.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "Create sets", None, QtGui.QApplication.UnicodeUTF8))
        self.copy_attr_checkBox.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "Copy user attr", None, QtGui.QApplication.UnicodeUTF8))
        self.searchingMethod_groupBox.setTitle(QtGui.QApplication.translate("transferAttrUv_QWidget", "Searching method", None, QtGui.QApplication.UnicodeUTF8))
        self.search_by_topology_checkBox.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "By topology", None, QtGui.QApplication.UnicodeUTF8))
        self.search_by_shape_checkBox.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "By shape name", None, QtGui.QApplication.UnicodeUTF8))
        self.render_char_build_button.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "Do", None, QtGui.QApplication.UnicodeUTF8))
        self.print_match_pushButton.setText(QtGui.QApplication.translate("transferAttrUv_QWidget", "Print Match", None, QtGui.QApplication.UnicodeUTF8))

