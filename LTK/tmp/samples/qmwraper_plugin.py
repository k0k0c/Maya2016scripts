# coding=utf-8
__author__ = 'korovkin_m'


# coding=utf-8
from PyQt4 import QtDesigner, QtGui, QtCore
import sys

LGT_PATCH = 'p:/lib/setup/maya/maya_scripts_rfm4/LGT/test'
sys.path.append(LGT_PATCH)

import qmwraper



class QMainWindowWrapperPlugin(QtDesigner.QPyDesignerCustomWidgetPlugin):
    """
    QMainWindowWrapper
    """

    def __init__(self, parent=None):
        QtDesigner.QPyDesignerCustomWidgetPlugin.__init__(self, parent)
        self.initialized = True

    def createWidget(self, parent):
        # метод должен вернуть экземпляр класса нашего виджета
        # вот тут и пригодилось согласование с принятым в Qt4 API
        return qmwraper.QMainWindowWrapper(parent)

    def name(self):
        # этод метод должен вернуть имя класса виджета
        return "QMainWindowWrapper"

    def group(self):
        # имя группы виджета
        return "PyQt custom widgets"

    def icon(self):
        # иконка виджета
        return QtGui.QIcon()

    def toolTip(self):
        # всплывающая подсказка
        return "QMainWindow Wrapper"

    def whatsThis(self):
        # краткое описание
        return "Custom widget QMainWindowWrapper"

    def isContainer(self):
        # True, если виджет может служить контейнером других виджетов,
        # при этом требуется реализация QDesignerContainerExtension
        # False в противном случае
        return True

    def domXml(self):
        # должен вернуть XML-описание виджета и параметры его свойств.
        # минимально -- класс и имя экземпляра класса
        # вставляется в .ui
        return '<widget class="QMainWindowWrapper" name=\"mainWindowWrapper\" />\n'

    def includeFile(self):
        # возвращает имя модуля, в котором хранится наш виджет
        # вставляется как `import <includeFile>` в генеренном из .ui Python-коде
        return "widget"