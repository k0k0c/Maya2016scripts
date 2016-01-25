import LTK.config

from PySide import QtGui
import inspect

from PySide.QtGui import *
from PySide.QtCore import *

import maya.mel as mel

import func.ltk_func as func
import func.maya_func as maya
import func.ui_to_py as ui_to_py
import func.setsOperator as sets

reload(func)
reload(maya)
reload(ui_to_py)
reload(sets)

import ui.pyuic as ui
reload(ui)


class Ui_ltk_setup(QDockWidget, QWidget):
    def __init__(self, parent=func.getMayaWindow()):
        super(Ui_ltk_setup, self).__init__(parent)
        self.maya_dock = self.parent().findChildren((QtGui.QDockWidget), 'dockControl1')
        self.mainWindow = parent
        self.mainWindow.tabifyDockWidget(self.maya_dock[-1], self)
        self.ui = ui.LTK_main_ui.Ui_LTK()
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.ui.setupUi(self)
        self.objname = QObject.objectName(self)
        childock = self.ui.Tools.findChildren(QtGui.QDockWidget)
        self.submain = QMainWindow(self)
        self.ui.verticalLayout_9.addWidget(self.submain)
        self.cw = QtGui.QListWidget(self.submain)
        self.cw.hide()
        self.submain.setCentralWidget(self.cw)
        for dock in childock:
            self.submain.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.guirestore(self.ui)
        self.connect_interface()

    def do_chr_rnd_copy(self, fm=False):
        mayafoo = maya.MayaFoo()
        uv = self.ui.copy_uv_checkBox.checkState() == 2 and True or False
        atr = self.ui.copy_attr_checkBox.checkState() == 2 and True or False
        sm = self.ui.search_by_shape_checkBox.checkState() == 2 and True or False
        tpl = self.ui.search_by_topology_checkBox.checkState() == 2 and True or False
        sets = self.ui.create_sets_checkBox.checkState() == 2 and True or False
        history = self.ui.delete_history_checkBox.checkState() == 2 and True or False
        colorsets = self.ui.delete_color_sets_checkBox.checkState() == 2 and True or False
        unlocktr = self.ui.unlock_tr_checkBox.checkState() == 2 and True or False
        if not fm:
            mayafoo.transfer(uv=uv, shapename=sm, topology=tpl, atr=atr, sets=sets, history=history,
                             colorsets=colorsets,
                             unlock=unlocktr)
        if fm:
            print mayafoo.find_match(shapename=sm, topology=tpl, sets=sets)

    @staticmethod
    def del_attr():
        mayafoo = maya.MayaFoo()
        mayafoo.delete_user_attr()

    def setsOp(self, setname):
        ci = sets.setsOperator(setname)
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            return ci.select()
        elif modifiers == Qt.AltModifier:
            return ci.exclude()
        elif modifiers == Qt.ControlModifier:
            return ci.visibility()
        else:
            return ci.add()

    def connect_interface(self):
        self.ui.render_char_build_button.clicked.connect(lambda: self.do_chr_rnd_copy())
        self.ui.attr_tools_del_pushButton.clicked.connect(lambda: self.del_attr())
        self.ui.print_match_pushButton.clicked.connect(lambda: self.do_chr_rnd_copy(fm=True))
        self.ui.MELverpushButton.clicked.connect(
            lambda: mel.eval('source "//SERVER-3D/Project/lib/setup/maya/maya_scripts_rfm4/LGT/runLGT";addCRClocUI;'))
        # self.ui.nearRenderPlaneButton.clicked.connect(lambda: self.setsOp("ltkNear_set"))
        # self.ui.midRenderPlaneButton.clicked.connect(lambda: self.setsOp("ltkMid_set"))
        # self.ui.farRenderPlaneButton.clicked.connect(lambda: self.setsOp("ltkFar_set"))

    def guisave(self):
        settings = QSettings(self.objname, self.objname)
        settings.beginGroup('MainWindow')
        for name, obj in inspect.getmembers(self.ui):
            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                state = obj.checkState()
                settings.setValue(name, state)
        settings.endGroup()
        self.deleteLater()

    def guirestore(self, ui=None):
        settings = QSettings(self.objname, self.objname)
        settings.beginGroup('MainWindow')
        for name, obj in inspect.getmembers(ui):
            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                value = settings.value(name)  # get stored value from registry
                if value == 1:
                    obj.setCheckState(Qt.Checked)  # restore checkbox
                if value == 0:
                    obj.setCheckState(Qt.Unchecked)  # restore checkbox
        settings.endGroup()

    def closeEvent(self, event):
        self.guisave()
        event.accept()

    def startup(self):
        LTK = func.getMayaWindow().findChildren(QtGui.QDockWidget, self.objname)
        if len(LTK) > 1:
            for i in range(len(LTK) - 1):
                LTK[i-1].close()
        LTK = LTK[0]
        if func.getMayaWindow().tabifiedDockWidgets(LTK):
            func.getMayaWindow().tabifyDockWidget(func.getMayaWindow().tabifiedDockWidgets(LTK)[0], LTK)
        LTK.show()


def startup():
    ui_to_py.init()
    LTK = Ui_ltk_setup()
    LTK.startup()

if __name__ == "__main__":
    # import LTK.setup as LTK
    import sys
    app = QtGui.QApplication([])
    window = Ui_ltk_setup()
    window.show()
    sys.exit(app.exec_())

    reload(LTK)
    LTK.startup()
