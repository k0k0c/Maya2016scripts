import sys
import sip

from PyQt4 import QtGui, QtCore
import inspect

from PyQt4.QtGui import *
from PyQt4.QtCore import *

LGT_PATCH = '//SERVER-3D/Project/lib/setup/maya/maya_scripts_rfm4/LGT'

sys.path.append(LGT_PATCH)

import globalProcs_lgt as gproc

reload(gproc)

import ui_to_py

reload(ui_to_py)

from lgt_py import addCRCloc_test, find_match_widget

reload(addCRCloc_test)
reload(find_match_widget)


class Ui_lgt(QtGui.QDockWidget, addCRCloc_test.Ui_Lighter_Tools):
    def __init__(self, parent=gproc.getMayaWindow(), *args):
        super(Ui_lgt, self).__init__(parent)
        self.maya_dock = self.parent().findChildren((QtGui.QDockWidget), 'dockControl1')
        self.setObjectName('Lighter_Tools')
        self.guirestore()
        self.mainWindow = parent
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.mainWindow.tabifyDockWidget(self.maya_dock[0], self)
        self.setupUi(self)

    def do_chr_rnd_copy(self):
        uv = self.copy_uv_checkBox.checkState() == 2 and True or False
        sm = self.search_by_shape_checkBox.checkState() == 2 and True or False
        tpl = self.search_by_topology_checkBox.checkState() == 2 and True or False
        sets = self.create_sets_checkBox.checkState() == 2 and True or False
        history = self.delete_history_checkBox.checkState() == 2 and True or False
        crb = gproc.CharRenderBuild()
        crb.copy_user_attr(uv=uv, shapename=sm, topology=tpl, sets=sets, history=history)

    def connect_interface(self):
        self.render_char_build_button.clicked.connect(self.do_chr_rnd_copy)

    def guisave(self):
        settings = QSettings('Lighter_Tools', 'Lighter_Tools')
        settings.beginGroup('MainWindow')
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                state = obj.checkState()
                settings.setValue(name, state)
        settings.endGroup()
        self.deleteLater()

    def guirestore(self, ui=None):
        settings = QSettings('Lighter_Tools', 'Lighter_Tools')
        settings.beginGroup('MainWindow')
        for name, obj in inspect.getmembers(ui):
            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                value = QVariant.toPyObject(settings.value(name))  # get stored value from registry
                if value != None:
                    obj.setCheckState(value)  # restore checkbox
        settings.endGroup()

    def closeEvent(self, event):
        # event.ignore()
        self.guisave()
        event.accept()


class Ui_lgt_table_wiget(Ui_lgt, find_match_widget.Ui_find_match_widget, QWidget):
    def __init__(self, mainWindow=gproc.getMayaWindow()):
        super(Ui_lgt_table_wiget, self).__init__(mainWindow)
        self.window = QWidget()
        self.setObjectName('Find match')

    def init_ui(self):
        self.setupUi(self.window)
        self.window.show()


def startup():
    ui_to_py.init()
    mainWindowInstances = gproc.getMayaWindow().findChildren(QtGui.QDockWidget, 'Lighter_Tools')
    for mainWindowInstance in mainWindowInstances:
        # print mainWindowInstance
        mainWindowInstance.close()
    lgt_window = Ui_lgt()
    # lgt_matchtable = Ui_lgt_table_wiget()
    # lgt_matchtable.init_ui()
    lgt_window.show()
    lgt_window.connect_interface()
    lgt_window.guirestore(ui=lgt_window)
