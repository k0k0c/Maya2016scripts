import shiboken as sip
import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
from PySide import QtGui, QtCore


def getMayaWindow():
    'Get the maya main window as a QMainWindow instance'
    ptr = apiUI.MQtUtil.mainWindow()
    return sip.wrapInstance(long(ptr), QtCore.QObject)


def getFocusWidget():
    'Get the currently focused widget'
    return QtGui.qApp.focusWidget()


def layout_widgets(layout):
    """Get widgets contained in layout"""
    return [layout.itemAt(i).widget() for i in range(layout.count())]

def getWidgetAtMouse():
    'Get the widget under the mouse'
    currentPos = QtGui.QCursor().pos()
    widget = QtGui.qApp.widgetAt(currentPos)
    widgetParent = widget.parent()


    # QtGui.QVBoxLayout.__instancecheck__()
    print(widgetParent)
    print(widgetParent)
    widgetParentLayout = widgetParent.layout()
    print(widgetParentLayout)
    result = findWidgetInLayout(widgetParentLayout, widget)
    print result[0], result[0].objectName()
    print result[1], result[1].objectName()
    return result

def findWidgetInLayout(layout, widget):
    count = layout.count()
    found = False
    for i in range(count):
        item = layout.itemAt(i).widget()
        if item == widget:
            found =True
            return layout, widget
    if not found:
        return findLayoutInLayout(layout, widget)

def findLayoutInLayout(layout, widget):
    layouts = layout.findChildren(QtGui.QLayout)
    print "===findLayoutInLayout==="
    for item in layouts:
        return findWidgetInLayout(item, widget)

