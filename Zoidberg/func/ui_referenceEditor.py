import maya.cmds as cmds
import maya.mel as mel
import shiboken as sip
import sys
import os
import linecache
import re
from PySide import QtCore, QtGui
import maya.OpenMayaUI as mui
import ml_reference
import listFromView
import json
import Zoidberg.config as cfg

WINUSER = cfg.WINUSER

reload(ml_reference)
OSTYPE = sys.platform != "win32" and "c:/" or "c:/"

globaljobBatchContextLE = ""


def testPrint(stp):
    print(stp)


def exception():
    print "\nEXPECTED ERROR {"
    extype, exobj, traceback = sys.exc_info()
    lineno = traceback.tb_lineno
    nfile = traceback.tb_frame
    filename = nfile.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, nfile.f_globals)
    linestp = line.strip()
    linestp = linestp and linestp or "<module>"
    result = "# Error: {3}# Traceback (most recent call last):\n# \tFile {0}, line {1}, in {2}\n# {4}: {3}".format(
            filename, lineno, linestp, exobj, extype.__name__)
    print result
    print "}"
    return result


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    if ptr is not None:
        return sip.wrapInstance(long(ptr), QtGui.QWidget)


class referenceEditor(QtGui.QDialog):
    def __init__(self, parent=getMayaWindow()):
        super(referenceEditor, self).__init__(parent)
        self.delegate = itemDelegate()
        self.mainlayout = QtGui.QVBoxLayout()
        self.mainlayout.setContentsMargins(0, 0, 0, 0, )
        self.setLayout(self.mainlayout)
        self.setProperty("index", "References")
        self.setObjectName("referenceEditor")
        self.OSTYPE = sys.platform != "win32" and "c:/" or "c:/"
        self.isLoad = False

    def load(self):
        self.mainMenuBar = QtGui.QMenuBar(self)
        self.mainlayout.addWidget(self.mainMenuBar)
        self.fileMenu = QtGui.QMenu("File")
        self.fileMenu.setTearOffEnabled(True)
        self.mainMenuBar.addMenu(self.fileMenu)
        self.loadPresetStateAction = QtGui.QAction("Load preload preset", self)
        self.loadPresetStateAction.triggered.connect(self.loadPresetForScene)
        self.fileMenu.addAction(self.loadPresetStateAction)
        self.savePresetStateAction = QtGui.QAction("Save preload preset", self)
        self.savePresetStateAction.triggered.connect(self.saveScenePreset)
        self.fileMenu.addAction(self.savePresetStateAction)
        self.fileMenu.addSeparator()
        self.loadReferencePresetStateAction = QtGui.QAction("Load reference preload preset", self)
        self.loadReferencePresetStateAction.triggered.connect(self.loadPresetForCurrentReference)
        self.fileMenu.addAction(self.loadReferencePresetStateAction)
        self.saveReferencePresetStateAction = QtGui.QAction("Save reference preload preset", self)
        self.saveReferencePresetStateAction.triggered.connect(self.saveReferencePreset)
        self.fileMenu.addAction(self.saveReferencePresetStateAction)
        self.fileMenu.addSeparator()
        self.refreshViewAction = QtGui.QAction("Refresh reference editor view", self)
        self.refreshViewAction.triggered.connect(self.updateGUI)
        self.fileMenu.addAction(self.refreshViewAction)
        self.referenceMenu = QtGui.QMenu("Reference")
        self.referenceMenu.setTearOffEnabled(True)
        self.mainMenuBar.addMenu(self.referenceMenu)
        self.reloadReferenceMenu = QtGui.QMenu("Reload as")
        self.referenceMenu.addMenu(self.reloadReferenceMenu)
        self.referenceDepthDefaultAction = QtGui.QAction("Default", self)
        self.referenceDepthDefaultAction.triggered.connect(self.reload)
        self.reloadReferenceMenu.addAction(self.referenceDepthDefaultAction)
        self.referenceDepthFullAction = QtGui.QAction("All included references", self)
        self.referenceDepthFullAction.triggered.connect(self.reloadFull)
        self.reloadReferenceMenu.addAction(self.referenceDepthFullAction)
        self.referenceDepthTopOnlyAction = QtGui.QAction("Top only reference", self)
        self.referenceDepthTopOnlyAction.triggered.connect(self.reloadTopOnly)
        self.reloadReferenceMenu.addAction(self.referenceDepthTopOnlyAction)
        self.referenceDepthNoneAction = QtGui.QAction("None references", self)
        self.referenceDepthNoneAction.triggered.connect(self.reloadNone)
        self.reloadReferenceMenu.addAction(self.referenceDepthNoneAction)
        self.referenceDepthOriginalAction = QtGui.QAction("Original references", self)
        self.referenceDepthOriginalAction.triggered.connect(self.reloadOriginal)
        self.reloadReferenceMenu.addAction(self.referenceDepthOriginalAction)
        self.referenceDepthProxyAction = QtGui.QAction("Proxy references", self)
        self.referenceDepthProxyAction.triggered.connect(self.reloadProxy)
        self.reloadReferenceMenu.addAction(self.referenceDepthProxyAction)
        self.unloadReferenceAction = QtGui.QAction("Unload reference", self)
        self.unloadReferenceAction.triggered.connect(self.unload)
        self.referenceMenu.addAction(self.unloadReferenceAction)
        self.referenceMenu.addSeparator()
        self.openReferenceAction = QtGui.QAction("Open reference", self)
        self.openReferenceAction.triggered.connect(self.openReferenceInNewMaya)
        self.referenceMenu.addAction(self.openReferenceAction)
        self.referenceMenu.addSeparator()
        self.importReferenceAction = QtGui.QAction("import reference", self)
        self.importReferenceAction.triggered.connect(self.importReference)
        self.referenceMenu.addAction(self.importReferenceAction)
        self.removeReferenceAction = QtGui.QAction("Remove reference", self)
        self.referenceMenu.addAction(self.removeReferenceAction)
        self.removeReferenceAction.triggered.connect(self.removeReference)
        self.proxyMenu = QtGui.QMenu("Proxy")
        self.proxyMenu.setTearOffEnabled(True)
        self.mainMenuBar.addMenu(self.proxyMenu)
        self.addProxyAction = QtGui.QAction("Add proxy", self)
        self.addProxyAction.triggered.connect(self.addProxy)
        self.proxyMenu.addAction(self.addProxyAction)
        self.addDefaultProxyAction = QtGui.QAction("Add proxy, available for reference", self)
        self.addDefaultProxyAction.triggered.connect(self.addDefaultProxy)
        self.proxyMenu.addAction(self.addDefaultProxyAction)
        self.proxyMenu.addSeparator()
        self.switchToNextProxyAction = QtGui.QAction("Load reference as next available proxy", self)
        self.switchToNextProxyAction.triggered.connect(self.switchProxyNext)
        self.proxyMenu.addAction(self.switchToNextProxyAction)
        self.switchToOriginalAction = QtGui.QAction("Load reference as original", self)
        self.switchToOriginalAction.triggered.connect(self.switchToOriginal)
        self.proxyMenu.addAction(self.switchToOriginalAction)
        self.removeEmptyProxyAction = QtGui.QAction("Remove empty proxy", self)
        self.removeEmptyProxyAction.triggered.connect(self.removeEmptyReferences)
        self.proxyMenu.addAction(self.removeEmptyProxyAction)
        self.proxyMenu.addSeparator()
        self.switchProxyMenu = QtGui.QMenu("Switch to ...")
        self.proxyMenu.addMenu(self.switchProxyMenu)
        self.editsMenu = QtGui.QMenu("Edits")
        self.editsMenu.setTearOffEnabled(True)
        self.mainMenuBar.addMenu(self.editsMenu)
        self.showEditsAction = QtGui.QAction("Show edits for selected references", self)
        self.showEditsAction.triggered.connect(self.updateEditsEditor)
        self.editsMenu.addAction(self.showEditsAction)
        self.editsMenu.addSeparator()
        self.exportEditsAction = QtGui.QAction("Export edits from selected references", self)
        self.exportEditsAction.triggered.connect(self.exportEdits)
        self.editsMenu.addAction(self.exportEditsAction)
        self.removeEditsAction = QtGui.QAction("Remove edits from current scene for selected references", self)
        self.editsMenu.addAction(self.removeEditsAction)
        self.removeEditsAction.triggered.connect(self.cleanUpReferences)
        self.selectMenu = QtGui.QMenu("Selection")
        self.selectMenu.setTearOffEnabled(True)
        self.mainMenuBar.addMenu(self.selectMenu)
        self.selectFromOutlinerAction = QtGui.QAction("Select references from outliner", self)
        self.selectFromOutlinerAction.triggered.connect(self.selectFromOutliner)
        self.selectMenu.addAction(self.selectFromOutlinerAction)
        self.selectFromReferenceEditorAction = QtGui.QAction("Select references from reference editor", self)
        self.selectFromReferenceEditorAction.triggered.connect(self.selectFromReferenceEditor)
        self.selectMenu.addAction(self.selectFromReferenceEditorAction)
        self.selectMenu.addSeparator()

        self.selectFromInvertViewAction = QtGui.QAction("Select references from outside view", self)
        self.selectFromInvertViewAction.setCheckable(True)
        self.selectMenu.addAction(self.selectFromInvertViewAction)

        self.selectFromViewAction = QtGui.QAction("Select references from view", self)
        self.selectFromViewAction.triggered.connect(self.selectFromView)
        self.selectMenu.addAction(self.selectFromViewAction)
        self.selectFromViewWithAnimationAction = QtGui.QAction("Select references from view with animation", self)
        self.selectFromViewWithAnimationAction.triggered.connect(self.selectFromViewWithAnimation)
        self.selectMenu.addAction(self.selectFromViewWithAnimationAction)
        self.selectMenu.addSeparator()
        self.invertSelectionAction = QtGui.QAction("Invert selection", self)
        self.invertSelectionAction.triggered.connect(self.invertSelection)
        self.selectMenu.addAction(self.invertSelectionAction)
        self.selectMenu.addSeparator()
        self.selectReferenceContentAction = QtGui.QAction("Select reference content", self)
        self.selectReferenceContentAction.triggered.connect(self.selectReferenceContent)
        self.selectMenu.addAction(self.selectReferenceContentAction)
        self.selectReferenceNodesAction = QtGui.QAction("Select reference nodes", self)
        self.selectReferenceNodesAction.triggered.connect(self.selectReferenceNode)
        self.selectMenu.addAction(self.selectReferenceNodesAction)
        self.selectMenu.addSeparator()
        self.expandTreeAction = QtGui.QAction("Expand view", self)
        self.expandTreeAction.triggered.connect(self.expandTree)
        self.selectMenu.addAction(self.expandTreeAction)
        self.mainSplitter = QtGui.QSplitter()
        self.mainSplitter.setOrientation(QtCore.Qt.Vertical)
        self.referenceInfoWidget = QtGui.QWidget()
        self.referenceInfoWidget.setMaximumHeight(90)
        self.referenceInfoLayout = QtGui.QGridLayout()
        self.referenceInfoLayout.setContentsMargins(0, 0, 0, 0, )
        self.referenceInfoWidget.setLayout(self.referenceInfoLayout)
        self.mainSplitter.addWidget(self.referenceInfoWidget)
        self.referenceNameLabel = QtGui.QLabel("Filename:")
        self.referenceInfoLayout.addWidget(self.referenceNameLabel, 0, 0)
        self.referenceNameLineEdit = QtGui.QLineEdit("")
        self.referenceNameLineEdit.returnPressed.connect(self.remapFilename)
        self.referenceInfoLayout.addWidget(self.referenceNameLineEdit, 0, 1)
        self.referenceResolvedNameLabel = QtGui.QLabel("Resolved name:")
        self.referenceInfoLayout.addWidget(self.referenceResolvedNameLabel, 1, 0)
        self.referenceResolvedNameLineEdit = QtGui.QLineEdit("")
        self.referenceResolvedNameLineEdit.setEnabled(False)
        self.referenceInfoLayout.addWidget(self.referenceResolvedNameLineEdit, 1, 1)
        self.referenceNamespaceLabel = QtGui.QLabel("Namespace:")
        self.referenceInfoLayout.addWidget(self.referenceNamespaceLabel, 2, 0)
        self.referenceNamespaceLineEdit = QtGui.QLineEdit("")
        self.referenceNamespaceLineEdit.returnPressed.connect(self.remapNamespace)
        self.referenceInfoLayout.addWidget(self.referenceNamespaceLineEdit, 2, 1)
        self.reloadButton = QtGui.QPushButton("Reload")
        self.referenceInfoLayout.addWidget(self.reloadButton, 0, 2)
        self.reloadButton.released.connect(self.reload)
        self.unloadButton = QtGui.QPushButton("Unload")
        self.referenceInfoLayout.addWidget(self.unloadButton, 1, 2)
        self.unloadButton.released.connect(self.unload)
        self.removeButton = QtGui.QPushButton("Remove")
        self.referenceInfoLayout.addWidget(self.removeButton, 2, 2)
        self.removeButton.released.connect(self.removeReference)
        self.referenceTreeWidget = QtGui.QWidget()
        self.referenceTreeLayout = QtGui.QVBoxLayout()
        self.referenceTreeLayout.setContentsMargins(0, 0, 0, 0)
        self.referenceTreeWidget.setLayout(self.referenceTreeLayout)
        self.filterWidget = QtGui.QWidget()
        self.filterLayout = QtGui.QHBoxLayout()
        self.filterWidget.setLayout(self.filterLayout)
        self.filterIconOff = QtGui.QIcon()
        self.filterIconOn = QtGui.QIcon()
        self.filterPixmapOff = QtGui.QPixmap(
            cfg.RESURCES_PATCH + "filterOff.png")
        self.filterPixmapOn = QtGui.QPixmap(
            cfg.RESURCES_PATCH + "filterOn.png")
        self.filterIconOn.addPixmap(self.filterPixmapOn)
        self.filterIconOff.addPixmap(self.filterPixmapOff)
        self.resetFilterButton = QtGui.QPushButton("")
        self.resetFilterButton.setIcon(self.filterIconOff)
        self.resetFilterButton.setStyleSheet(
                "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,90,90) }")
        self.resetFilterButton.released.connect(self.resetSortRegexpTree)
        self.filterLayout.addWidget(self.resetFilterButton)
        self.filterReference = QtGui.QLineEdit("")
        self.filterReference.returnPressed.connect(self.sortRegexpTree)
        self.filterLayout.addWidget(self.filterReference)
        self.referenceTreeLayout.addWidget(self.filterWidget)
        self.mainTree = QtGui.QTreeView()
        self.mainTree.setExpandsOnDoubleClick(False)
        # self.mainTree.setStyleSheet("""
        # QTreeView::branch:has-siblings:!adjoins-item {
        #     border-image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-vline.png) 0;
        # }
        # QTreeView::branch:has-siblings:adjoins-item {
        #    border-image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-branch-more.png) 0;
        # }
        # QTreeView::branch:!has-children:!has-siblings:adjoins-item {
        #    border-image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-branch-end.png) 0;
        # }
        # QTreeView::branch:has-children:!has-siblings:closed,
        # QTreeView::branch:closed:has-children:has-siblings {
        #    border-image: none;
        #    image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-branch-closed.png);
        # }
        # QTreeView::branch:open:has-children:!has-siblings,
        # QTreeView::branch:open:has-children:has-siblings  {
        #    border-image: none;
        #    image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-branch-open.png);
        # }""")
        self.connect(self.delegate, QtCore.SIGNAL("itemCheckChange(const QModelIndex &)"), self.toogleLoadState)
        self.connect(self.delegate, QtCore.SIGNAL("itemExpanded(const QModelIndex &)"), self.setExpanded)
        self.mainTree.setItemDelegate(self.delegate)
        self.mainTree.setAlternatingRowColors(True)
        self.mainTree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.mainTree.setSelectionMode(QtGui.QTreeView.ExtendedSelection)
        self.mainTree.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.mainTree.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.mainTree.setSelectionBehavior(QtGui.QTreeView.SelectRows)
        self.mainTree.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mainTree.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.baseModel = QtGui.QStandardItemModel()
        self.proxyModel = customProxyFilter()  # QtGui.QSortFilterProxyModel()
        self.proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxyModel.setSourceModel(self.baseModel)
        self.mainTree.setModel(self.proxyModel)
        self.mainTree.setHeaderHidden(True)
        # self.mainTree.doubleClicked.connect( self.toogleLoadState )
        self.referenceTreeLayout.addWidget(self.mainTree)
        self.mainSplitter.addWidget(self.referenceTreeWidget)
        self.referenceEditsWidget = QtGui.QWidget()
        self.referenceEditsLayout = QtGui.QVBoxLayout()
        self.referenceEditsLayout.setContentsMargins(0, 0, 0, 0)
        self.referenceEditsWidget.setLayout(self.referenceEditsLayout)
        self.referenceEditsEditor = ReferenceEditsEditor()
        self.referenceEditsLayout.addWidget(self.referenceEditsEditor)
        self.m_actionEditsWidget = QtGui.QWidget()
        self.m_actionEditsWidget.setMaximumHeight(30)
        self.m_actionEditsLayout = QtGui.QHBoxLayout()
        self.m_actionEditsLayout.setContentsMargins(0, 0, 0, 0)
        self.m_actionEditsWidget.setLayout(self.m_actionEditsLayout)
        self.m_removeEditsButton = QtGui.QPushButton("Remove")
        self.m_removeEditsButton.released.connect(self.referenceEditsEditor.removeEdits)
        self.m_actionEditsLayout.addWidget(self.m_removeEditsButton)
        self.m_refreshCurrentEditsButton = QtGui.QPushButton("Refresh")
        self.m_refreshCurrentEditsButton.released.connect(self.updateEditsEditor)
        self.m_actionEditsLayout.addWidget(self.m_refreshCurrentEditsButton)
        self.referenceEditsLayout.addWidget(self.m_actionEditsWidget)
        self.mainSplitter.addWidget(self.referenceEditsWidget)
        self.mainlayout.addWidget(self.mainSplitter)
        self.mainTreeSM = self.mainTree.selectionModel()
        self.mainTreeSM.selectionChanged.connect(self.updateEditor)
        self.updateGUI()
        self.updateEditor()
        self.setWindowTitle("Reference editor")
        self.isLoad = True

    def setExpanded(self, index):
        boolean = not self.mainTree.isExpanded(index) and True or False
        self.mainTree.setExpanded(index, boolean)

    def updateEditsEditor(self):
        referenceNodes = self.getSelected()
        self.referenceEditsEditor.setReferences(referenceNodes)

    def resetSortRegexpTree(self):
        self.proxyModel.setFilterRegExp("")
        self.resetFilterButton.setIcon(self.filterIconOff)
        # self.resetFilterButton.setStyleSheet( "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,90,90) }" )

    def sortRegexpTree(self):
        expr = self.filterReference.text()
        self.proxyModel.setFilterRegExp(expr)
        if expr != "":
            self.resetFilterButton.setIcon(self.filterIconOn)
            # self.resetFilterButton.setStyleSheet( "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,180,90) }" )
        else:
            self.resetFilterButton.setIcon(self.filterIconOff)
            # self.resetFilterButton.setStyleSheet( "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,90,90) }" )

    def updateGUI(self):
        print "     ++ updateGUI"
        self.baseModel.clear()
        self.updateValidReferences()
        self.build(update=True)

    def build(self, parent=None, reference="", update=False, data=[]):
        if update is True:
            data = []
        if not parent:
            root = self.baseModel.invisibleRootItem()
        else:
            root = parent
        if reference == "":
            references = cmds.file(query=True, reference=True)
        else:
            references = cmds.file(reference, query=True, reference=True)
        for i in range(0, len(references)):
            namespace = cmds.file(references[i], query=True, renamingPrefix=True)
            name = self.referenceInfo(references[i])
            proxy = name[1]
            unknown = name[2]
            name = name[0]
            loaded = False
            rfn = ""
            if cmds.objExists(name):
                rfn = name
            else:
                rfn = cmds.file(references[i], query=True, referenceNode=True)
            if rfn:
                loaded = cmds.referenceQuery(rfn, isLoaded=True)
            loaded = loaded is True and 1 or 0
            if name not in data:
                if cmds.objExists(name) and cmds.nodeType(name) == "reference":
                    path = cmds.referenceQuery(name, filename=True)
                elif not os.path.isfile(name):
                    path = references[i]
                else:
                    path = name
                data.append(name)
                item = QtGui.QStandardItem(name)
                item.setCheckable(True)
                item.setData(name, QtCore.Qt.DisplayRole)
                item.setData(name.split(":")[-1], QtCore.Qt.DisplayRole + 1)
                item.setData(unknown, QtCore.Qt.UserRole + 3)
                item.setData(proxy, QtCore.Qt.UserRole + 4)
                item.setData(path, QtCore.Qt.UserRole + 5)
                item.setData(namespace, QtCore.Qt.UserRole + 6)
                item.setData(loaded, QtCore.Qt.UserRole + 7)
                root.setChild(root.rowCount(), item)
                self.build(parent=item, reference=references[i], data=data)

    def updateItem(self, item):
        self.data = []
        self.removeItemChilds(item)
        itemName = str(item.data(QtCore.Qt.DisplayRole))
        reference = itemName
        if cmds.objExists(reference):
            reference = cmds.referenceQuery(reference, filename=True)
        namespace = cmds.file(reference, query=True, renamingPrefix=True)
        name = self.referenceInfo(reference)
        loaded = False
        proxy = name[1]
        unknown = name[2]
        name = name[0]
        if cmds.objExists(name) and cmds.nodeType(name) == "reference":
            print "updateItem", name
            rfn = name
        else:
            rfn = cmds.file(reference, query=True, referenceNode=True)
        if rfn:
            loaded = cmds.referenceQuery(rfn, isLoaded=True)
        loaded = loaded is True and 1 or 0
        item.setData(name, QtCore.Qt.DisplayRole)
        item.setData(unknown, QtCore.Qt.UserRole + 3)
        item.setData(proxy, QtCore.Qt.UserRole + 4)
        item.setData(reference, QtCore.Qt.UserRole + 5)
        item.setData(namespace, QtCore.Qt.UserRole + 6)
        item.setData(loaded, QtCore.Qt.UserRole + 7)
        self.updateValidReferences()
        self.build(parent=item, reference=reference, update=True)

    def removeEmptyReferences(self):
        references = cmds.ls(type="reference")
        if references:
            for reference in references:
                if cmds.listConnections(type="proxyManager"):
                    try:
                        cmds.referenceQuery(reference, filename=True)
                    except:
                        try:
                            mel.eval("proxyRemove %s" % reference)
                        except:
                            exception()

    def updateEditor(self):
        selected = self.getSelectedItems()
        selectedLenght = len(selected)
        actions = self.switchProxyMenu.actions()
        if actions:
            for i in range(0, len(actions)):
                self.switchProxyMenu.removeAction(actions[i])
        if selectedLenght == 1:
            self.switchProxyMenu.setEnabled(True)
            resolved = str(selected[0].data(QtCore.Qt.UserRole + 5))
            namespace = str(selected[0].data(QtCore.Qt.UserRole + 6))
            filename = resolved.split("{")[0]
            self.referenceNameLineEdit.setText(filename)
            self.referenceNameLineEdit.setEnabled(True)
            self.referenceResolvedNameLineEdit.setText(resolved)
            self.referenceNamespaceLineEdit.setText(namespace)
            self.referenceNamespaceLineEdit.setEnabled(True)
            path = str(selected[0].data(QtCore.Qt.UserRole + 5))
            rfn = cmds.file(path, query=True, rfn=True)
            references = self.listAvalaibleProxy(rfn)
            if references:
                for node in references:
                    self.makeSwitchProxyAction(rfn, node)
            else:
                self.switchProxyMenu.setEnabled(False)
        else:
            self.switchProxyMenu.setEnabled(False)
            self.referenceNameLineEdit.setText("N/A")
            self.referenceNameLineEdit.setEnabled(False)
            self.referenceResolvedNameLineEdit.setText("N/A")
            self.referenceNamespaceLineEdit.setText("N/A")
            self.referenceNamespaceLineEdit.setEnabled(False)

    def makeSwitchProxyAction(self, src, dst):
        rfnAction = QtGui.QAction(dst, self)
        if src != dst:
            rfnAction.triggered.connect(lambda: self.switchProxyTo(src, dst))
        else:
            rfnAction.setEnabled(False)
        self.switchProxyMenu.addAction(rfnAction)

    def listReferencesFromNodes(self, nodes):
        paths = []
        for i in range(0, len(nodes)):
            if cmds.referenceQuery(nodes[i], isNodeReferenced=True):
                rfn = cmds.referenceQuery(nodes[i], rfn=True)
                references = [rfn]
                if rfn:
                    pm = cmds.listConnections(rfn, type="proxyManager")
                    if pm:
                        proxy = cmds.listConnections(pm, type="reference")
                        [references.append(proxy[r]) for r in range(0, len(proxy)) if proxy[r] not in references]
                for r in range(0, len(references)):
                    path = cmds.referenceQuery(references[r], filename=True)
                    if path not in paths:
                        paths.append(path)
        return paths

    def selectFromOutliner(self):
        nodes = cmds.ls(sl=True)
        paths = self.listReferencesFromNodes(nodes)
        self.selectItems(paths)

    def selectFromView(self):
        outside = self.selectFromInvertViewAction.isChecked()
        modelEditor = cmds.playblast(activeEditor=True)
        camera = cmds.modelEditor(modelEditor, query=True, camera=True)
        camera = cmds.ls(camera, dag=True, type=["camera", "stereoRigCamera"])
        if camera:
            camera = camera[-1]
            nodes = listFromView.listFromView(camera, outside=outside, animation=False, frustum=0, aspect=1)
            paths = self.listReferencesFromNodes(nodes)
            self.selectItems(paths)

    def selectFromViewWithAnimation(self):
        outside = self.selectFromInvertViewAction.isChecked()
        modelEditor = cmds.playblast(activeEditor=True)
        camera = cmds.modelEditor(modelEditor, query=True, camera=True)
        camera = cmds.ls(camera, dag=True, type=["camera", "stereoRigCamera"])
        if camera:
            camera = camera[-1]
            nodes = listFromView.listFromView(camera, outside=outside, animation=True,
                                              start=cmds.playbackOptions(query=True, animationStartTime=True),
                                              end=cmds.playbackOptions(query=True, animationEndTime=True),
                                              frameSpacing=1, frustum=0, aspect=1)
            paths = self.listReferencesFromNodes(nodes)
            self.selectItems(paths)

    def selectReferenceNode(self):
        cmds.select(clear=True)
        nodes = []
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            rfn = cmds.file(path, query=True, rfn=True)
            if rfn and cmds.objExists(rfn):
                nodes.append(rfn)
        if nodes:
            cmds.select(nodes)

    def invertSelection(self):
        ignore = []
        selected = self.mainTree.selectionModel().selectedIndexes()
        for i in range(0, len(selected)):
            item = self.proxyModel.mapToSource(selected[i])
            item = self.baseModel.itemFromIndex(item)
            ignore.append(item)
        paths = self.listItems(ignoreItems=ignore, paths=True)
        if paths:
            self.selectItems(paths)

    def selectReferenceContent(self):
        cmds.select(clear=True)
        nodes = []
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            rfn = cmds.file(path, query=True, rfn=True)
            if rfn and cmds.objExists(rfn):
                content = cmds.referenceQuery(rfn, nodes=True, dagPath=True)
                if content:
                    nodes = nodes + content
        if nodes:
            cmds.select(nodes)

    def selectFromReferenceEditor(self):
        paths = []
        windowList = cmds.lsUI(windows=True)
        for wl in windowList:
            if re.match(".*referenceEditorPanel.*", wl):
                break
        referencecNodes = mel.eval(
                "global string $gReferenceEditorPanel; sceneEditor -q -selectReference $gReferenceEditorPanel;")
        for i in range(0, len(referencecNodes)):
            rfn = referencecNodes[i]
            references = [rfn]
            if rfn:
                pm = cmds.listConnections(rfn, type="proxyManager")
                if pm:
                    proxy = cmds.listConnections(pm, type="reference")
                    [references.append(proxy[r]) for r in range(0, len(proxy)) if proxy[r] not in references]
            for r in range(0, len(references)):
                path = cmds.referenceQuery(references[r], filename=True)
                if path not in paths:
                    paths.append(path)
        self.selectItems(paths)

    def selectItems(self, paths):
        print paths
        paths = type(paths) is list and paths or [paths]
        root = self.baseModel.invisibleRootItem()
        print root
        smodel = self.mainTree.selectionModel()
        smodel.clearSelection()
        items = self.getChildItems(root)
        for i in range(0, len(items)):
            path = str(items[i].data(QtCore.Qt.UserRole + 5))
            modelindex = self.baseModel.indexFromItem(items[i])
            mappedmodelindex = self.proxyModel.mapFromSource(modelindex)
            print path
            if path in paths:
                smodel.select(mappedmodelindex, QtGui.QItemSelectionModel.Select)
                self.expandItem(mappedmodelindex)
                # self.mainTree.expandAll()

    def getChildItems(self, item, onlyEnabled=False):
        result = []
        for r in range(item.rowCount() - 1, -1, -1):
            child = item.child(r)
            if onlyEnabled is True:
                isEnabled = child.isEnabled()
            else:
                isEnabled = True
            # if child not in result and isEnabled is True:
            if child and isEnabled is True:
                result.append(child)
                descendents = self.getChildItems(child, onlyEnabled=onlyEnabled)
                for i in range(0, len(descendents)):
                    result.append(descendents[i])
        return result

    def expandItem(self, item, query=False):
        result = []
        root = self.baseModel.invisibleRootItem()
        root = self.baseModel.indexFromItem(root)
        root = self.proxyModel.mapFromSource(root)
        parent = item.parent()
        while parent:
            result.append(parent)
            if query is False:
                self.mainTree.expand(parent)
            parent = parent.parent()
            if parent == root:
                break
        return result

    def expandTree(self):
        self.mainTree.expandAll()

    def listItems(self, ignoreItems=[], paths=False, childs=False):
        result = []
        root = self.baseModel.invisibleRootItem()
        items = [root]
        while items:
            childs = []
            for i in range(0, len(items)):
                temp = []
                for n in range(items[i].rowCount() - 1, -1, -1):
                    child = items[i].child(n)
                    if child not in ignoreItems:
                        temp.append(child)
                if not temp:
                    if paths is True:
                        result.append(str(items[i].data(QtCore.Qt.UserRole + 5)))
                    else:
                        result.append(items[i])
                else:
                    childs = childs + temp
            items = childs
        return result

    def remapNamespace(self):
        selected = self.getSelectedItems()
        filename = str(self.referenceNameLineEdit.text())
        namespace = str(self.referenceNamespaceLineEdit.text())
        if selected and len(selected) == 1:
            if os.path.isfile(filename):
                node = str(selected[0].data(QtCore.Qt.DisplayRole))
                if re.findall(".mb|.ma", filename, re.IGNORECASE):
                    if cmds.objExists(node):
                        cmds.file(filename, edit=True, ns=namespace)
                    else:
                        print "Reference not applied for current opened scene."
                else:
                    print "Please specify valid filename."
            else:
                print "File not exists."
        else:
            print "Please select reference."

    def remapFilename(self):
        selected = self.getSelectedItems()
        filename = str(self.referenceNameLineEdit.text())
        if selected and len(selected) == 1:
            if os.path.isfile(filename):
                node = str(selected[0].data(QtCore.Qt.DisplayRole))
                if re.findall(".mb|.ma", filename, re.IGNORECASE):
                    if cmds.objExists(node):
                        cmds.file(filename, options="v=0", loadReference=node)
                    else:
                        print "Reference not applied for current opened scene."
                else:
                    print "Please specify valid filename."
            else:
                print "File not exists."
        else:
            print "Please select reference."

    def getSelectedItems(self):
        result = []
        selected = self.mainTree.selectionModel().selectedIndexes()
        for i in range(0, len(selected)):
            item = self.mainTree.model().mapToSource(selected[i])
            item = self.baseModel.itemFromIndex(item)
            result.append(item)
        return result

    def getSelected(self):
        result = []
        selected = self.mainTree.selectionModel().selectedIndexes()
        for i in range(0, len(selected)):
            m_temp = selected[i].data(QtCore.Qt.DisplayRole)
            m_temp = str(m_temp)
            if m_temp not in result:
                result.append(m_temp)
        return result

    def removeItemChilds(self, item):
        for i in range(item.rowCount() - 1, -1, -1):
            item.removeRow(i)

    def removeItem(self, item):
        parent = item.parent()
        if parent:
            parent.removeRow(item.row())
        else:
            self.baseModel.removeRow(item.row())

    def removeSelected(self):
        selected = self.mainTree.selectionModel().selectedIndexes()
        for i in range(len(selected) - 1, -1, -1):
            item = self.mainTree.model().mapToSource(selected[i])
            item = self.baseModel.itemFromIndex(item)
            parent = item.parent()
            if parent:
                parent.removeRow(item.row())
            else:
                self.baseModel.removeRow(item.row())

    def updateValidReferences(self):
        self.valid = ml_reference.listReferences(referenceNodes=True)

    def referenceInfo(self, reference):
        proxy = 0
        isUnknown = 0
        name = ""
        if cmds.objExists(reference):
            rfn = reference
        else:
            rfn = cmds.file(reference, query=True, rfn=True)
        if rfn:
            connectedReferences = [rfn]
            proxyManager = cmds.listConnections(rfn, type="proxyManager")
            if proxyManager:
                proxyManager = proxyManager[-1]
                temp = cmds.listConnections(proxyManager, type="reference")
                [connectedReferences.append(temp[i]) for i in range(0, len(temp)) if
                 temp[i] not in connectedReferences and temp[i] in self.valid]
                loaded = []
                [connectedReferences[i] for i in range(0, len(connectedReferences)) if
                 cmds.referenceQuery(connectedReferences[i], isLoaded=True) and connectedReferences[i] not in loaded]
                if len(connectedReferences) > 1:
                    proxy = 1
                    active = ""
                    sactive = ""
                    activeProxy = cmds.listConnections("%s.activeProxy" % proxyManager, plugs=True, type="proxyManager")
                    if activeProxy:
                        activeReference = cmds.listConnections(activeProxy, type="reference")
                        if activeReference:
                            active = activeReference[-1]
                    for i in range(0, len(connectedReferences)):
                        if cmds.referenceQuery(connectedReferences[i], isLoaded=True):
                            sactive = connectedReferences[i]
                            break
                    if sactive != "":
                        name = sactive
                        if active != sactive:
                            proxy = -2
                        elif len(loaded) > 1:
                            proxy = -2
                    elif active != "":
                        name = active
                    else:
                        proxy = -2
                        name = rfn
                else:
                    name = rfn
                    proxy = -2
            else:
                name = rfn
            unknown = cmds.listConnections(connectedReferences, type="reference")
            if unknown:
                unknown = "|".join(unknown)
                if "UNKNOWN_REF_NODE" in unknown:
                    isUnknown = 1
        else:
            name = reference
            proxy = -1
        return [name, proxy, isUnknown]

    def exportEdits(self):
        references = self.getSelected()
        if references:
            m_directory = "/".join(cmds.fileDialog2(caption="Save edits", dialogStyle=1, fm=3)[0].split("\\")) + "/"
            for i in range(0, len(references)):
                if cmds.objExists(references[i]):
                    filename = (references[i].split("/")[-1]).split(".")[0]
                    filename = filename.split(" ")[-1].split(":")[-1]
                    path = os.path.join(m_directory, filename)
                    cmds.exportEdits(path + ".ma", includeNetwork=True, includeAnimation=True, includeShaders=True,
                                     includeSetAttrs=True, onReferenceNode=references[i], type="editMA")
                else:
                    print "Failed to find reference associated node."

    def toogleLoadState(self):
        items = self.getSelectedItems()
        for i in range(0, len(items)):
            rfn = self.getCurrentReferenceNode(items[i])
            if rfn:
                isLoaded = cmds.referenceQuery(rfn, isLoaded=True)
                if isLoaded is True:
                    self.unload(items=items[i])
                else:
                    self.reload(items=items[i])
            else:
                print "Failed to find reference node."

    def reload(self, items=None):
        if items:
            items = type(items) is list and items or [items]
        else:
            items = self.getSelectedItems()
        for i in range(0, len(items)):
            node = self.getCurrentReferenceNode(items[i])
            if node:
                cmds.file(loadReference=node)
            self.updateItem(items[i])

    def reloadFull(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            node = self.getCurrentReferenceNode(selected[i])
            if node:
                cmds.file(loadReference=node, loadReferenceDepth="all")
                self.updateItem(selected[i])

    def reloadTopOnly(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            node = self.getCurrentReferenceNode(selected[i])
            if node:
                cmds.file(loadReference=node, loadReferenceDepth="topOnly")
                self.updateItem(selected[i])

    def reloadNone(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            node = self.getCurrentReferenceNode(selected[i])
            if node:
                cmds.file(loadReference=node, loadReferenceDepth="none")
                self.updateItem(selected[i])

    def reloadOriginal(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            node = self.getCurrentReferenceNode(selected[i])
            if node:
                ml_reference.loadContainer(node, 0)
                self.updateItem(selected[i])

    def reloadProxy(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            node = self.getCurrentReferenceNode(selected[i])
            if node:
                ml_reference.loadContainer(node, 1)
                self.updateItem(selected[i])

    def getCurrentReferenceNode(self, item):
        result = None
        path = str(item.data(QtCore.Qt.UserRole + 5))
        unresolve = path.split("{")[0]
        if os.path.isfile(unresolve):
            rfn = cmds.file(path, query=True, rfn=True)
            if rfn and cmds.objExists(rfn):
                result = rfn
        return result

    def unload(self, items=None):
        if items:
            items = type(items) is list and items or [items]
        else:
            items = self.getSelectedItems()
        for i in range(0, len(items)):
            node = str(items[i].data(QtCore.Qt.DisplayRole))
            if cmds.objExists(node):
                proxyManager = cmds.listConnections(node, type="proxyManager")
                if proxyManager:
                    references = cmds.listConnections(proxyManager, type="reference")
                    for r in range(0, len(references)):
                        try:
                            if cmds.referenceQuery(references[r], isLoaded=True):
                                cmds.file(unloadReference=references[r])
                        except:
                            print "failed to unload", references[r]
                else:
                    try:
                        if cmds.referenceQuery(node, isLoaded=True):
                            cmds.file(unloadReference=node)
                    except:
                        print "failed to unload", node
            self.updateItem(items[i])
            self.updateEditor()

    def removeReference(self):
        references = cmds.file(query=True, reference=True)
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            if path in references:
                cmds.file(path, removeReference=True)
                self.removeItem(selected[i])
            self.updateEditor()

    def openReferenceInNewMaya(self):
        result = []
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            if path not in result:
                result.append(path)
                namespace = cmds.referenceQuery(path, rfn=True)
                m_dialogLoop = confirmLoop()
                m_dialogLoop.load(label=namespace, text="Open this reference in new maya?")
                boolean = m_dialogLoop.exec_()
                if boolean:
                    if boolean == 1:
                        ml_reference.openReference(namespace)
                    elif boolean == 2:
                        continue
                    else:
                        break
        return result

    def addDefaultProxy(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            rfn = cmds.referenceQuery(path, rfn=True)
            if rfn:
                m_filename = path.split("{")[0]
                m_proxy_filename = ml_reference.findReference(path=m_filename, expression="proxy|_proxy", force=True)
                m_relatives = ml_reference.referenceRelatives(path, parents=True)
                if m_proxy_filename and m_relatives and len(m_relatives) < 2:
                    ml_reference.addReference(rfn, m_proxy_filename)
                else:
                    print "%s has parent reference." % path
                    break
                self.updateEditor()

    def addProxy(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            rfn = cmds.referenceQuery(path, rfn=True)
            filename = path.split("{")[0]
            if rfn:
                proxy = ml_reference.findReference(path=filename, dialog=True)
                if proxy:
                    ml_reference.addReference(rfn, proxy)
            self.updateItem(selected[i])
            self.updateEditor()

    def switchProxyNext(self):
        result = []
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            reference = str(selected[i].data(QtCore.Qt.DisplayRole))
            if cmds.objExists(reference):
                pm = cmds.listConnections(reference, type="proxyManager")
                connections = []
                if pm:
                    temp = cmds.listConnections(pm, type="reference")
                    [connections.append(temp[t]) for t in range(0, len(temp)) if temp[t] not in connections]
                if connections:
                    ml_reference.switchProxy(reference)
                    result.append(reference)
                    self.updateItem(selected[i])
        self.updateEditor()
        return result

    def switchProxyTo(self, src, dst):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            if cmds.objExists(src):
                ml_reference.switchProxy(src, to=dst)
                self.updateItem(selected[i])
        self.updateEditor()

    def switchToOriginal(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            rfn = cmds.file(path, query=True, rfn=True)
            references = self.listAvalaibleProxy(rfn)
            if references:
                ml_reference.switchProxy(rfn, to=references[0])
                self.updateItem(selected[i])
        self.updateEditor()

    def listAvalaibleProxy(self, rfn):
        references = []
        if cmds.objExists(rfn):
            pm = cmds.listConnections(rfn, type="proxyManager")
            if pm:
                temp = cmds.listConnections(pm, type="reference")
                [references.append(temp[i]) for i in range(0, len(temp)) if temp[i] not in references]
        return references

    def importReference(self):
        selected = self.getSelectedItems()
        m_import = []
        result = []
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            m_dialogLoop = confirmLoop()
            m_dialogLoop.load(label=path, text="Do you want to import this reference in the current scene?")
            m_bool = m_dialogLoop.exec_()
            if m_bool:
                if m_bool == 1:
                    m_relatives = ml_reference.referenceRelatives(path, parents=True)
                    if m_relatives:
                        for r in range(0, len(m_relatives)):
                            m_filename = cmds.referenceQuery(m_relatives[r], filename=True)
                            m_import.insert(0, m_filename)
                elif m_bool == 2:
                    continue
                else:
                    break
        if m_import:
            for i in range(0, len(m_import)):
                if m_import[i] not in result:
                    m_node = cmds.file(m_import[i], query=True, referenceNode=True)
                    pm = cmds.listConnections(m_node, type="proxyManager")
                    m_proxy = []
                    if pm:
                        m_cache = cmds.listConnections("%s.proxyList" % pm[0], type="reference")
                        if m_cache:
                            for p in range(0, len(m_cache)):
                                if m_cache[p] != m_node:
                                    m_name = cmds.referenceQuery(m_cache[p], filename=True)
                                    if m_name and m_name not in m_proxy:
                                        m_proxy.append(m_name)
                    cmds.file(m_import[i], importReference=True)
                    result.append(m_import[i])
                    if m_proxy:
                        for p in range(0, len(m_proxy)):
                            cmds.file(m_proxy[p], removeReference=True)
        self.updateGUI()
        return result

    def cleanUpReferences(self):
        selected = self.mainTree.selectionModel().selectedIndexes()
        for i in range(0, len(selected)):
            node = str(selected[i].data(QtCore.Qt.DisplayRole))
            if cmds.objExists(node):
                ml_reference.cleanupReference(node)

    def saveScenePreset(self):
        filename = cmds.file(query=True, sceneName=True)
        rpe = ReferencePresetEditor()
        rpe.filename = filename
        rpe.savegui()
        rpe.show()

    def saveReferencePreset(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            name = str(selected[i].data(QtCore.Qt.DisplayRole))
            rpe = ReferencePresetEditor()
            rpe.filename = path
            rpe.rfn = name
            rpe.savegui()
            rpe.show()

    def loadPresetForScene(self):
        filename = cmds.file(query=True, sceneName=True)
        rpe = ReferencePresetEditor()
        rpe.filename = filename
        rpe.loadgui()
        rpe.show()

    def loadPresetForCurrentReference(self):
        selected = self.getSelectedItems()
        for i in range(0, len(selected)):
            path = str(selected[i].data(QtCore.Qt.UserRole + 5))
            name = str(selected[i].data(QtCore.Qt.DisplayRole))
            rpe = ReferencePresetEditor()
            rpe.filename = path
            rpe.rfn = name
            rpe.loadgui()
            rpe.show()


class ReferencePresetEditor(QtGui.QDialog):
    def __init__(self, parent=getMayaWindow()):
        super(ReferencePresetEditor, self).__init__(parent)
        self.mainlayout = QtGui.QVBoxLayout()
        self.mainlayout.setSpacing(0)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainlayout)
        self.OSTYPE = sys.platform != "win32" and "/Server-3d/Project" or "//Server-3d/Project"
        self.filename = None
        self.rfn = None

    def loadgui(self):
        self.mainMenuBar = QtGui.QMenuBar(self)
        self.mainlayout.addWidget(self.mainMenuBar)
        self.fileMenu = QtGui.QMenu("File")
        self.fileMenu.setTearOffEnabled(True)
        self.mainMenuBar.addMenu(self.fileMenu)
        self.loadPresetFromFileAction = QtGui.QAction("Load from file", self)
        self.loadPresetFromFileAction.triggered.connect(self.loadFromFile)
        self.fileMenu.addAction(self.loadPresetFromFileAction)
        self.removePresetAction = QtGui.QAction("Remove preset", self)
        self.removePresetAction.triggered.connect(self.removePresetFromGui)
        self.fileMenu.addAction(self.removePresetAction)
        self.editMenu = QtGui.QMenu("Edit")
        self.editMenu.setTearOffEnabled(True)
        self.mainMenuBar.addMenu(self.editMenu)
        self.unloadAction = QtGui.QAction("Unload", self)
        self.unloadAction.triggered.connect(self.setUnloaded)
        self.editMenu.addAction(self.unloadAction)
        self.loadAction = QtGui.QAction("Load", self)
        self.loadAction.triggered.connect(self.setLoaded)
        self.editMenu.addAction(self.loadAction)
        self.proxyMenu = QtGui.QMenu("Proxy", self)
        self.editMenu.addMenu(self.proxyMenu)
        self.viewMenu = QtGui.QMenu("View")
        self.viewMenu.setTearOffEnabled(True)
        self.mainMenuBar.addMenu(self.viewMenu)
        self.expandAllAction = QtGui.QAction("Expand all", self)
        self.expandAllAction.triggered.connect(self.expandTree)
        self.viewMenu.addAction(self.expandAllAction)
        self.setPresetWidget = QtGui.QWidget()
        self.setPresetLayout = QtGui.QGridLayout()
        self.setPresetWidget.setLayout(self.setPresetLayout)
        self.mainlayout.addWidget(self.setPresetWidget)
        self.presetSwitcher = QtGui.QComboBox()
        self.presetSwitcher.activated.connect(self.updateGUI)
        self.presetsComboBoxList = QtCore.QStringList()
        presets = self.listPresets(filename=self.filename)
        for i in range(0, len(presets)):
            self.presetsComboBoxList.append(presets[i])
        self.presetSwitcher.addItems(self.presetsComboBoxList)
        self.setPresetLayout.addWidget(self.presetSwitcher, 0, 1)
        self.applyPresetButton = QtGui.QPushButton("Load")
        self.applyPresetButton.setMaximumWidth(45)
        self.applyPresetButton.released.connect(self.loadReferenceSet)
        self.setPresetLayout.addWidget(self.applyPresetButton, 0, 2)
        self.mainSplitter = QtGui.QSplitter()
        self.mainSplitter.setOrientation(QtCore.Qt.Vertical)
        self.referenceTreeWidget = QtGui.QWidget()
        self.referenceTreeLayout = QtGui.QVBoxLayout()
        self.referenceTreeLayout.setContentsMargins(0, 0, 0, 0)
        self.referenceTreeWidget.setLayout(self.referenceTreeLayout)
        self.filterWidget = QtGui.QWidget()
        self.filterLayout = QtGui.QHBoxLayout()
        self.filterWidget.setLayout(self.filterLayout)

        self.filterIconOff = QtGui.QIcon()
        self.filterIconOn = QtGui.QIcon()
        self.filterPixmapOff = QtGui.QPixmap(
            cfg.RESURCES_PATCH + "filterOff.png")
        self.filterPixmapOn = QtGui.QPixmap(
            cfg.RESURCES_PATCH + "filterOn.png")
        self.filterIconOn.addPixmap(self.filterPixmapOn)
        self.filterIconOff.addPixmap(self.filterPixmapOff)
        self.resetFilterButton = QtGui.QPushButton("")
        self.resetFilterButton.setIcon(self.filterIconOff)
        self.resetFilterButton.setStyleSheet(
                "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,90,90) }")
        self.resetFilterButton.released.connect(self.resetSortRegexpTree)
        self.filterLayout.addWidget(self.resetFilterButton)
        self.filterReference = QtGui.QLineEdit("")
        self.filterReference.returnPressed.connect(self.sortRegexpTree)
        self.filterLayout.addWidget(self.filterReference)
        self.referenceTreeLayout.addWidget(self.filterWidget)
        self.mainTree = QtGui.QTreeView()
        # self.mainTree.setStyleSheet("""
        # QTreeView::branch:has-siblings:!adjoins-item {
        #     border-image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-vline.png) 0;
        # }
        # QTreeView::branch:has-siblings:adjoins-item {
        #    border-image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-branch-more.png) 0;
        # }
        # QTreeView::branch:!has-children:!has-siblings:adjoins-item {
        #    border-image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-branch-end.png) 0;
        # }
        # QTreeView::branch:has-children:!has-siblings:closed,
        # QTreeView::branch:closed:has-children:has-siblings {
        #    border-image: none;
        #    image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-branch-closed.png);
        # }
        # QTreeView::branch:open:has-children:!has-siblings,
        # QTreeView::branch:open:has-children:has-siblings  {
        #    border-image: none;
        #    image: url(""" + self.OSTYPE + """Users/MikhailKorovkin/Documents/maya/2016/scripts/maya_scripts_rfm4/SSM/resources/stylesheet-branch-open.png);
        # }""")
        self.delegate = itemDelegate()
        self.mainTree.setItemDelegate(self.delegate)
        self.mainTree.doubleClicked.connect(self.toogleLoadState)
        self.mainTree.setAlternatingRowColors(True)
        self.mainTree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.mainTree.setSelectionMode(QtGui.QTreeView.ExtendedSelection)
        self.mainTree.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.mainTree.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.mainTree.setSelectionBehavior(QtGui.QTreeView.SelectRows)
        self.mainTree.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mainTree.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.baseModel = QtGui.QStandardItemModel()
        self.proxyModel = customProxyFilter()  # QtGui.QSortFilterProxyModel()
        self.proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxyModel.setSourceModel(self.baseModel)
        self.mainTree.setModel(self.proxyModel)
        self.mainTree.setHeaderHidden(True)
        self.referenceTreeLayout.addWidget(self.mainTree)
        self.mainSplitter.addWidget(self.referenceTreeWidget)
        self.mainlayout.addWidget(self.mainSplitter)
        self.mainTree.selectionModel().selectionChanged.connect(self.updateEditor)
        self.updateGUI()
        self.updateEditor()
        self.setWindowTitle("Reference preload editor --- %s" % self.rfn)

    def savegui(self):
        self.setPresetWidget = QtGui.QWidget()
        self.setPresetLayout = QtGui.QGridLayout()
        self.setPresetWidget.setLayout(self.setPresetLayout)
        self.mainlayout.addWidget(self.setPresetWidget)
        self.presetName = QtGui.QLineEdit("")
        self.setPresetLayout.addWidget(self.presetName, 0, 0)
        self.savePreset = QtGui.QPushButton("Save")
        self.setPresetLayout.addWidget(self.savePreset, 0, 1)
        self.savePreset.released.connect(self.saveFromGui)
        self.setWindowTitle(self.filename)

    def saveFromGui(self):
        name = self.presetName.text()
        if name != "":
            names = self.listPresets(self.filename)
            if name not in names:
                self.save(name, filename=self.filename)
            else:
                print "Preset is already exists, please specify  another name."
        else:
            print "Please specify preset name."
        self.close()

    def updateValidReferences(self):
        self.valid = ml_reference.listReferences(referenceNodes=True)

    def buildData(self, references=None, namespace=None):
        result = []
        checked = []
        if not namespace:
            if self.rfn != "":
                if cmds.objExists(self.rfn):
                    parent = self.rfn
                    filename = cmds.referenceQuery(self.rfn, filename=True)
                    namespace = cmds.file(filename, query=True, renamingPrefix=True)
                else:
                    parent = cmds.file(self.rfn, query=True, rfn=True)
                    filename = self.rfn
                    namespace = cmds.file(self.rfn, query=True, renamingPrefix=True)
                namespace = ":".join(parent.split(":")[:-1]) + ":" + namespace + ":"
                if not references:
                    references = cmds.file(filename, query=True, reference=True)
                    print references
            else:
                namespace = None
        if references and not references:
            references = type(references) is list and references or [references]
        if not references:
            references = cmds.file(query=True, reference=True)
        for i in range(0, len(references)):
            rfn = cmds.file(references[i], query=True, rfn=True)
            if rfn and cmds.objExists(rfn):
                data = {}
                pm = cmds.listConnections(rfn, type="proxyManager")
                active = ""
                proxy = [rfn]
                if pm:
                    active = cmds.listConnections("%s.activeProxy" % pm[-1], type="proxyManager", plugs=True)
                    temp = cmds.listConnections(pm, type="reference")
                    for p in range(0, len(temp)):
                        if temp[p] not in proxy:
                            proxy.append(temp[p])
                proxyLenght = len(proxy)
                for p in range(0, proxyLenght):
                    if proxy[p] in self.valid:
                        path = cmds.referenceQuery(proxy[p], filename=True)
                        if path not in checked:
                            checked.append(path)
                            connections = cmds.listConnections(proxy[p], type="proxyManager", plugs=True)
                            if connections:
                                connections = connections[-1]
                            else:
                                connections = ""
                            if proxyLenght > 1:
                                isActive = False
                            else:
                                isActive = True
                            loaded = False
                            if cmds.referenceQuery(proxy[p], isLoaded=True):
                                loaded = True
                                isActive = True
                            if connections in active:
                                isActive = True
                            nested = cmds.file(path, query=True, reference=True)
                            if nested:
                                childs = self.buildData(nested, namespace=namespace)
                            else:
                                childs = []
                            loaded = loaded is True and 1 or 0
                            isActive = isActive is True and 1 or 0
                            if proxyLenght < 2 and pm:
                                isProxy = -2
                            elif proxyLenght > 1 and pm:
                                isProxy = 1
                            else:
                                isProxy = 0
                            if namespace != "":
                                cache = proxy[p].split(namespace)
                                cache = [cache[c] for c in range(0, len(cache)) if cache[c] and cache[c] != ""]
                                resolved = ":".join(cache)
                            else:
                                resolved = proxy[p]
                            data.update(
                                    {resolved: {"load": loaded, "active": isActive, "proxy": isProxy, "ref": childs}})
                result.append(data)
        return result

    def getRootPath(self, filename=""):
        path = ""
        if filename == "":
            filename = cmds.file(query=True, sceneName=True)
        if filename != "":
            name = filename.split("/")[-1]
            cname = "".join(re.split("_v[0-9]+", name))
            directory = name.join(filename.split(name)[:-1])
            path = os.path.join(directory, cname.split(".")[0] + ".js")
            buffer_dir = directory.split("/")
            if re.findall("(/|)[Ww][Oo][Rr][Kk](/|)", buffer_dir[-2]):
                path = os.path.join("/".join(buffer_dir[:-2]) + "/", cname.split(".")[0] + ".js")
            else:
                path = os.path.join(directory, cname.split(".")[0] + ".js")
            if not os.path.isfile(path):
                m_file = file(path, "w")
                json.dump([], m_file, indent=4, ensure_ascii=False)
                m_file.close()
        else:
            print "\nScene is not saved!!!"
            return None
        return path

    def getSelectedItems(self):
        result = []
        selected = self.mainTree.selectionModel().selectedIndexes()
        for i in range(0, len(selected)):
            item = self.proxyModel.mapToSource(selected[i])
            item = self.baseModel.itemFromIndex(item)
            result.append(item)
        return result

    def getChildItems(self, item, onlyEnabled=False):
        result = []
        for r in range(item.rowCount() - 1, -1, -1):
            child = item.child(r)
            if onlyEnabled is True:
                isEnabled = child.isEnabled()
            else:
                isEnabled = True
            if child not in result and isEnabled:
                result.append(child)
                descendents = self.getChildItems(child, onlyEnabled=onlyEnabled)
                for i in range(0, len(descendents)):
                    result.append(descendents[i])
        return result

    def buildReferenceSet(self, namespace=None):
        result = []
        root = self.baseModel.invisibleRootItem()
        items = self.getChildItems(root, onlyEnabled=True)
        for i in range(0, len(items)):
            node = str(items[i].data(QtCore.Qt.DisplayRole))
            loaded = str(items[i].data(QtCore.Qt.UserRole + 7))
            if loaded == "1":
                resolved = node
                if namespace:
                    resolved = "%s:%s" % (namespace, node)
                result.append(resolved)
        return result

    def loadReferenceSet(self):
        unloadUnused = True
        result = []
        if self.rfn != "":
            if cmds.objExists(self.rfn):
                parent = self.rfn
                filename = cmds.referenceQuery(self.rfn, filename=True)
                namespace = cmds.file(filename, query=True, renamingPrefix=True)
            else:
                parent = cmds.file(self.rfn, query=True, rfn=True)
                filename = self.rfn
                namespace = cmds.file(self.rfn, query=True, renamingPrefix=True)
            namespace = ":".join(parent.split(":")[:-1]) + ":" + namespace
        else:
            parent = ""
            namespace = ""
        referenceSet = self.buildReferenceSet(namespace=namespace)
        if parent != "":
            references = self.listValidReferences(references=filename, onlyLoaded=True, source=filename)
        else:
            references = self.listValidReferences()
        for i in range(0, len(references)):
            if unloadUnused is True and cmds.objExists(references[i]) and references[i] not in referenceSet:
                ml_reference.unloadReference(references[i])
        for i in range(0, len(referenceSet)):
            if cmds.objExists(referenceSet[i]) and cmds.nodeType(referenceSet[i]) == "reference":
                if cmds.referenceQuery(referenceSet[i], isLoaded=True) is False:
                    if referenceSet[i] not in result:
                        result.append(referenceSet[i])
                        ml_reference.loadReference(referenceSet[i], loadReferenceDepth="topOnly")
        return result

    def listValidReferences(self, references=[], onlyLoaded=False, source=[]):
        result = []
        if source:
            source = type(source) is list and source or [source]
        if not references:
            references = cmds.file(query=True, reference=True)
        else:
            references = type(references) is list and references or [references]
        for i in range(0, len(references)):
            if references[i] not in result:
                rfn = cmds.file(references[i], query=True, rfn=True)
                if rfn:
                    if onlyLoaded is False and True or onlyLoaded is True and cmds.referenceQuery(rfn, isLoaded=True):
                        if references[i] not in source:
                            result.append(rfn)
                        childs = cmds.file(references[i], query=True, reference=True)
                        for c in range(0, len(childs)):
                            nested = self.listValidReferences(references=childs[c], onlyLoaded=onlyLoaded)
                            for n in range(0, len(nested)):
                                if nested[n] not in result:
                                    result.append(nested[n])
        return result

    def getParentItems(self, item):
        result = []
        baseroot = self.baseModel.invisibleRootItem()
        proxyroot = self.baseModel.indexFromItem(baseroot)
        proxyroot = self.proxyModel.mapFromSource(proxyroot)
        parent = item.parent()
        while parent:
            result.append(parent)
            parent = parent.parent()
            if parent == baseroot or parent == proxyroot:
                break
        return result

    def expandTree(self):
        self.mainTree.expandAll()

    def save(self, name, filename=""):
        if name and str(name) != "":
            name = str(name)
        path = self.getRootPath(filename=filename)
        m_file = open(path).read()
        data = json.loads(m_file)
        presets = [data[i]["name"] for i in range(0, len(data)) if data[i]["type"] == "referencePreset"]
        if name in presets:
            print "Preset name already exists. Please specify another name."
            return None
        scenename = cmds.file(query=True, sceneName=True)
        if scenename in filename:
            reference = []
        else:
            reference = cmds.file(filename, query=True, reference=True)
        self.updateValidReferences()
        preset = {
            "type": "referencePreset",
            "name": name,
            "preset": self.buildData(reference)
        }
        data.append(preset)
        m_file = file(path, "w")
        json.dump(data, m_file, indent=0, ensure_ascii=False)
        m_file.close()
        print "Preset \"%s\" saved to %s" % (name, path)

    def load(self, name, filename=""):
        if name:
            path = self.getRootPath(filename=filename)
            filename = open(path).read()
            data = json.loads(filename)
            for i in range(0, len(data)):
                if data[i]["type"] == "referencePreset":
                    if data[i]["name"] == name:
                        self.preset = data[i]["preset"]
                        self.buildTree(data=self.preset)
                        break

    def buildTree(self, parent=None, data=None, level=None):
        if not parent:
            root = self.baseModel.invisibleRootItem()
        else:
            root = parent
        if not level:
            level = data
        for i in range(0, len(level)):
            proxy = level[i].keys()
            proxyLenght = len(proxy)
            activeFounded = False
            for p in range(0, proxyLenght):
                rfn = level[i][proxy[p]]
                proxyList = "|".join(proxy)
                isLoaded = rfn["load"]
                valid = rfn["proxy"]
                if p == proxyLenght - 1 and activeFounded is False:
                    isActive = 1
                else:
                    isActive = rfn["active"]
                content = rfn["ref"]
                if isActive == 1:
                    activeFounded = True
                    item = QtGui.QStandardItem(proxy[p])
                    item.setData(proxy[p], QtCore.Qt.DisplayRole)
                    item.setData(proxy[p].split(":")[-1], QtCore.Qt.DisplayRole + 1)
                    item.setData(isLoaded, QtCore.Qt.UserRole + 7)
                    item.setData(valid, QtCore.Qt.UserRole + 4)
                    item.setData(proxy[p], QtCore.Qt.UserRole + 9)
                    item.setData(proxyList, QtCore.Qt.UserRole + 10)
                    item.setData(valid, QtCore.Qt.UserRole + 11)
                    root.setChild(root.rowCount(), item)
                    if isLoaded == 1 and content:
                        self.buildTree(parent=item, data=data, level=content)

    def listPresets(self, filename=""):
        result = []
        path = self.getRootPath(filename=filename)
        filename = open(path).read()
        data = json.loads(filename)
        for i in range(0, len(data)):
            keys = data[i].keys()
            if "type" in keys:
                if data[i]["type"] == "referencePreset":
                    name = data[i]["name"]
                    result.append(name)
        return result

    def resetSortRegexpTree(self):
        self.proxyModel.setFilterRegExp("")
        self.resetFilterButton.setIcon(self.filterIconOff)
        # self.resetFilterButton.setStyleSheet( "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,90,90) }" )

    def sortRegexpTree(self):
        expr = self.filterReference.text()
        self.proxyModel.setFilterRegExp(expr)
        if expr != "":
            self.resetFilterButton.setIcon(self.filterIconOn)
            # self.resetFilterButton.setStyleSheet( "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,180,90) }" )
        else:
            self.resetFilterButton.setIcon(self.filterIconOff)
            # self.resetFilterButton.setStyleSheet( "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,90,90) }" )

    def loadFromFile(self):
        directory = "/".join(self.filename.split("/")[:-1])
        filename = cmds.fileDialog2(caption="Reference", fileFilter="Java script (*.js)", startingDirectory=directory,
                                    fileMode=1)
        if filename:
            self.filename = filename[-1]
            self.baseModel.clear()
            self.presetSwitcher.clear()
            self.presetSwitcher.clear()
            self.presetsComboBoxList = QtCore.QStringList()
            presets = self.listPresets(filename=self.filename)
            for i in range(0, len(presets)):
                self.presetsComboBoxList.append(presets[i])
            self.presetSwitcher.addItems(self.presetsComboBoxList)
            self.updateGUI()

    def updateGUI(self):
        self.baseModel.clear()
        name = self.presetSwitcher.currentText()
        self.load(name=name, filename=self.filename)

    def updateEditor(self):
        items = self.getSelectedItems()
        actions = self.proxyMenu.actions()
        self.proxyMenu.setEnabled(False)
        if actions:
            for i in range(0, len(actions)):
                self.proxyMenu.removeAction(actions[i])
        if items:
            if len(items) == 1:
                proxyList = str(items[0].data(QtCore.Qt.UserRole + 10))
                proxyList = proxyList.split("|")
                if len(proxyList) > 1:
                    name = str(items[0].data(QtCore.Qt.DisplayRole))
                    self.proxyMenu.setEnabled(True)
                    for i in range(0, len(proxyList)):
                        self.makeSwitchProxyAction(name, proxyList[i])

    def setItemChildsEnabled(self, item, boolean):
        childs = self.getChildItems(item)
        for i in range(0, len(childs)):
            childs[i].setEnabled(boolean)
            value = -3
            if boolean is True:
                original = str(childs[i].data(QtCore.Qt.UserRole + 11))
                value = int(original)
            childs[i].setData(value, QtCore.Qt.UserRole + 4)

    def toogleLoadState(self):
        items = self.getSelectedItems()
        for i in range(0, len(items)):
            value = str(items[i].data(QtCore.Qt.UserRole + 7))
            if value == "1":
                self.setUnloaded(items[i])
            else:
                self.setLoaded(items[i])

    def setUnloaded(self, items=None):
        if not items:
            items = self.getSelectedItems()
        else:
            items = type(items) is list and items or [items]
        for i in range(0, len(items)):
            items[i].setData(0, QtCore.Qt.UserRole + 7)
            childs = self.getChildItems(items[i])
            for c in range(0, len(childs)):
                childs[c].setData(0, QtCore.Qt.UserRole + 7)

    def setLoaded(self, items=None):
        if not items:
            items = self.getSelectedItems()
        else:
            items = type(items) is list and items or [items]
        for i in range(0, len(items)):
            items[i].setData(1, QtCore.Qt.UserRole + 7)
            parents = self.getParentItems(items[i])
            for p in range(0, len(parents)):
                parents[p].setData(1, QtCore.Qt.UserRole + 7)

    def makeSwitchProxyAction(self, src, dst):
        rfnAction = QtGui.QAction(dst, self)
        if src != dst:
            rfnAction.triggered.connect(lambda: self.switchProxy(dst))
        else:
            rfnAction.setEnabled(False)
        self.proxyMenu.addAction(rfnAction)

    def switchProxy(self, proxy):
        items = self.getSelectedItems()
        for i in range(0, len(items)):
            original = str(items[i].data(QtCore.Qt.UserRole + 9))
            if proxy != original:
                proxyList = str(items[i].data(QtCore.Qt.UserRole + 10))
                proxyList = proxyList.split("|")
                if proxy in proxyList:
                    items[i].setData(proxy, QtCore.Qt.DisplayRole)
                    self.setItemChildsEnabled(items[i], False)
            else:
                items[i].setData(proxy, QtCore.Qt.DisplayRole)
                self.setItemChildsEnabled(items[i], True)
        self.updateEditor()

    def removePresetFromGui(self):
        name = self.presetSwitcher.currentText()
        pindex = self.presetSwitcher.currentIndex()
        self.removePreset(name)
        self.presetSwitcher.removeItem(pindex)
        self.updateGUI()

    def removePreset(self, name):
        path = self.getRootPath(filename=self.filename)
        filejs = open(path).read()
        data = json.loads(filejs)
        for i in range(0, len(data)):
            if data[i]["type"] == "referencePreset":
                if data[i]["name"] == name:
                    data.pop(i)
                    break
        filejs = file(path, "w")
        json.dump(data, filejs, indent=0, ensure_ascii=False)
        filejs.close()
        print "Preset \"%s\" removed from %s" % (name, path)

    def overwritePreset(self, name):
        filename = cmds.file(query=True, sceneName=True)
        if name != "":
            names = self.listPresets(filename)
            if name in names:
                self.removePreset(name)
            self.save(name, filename=filename)
        else:
            print "Please specify preset name."


class ReferenceEditsEditor(QtGui.QDialog):
    def __init__(self, parent=getMayaWindow()):
        super(ReferenceEditsEditor, self).__init__(parent)
        self.m_referenceNodes = []
        self.mainlayout = QtGui.QVBoxLayout()
        self.mainlayout.setSpacing(0)
        self.mainlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainlayout)
        self.m_splitter = QtGui.QSplitter()
        self.mainlayout.addWidget(self.m_splitter)
        self.m_editsListGroupBox = QtGui.QGroupBox("Edits")
        self.m_editsListLayout = QtGui.QVBoxLayout()
        self.m_editsListLayout.setContentsMargins(0, 0, 0, 0)
        self.m_editsListGroupBox.setLayout(self.m_editsListLayout)
        self.m_splitter.addWidget(self.m_editsListGroupBox)
        self.m_filterWidget = QtGui.QWidget()
        self.m_filterLayout = QtGui.QHBoxLayout()
        self.m_filterWidget.setLayout(self.m_filterLayout)
        self.m_editsListLayout.addWidget(self.m_filterWidget)
        self.filterIconOff = QtGui.QIcon()
        self.filterIconOn = QtGui.QIcon()
        self.filterPixmapOff = QtGui.QPixmap(
            cfg.RESURCES_PATCH + "filterOff.png")
        self.filterPixmapOn = QtGui.QPixmap(
            cfg.RESURCES_PATCH + "filterOn.png")
        self.filterIconOn.addPixmap(self.filterPixmapOn)
        self.filterIconOff.addPixmap(self.filterPixmapOff)
        self.resetFilterButton = QtGui.QPushButton("")
        self.resetFilterButton.setIcon(self.filterIconOff)
        self.resetFilterButton.setStyleSheet(
                "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,90,90) }")
        self.resetFilterButton.released.connect(self.resetSortRegexpTree)
        self.m_filterLayout.addWidget(self.resetFilterButton)
        self.m_findEditsTextField = QtGui.QLineEdit("")
        self.m_findEditsTextField.returnPressed.connect(self.sortRegexpTree)
        self.m_findEditsTextField.setToolTip("Regular expression field.")
        self.m_filterLayout.addWidget(self.m_findEditsTextField)
        self.m_selectionListTree = QtGui.QTreeView()
        self.delegate = listDelegate()
        self.m_selectionListTree.setItemDelegate(self.delegate)
        self.m_selectionListTree.setAlternatingRowColors(True)
        self.m_selectionListTree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.m_selectionListTree.setIndentation(0)
        self.m_selectionListTree.setSelectionMode(QtGui.QTreeView.ExtendedSelection)
        self.m_selectionListTree.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.m_selectionListTree.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.m_selectionListTree.setMinimumWidth(400)
        self.m_selectionListTree.setSelectionBehavior(QtGui.QTreeView.SelectRows)
        self.m_selectionListTree.setFocusPolicy(QtCore.Qt.NoFocus)
        self.m_selectionListTree.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.m_selectionListModelProxy = QtGui.QSortFilterProxyModel()
        self.m_selectionListModel = QtGui.QStandardItemModel()
        self.m_selectionListModelProxy.setSourceModel(self.m_selectionListModel)
        self.m_selectionListModelProxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.m_selectionListTree.setModel(self.m_selectionListModelProxy)
        self.m_selectionListTree.setHeaderHidden(True)
        self.m_editsListLayout.addWidget(self.m_selectionListTree)
        self.setWindowTitle("Reference edits editor")

    def setReferences(self, referenceNodes):
        self.m_referenceNodes = referenceNodes
        self.removeAllContent()
        for i in range(0, len(self.m_referenceNodes)):
            if cmds.objExists(self.m_referenceNodes[i]) and cmds.nodeType(
                    self.m_referenceNodes[i]) == "reference" or cmds.referenceQuery(self.m_referenceNodes[i],
                                                                                    isNodeReferenced=True):
                self.addContent(self.m_referenceNodes[i])

    def addContent(self, reference):
        m_list = self.m_selectionListModel.invisibleRootItem()
        m_edits = ml_reference.listReferenceEdits(reference)
        scenename = cmds.file(query=True, sceneName=True)
        scenename = scenename != "" and scenename or "untitled"
        m_referenceFile = cmds.referenceQuery(reference, filename=True)
        for i in range(0, len(m_edits)):
            # [ m_reference, m_content[c], m_levels[l][-1], m_levels[l][0], m_edits[e].split( " " )[0], m_edits[e] ]
            editOptions = self.editsShowOptions(m_edits[i], scene=scenename)
            m_item = QtGui.QStandardItem(m_edits[i][-1])
            m_item.setData("", QtCore.Qt.UserRole + 1)
            m_item.setData(m_edits[i][4], QtCore.Qt.UserRole + 2)
            m_item.setData(m_edits[i][1].split("|")[-1], QtCore.Qt.UserRole + 3)
            m_item.setData("", QtCore.Qt.UserRole + 4)
            m_item.setData(m_edits[i][2], QtCore.Qt.UserRole + 5)
            m_item.setData(m_edits[i][1], QtCore.Qt.UserRole + 6)
            m_item.setData(m_edits[i][0], QtCore.Qt.UserRole + 7)
            m_item.setData(m_referenceFile, QtCore.Qt.UserRole + 8)
            m_item.setData(m_edits[i][-1], QtCore.Qt.UserRole + 9)
            m_item.setData(editOptions, QtCore.Qt.UserRole + 10)
            if editOptions[0] == "R" or editOptions[0] == "Z":
                m_item.setEnabled(False)
            m_list.appendRow(m_item)

    def editsShowOptions(self, edit, scene=""):
        result = ""
        filename = edit[2]
        string = edit[5]
        if filename == scene:
            result += "C "
        elif filename == "unknown":
            result += "U "
        elif filename == "":
            result += "Z "
        else:
            result += "R "
        if ".translate" in string or ".scale" in string or ".rotate" in string or "parent" in string:
            result += "T 0"
        else:
            result += "N "
            if ".inMesh" in string or ".worldMesh" in string or ".intermediaObject" in string or "Deformed" in string:
                result += "1"
            else:
                result += "0"
        return result

    def getSelected(self):
        m_result = []
        m_indexes = self.m_selectionListTree.selectionModel().selectedIndexes()
        for i in range(0, len(m_indexes)):
            m_temp = m_indexes[i].data()
            m_temp = str(m_temp)
            if m_temp not in m_result:
                m_result.append(m_temp)
        return m_result

    def refresh(self):
        if self.m_referenceNodes:
            self.setReferences(self.m_referenceNodes)

    def removeEdits(self):
        m_indexes = self.m_selectionListTree.selectionModel().selectedIndexes()
        m_strings = {}
        for i in range(0, len(m_indexes)):
            m_keys = m_strings.keys()
            m_string = m_indexes[i].data(QtCore.Qt.UserRole + 9)
            rfn = m_indexes[i].data(QtCore.Qt.UserRole + 7)
            if rfn not in m_keys:
                m_strings.update({rfn: [m_string]})
            else:
                m_array = m_strings[rfn]
                m_array.append(m_string)
                m_strings.update({rfn: m_array})
        m_keys = m_strings.keys()
        for i in range(0, len(m_keys)):
            m_array = m_strings[m_keys[i]]
            print "\nreference: %s\nremove: %s" % (m_keys[i], m_array)
            ml_reference.removeEdits(m_keys[i], m_array)
        if self.m_referenceNodes:
            self.setReferences(self.m_referenceNodes)

    def removeContent(self):
        m_selected = self.m_selectionListTree.selectionModel().selectedIndexes()
        for i in range(len(m_selected) - 1, -1, -1):
            self.m_selectionListModel.removeRow(m_selected[i].row())

    def resetSortRegexpTree(self):
        self.m_selectionListModelProxy.setFilterRegExp("")
        self.resetFilterButton.setIcon(self.filterIconOff)
        # self.resetFilterButton.setStyleSheet( "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,90,90) }" )

    def sortRegexpTree(self):
        expr = self.m_findEditsTextField.text()
        self.m_selectionListModelProxy.setFilterRegExp(expr)
        if expr != "":
            self.resetFilterButton.setIcon(self.filterIconOn)
            # self.resetFilterButton.setStyleSheet( "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,180,90) }" )
        else:
            self.resetFilterButton.setIcon(self.filterIconOff)
            # self.resetFilterButton.setStyleSheet( "QPushButton {border: none;font-size: 16px;font: bold;color: rgb(90,90,90) }" )

    def removeAllContent(self):
        self.m_selectionListModel.removeRows(0, self.m_selectionListModel.rowCount())


class customProxyFilter(QtGui.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(customProxyFilter, self).__init__(parent)
        self.__showAllChildren = False

    def showAllChildren(self):
        return self.__showAllChildren;

    def setShowAllChildren(self, showAllChildren):
        if showAllChildren == self.__showAllChildren:
            return
        self.__showAllChildren = showAllChildren
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if self.filterRegExp() == "":
            return True
        if super(customProxyFilter, self).filterAcceptsRow(source_row, source_parent):
            return True
        source_index = self.sourceModel().index(source_row, 0, source_parent)
        for i in range(self.sourceModel().rowCount(source_index)):
            if self.filterAcceptsRow(i, source_index):
                return True
        return False


class confirmLoop(QtGui.QDialog):
    def __init__(self, parent=None):
        super(confirmLoop, self).__init__(parent)

    def load(self, label="", text=""):
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setContentsMargins(2, 2, 2, 2)
        self.setWindowTitle(label)
        self.label = QtGui.QLabel(text)
        self.HLayout = QtGui.QHBoxLayout()
        self.executeButton = QtGui.QPushButton("Yes")
        self.executeButton.released.connect(self.executeSlot)
        self.continueButton = QtGui.QPushButton("No")
        self.continueButton.released.connect(self.continueSlot)
        self.breakButton = QtGui.QPushButton("Cancel")
        self.breakButton.released.connect(self.breakSlot)
        self.HLayout.addWidget(self.executeButton)
        self.HLayout.addWidget(self.continueButton)
        self.HLayout.addWidget(self.breakButton)
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addLayout(self.HLayout)
        self.setLayout(self.mainLayout)

    def executeSlot(self):
        self.done(1)

    def continueSlot(self):
        self.done(2)

    def breakSlot(self):
        self.done(3)


class itemDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QtGui.QSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, spinBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        return QtCore.QSize(100, 20)

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        gradient = QtGui.QLinearGradient(option.rect.x() + option.rect.width() / 2, option.rect.y(),
                                         option.rect.x() + option.rect.width() / 2,
                                         option.rect.y() + option.rect.height())
        col = QtGui.QColor(index.model().data(index, QtCore.Qt.BackgroundColorRole))
        if col.name() == "#000000":
            col = option.palette.window().color()
        gradient.setColorAt(0.05, option.palette.base().color())
        gradient.setColorAt(0.051, col)
        gradient.setColorAt(0.95, col)
        gradient.setColorAt(0.951, option.palette.base().color())
        brush = QtGui.QBrush(gradient)
        painter.fillRect(option.rect, brush)
        text = index.model().data(index, QtCore.Qt.DisplayRole)
        painter.drawText(option.rect.x() + 25, option.rect.y() + 2, option.rect.width(), option.rect.height(),
                         QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft, text)
        proxy = index.model().data(index, QtCore.Qt.UserRole + 4)
        loaded = index.model().data(index, QtCore.Qt.UserRole + 7)
        if proxy == 1:
            pixmap = QtGui.QPixmap(
                cfg.RESURCES_PATCH + "referenceProxy.png")
        elif proxy == 0:
            pixmap = QtGui.QPixmap(
                cfg.RESURCES_PATCH + "reference.png")
        elif proxy == -1:
            pixmap = QtGui.QPixmap(
                cfg.RESURCES_PATCH + "reference_damaged.png")
        elif proxy == -2:
            pixmap = QtGui.QPixmap(
                cfg.RESURCES_PATCH + "referenceProxy_damaged.png")
        elif proxy == -3:
            pixmap = QtGui.QPixmap(
                cfg.RESURCES_PATCH + "reference_disabled.png")
        else:
            pixmap = QtGui.QPixmap(
                cfg.RESURCES_PATCH + "reference_damaged.png")
        painter.drawPixmap(option.rect.x() + option.rect.width() - 1.1 * option.rect.height(),
                           option.rect.y() - 0.1 * option.rect.height(), option.rect.height(), option.rect.height(),
                           pixmap)
        unknown = index.model().data(index, QtCore.Qt.UserRole + 3)
        rect = QtCore.QRect(option.rect.x() + 0.14 * option.rect.height(),
                            option.rect.y() + 0.14 * option.rect.height(), 0.65 * option.rect.height(),
                            0.65 * option.rect.height())

        if loaded == 1:
            self.drawCheck(painter, option, rect, QtCore.Qt.CheckState(QtCore.Qt.Checked))
        else:
            self.drawCheck(painter, option, rect, QtCore.Qt.CheckState(QtCore.Qt.Unchecked))
        if unknown == 1:
            brush = QtGui.QBrush(QtGui.QColor(215, 0, 15))
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(brush)
            painter.drawEllipse(option.rect.x() + option.rect.width() - 1.1 * option.rect.height(),
                                option.rect.y() + 0.1 * option.rect.height(), option.rect.height() * 0.2,
                                option.rect.height() * 0.2)
        if option.state & QtGui.QStyle.State_Selected:
            colr = QtGui.QBrush(option.palette.highlight())
            ccc = QtGui.QColor(colr.color())
            ccc.setAlphaF(.2)
            colr.setColor(ccc)
            painter.fillRect(option.rect, colr)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        result = False
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            mouse = event
            rect = QtCore.QRect(option.rect.x() + 0.1 * option.rect.height(),
                                option.rect.y() - 0.05 * option.rect.height(), option.rect.height(),
                                option.rect.height())
            if rect.contains(mouse.x(), mouse.y()):
                result = True
                self.emit(QtCore.SIGNAL("itemCheckChange(const QModelIndex &)"), index)
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            mouse = event
            rect = QtCore.QRect(option.rect.x() + 0.205 * option.rect.height(),
                                option.rect.y() + 0.205 * option.rect.height(), 0.5 * option.rect.height(),
                                0.5 * option.rect.height())
            if not rect.contains(mouse.x(), mouse.y()):
                result = True
                self.emit(QtCore.SIGNAL("itemExpanded(const QModelIndex &)"), index)
        return result


class listDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        super(listDelegate, self).__init__(parent)
        self.mult = 1

    def createEditor(self, parent, option, index):
        editor = QtGui.QSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, spinBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)
        spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        myFont = QtGui.QFont("Tahoma")
        myFont.setPixelSize(11)
        myFontMetrics = QtGui.QFontMetrics(myFont)
        mySize = myFontMetrics.boundingRect(0, 0, 260, 0,
                                            (QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft),
                                            index.data(QtCore.Qt.DisplayRole))
        return QtCore.QSize(mySize.width(), mySize.height() + 40)

    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        editOptions = str(index.model().data(index, QtCore.Qt.UserRole + 10))
        editOptions = editOptions.split(" ")
        newMetr = QtGui.QFontMetrics(painter.font())
        heit = newMetr.height() + 2
        gradient = QtGui.QLinearGradient(option.rect.x() + option.rect.width() / 2, option.rect.y(),
                                         option.rect.x() + option.rect.width() / 2,
                                         option.rect.y() + option.rect.height())
        gradient.setColorAt(0.01, option.palette.base().color())
        gradient.setColorAt(0.02, option.palette.window().color())
        gradient.setColorAt(0.98, option.palette.window().color())
        gradient.setColorAt(0.99, option.palette.base().color())
        brush = QtGui.QBrush(gradient)
        painter.fillRect(option.rect, brush)
        if sys.platform == "win32":
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Multiply)
            gradient2 = QtGui.QLinearGradient(option.rect.x(), option.rect.y(), option.rect.width(),
                                              option.rect.height())
            gradient2.setColorAt(0, QtGui.QColor(255, 255, 255))
            gradient2.setColorAt(1, QtGui.QColor(200, 200, 200))
            brush2 = QtGui.QBrush(gradient2)
            painter.fillRect(option.rect, brush2)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Overlay)
            gradient3 = QtGui.QLinearGradient(option.rect.x(), option.rect.y(), option.rect.x() + option.rect.width(),
                                              option.rect.y() + option.rect.height())
            gradient3.setColorAt(1, QtGui.QColor(0, 0, 0, 100))
            gradient3.setColorAt(0, QtGui.QColor(255, 255, 255, 100))
            brush3 = QtGui.QBrush(gradient3)
            painter.fillRect(option.rect.x() + 2, option.rect.y() + 2, option.rect.width() / 2, heit, brush3)
            gradient4 = QtGui.QLinearGradient(option.rect.x(), option.rect.y(), option.rect.x() + option.rect.width(),
                                              option.rect.y() + option.rect.height())
            gradient4.setColorAt(0, QtGui.QColor(0, 0, 0, 100))
            gradient4.setColorAt(1, QtGui.QColor(255, 255, 255, 100))
            brush4 = QtGui.QBrush(gradient4)
            painter.fillRect(option.rect.x() + option.rect.width() / 2, option.rect.y() + option.rect.height() - heit,
                             option.rect.width() / 2, heit, brush4)
        gradient5 = QtGui.QLinearGradient(option.rect.x(), option.rect.y(), option.rect.x() + option.rect.width(),
                                          option.rect.y() + option.rect.height())
        gradient5.setColorAt(1, QtGui.QColor(100, 100, 100, 155))
        gradient5.setColorAt(0, QtGui.QColor(255, 255, 255, 155))
        brush5 = QtGui.QBrush(gradient5)
        painter.fillRect(option.rect.x() + 2, option.rect.y() + heit, option.rect.width(), 1, brush5)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        textNickname = index.data(QtCore.Qt.UserRole + 3)
        painter.drawText(option.rect.x() + 4, option.rect.y() + 2, option.rect.width(), option.rect.height(), (
            QtCore.Qt.TextWrapAnywhere | QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft),
                         textNickname)
        textSize = index.data(QtCore.Qt.UserRole + 5)
        one_widthSize = painter.fontMetrics().width(textSize)
        painter.drawText(option.rect.x() + option.rect.width() - one_widthSize - 2,
                         option.rect.y() + option.rect.height() - heit, option.rect.width(), option.rect.height(), (
                             QtCore.Qt.TextWrapAnywhere | QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft),
                         textSize)
        textDateTyme = index.data(QtCore.Qt.UserRole + 2)
        one_width = painter.fontMetrics().width(textDateTyme)
        painter.drawText(option.rect.x() + option.rect.width() - one_width - 2, option.rect.y() + 2,
                         option.rect.width(), option.rect.height(), (
                             QtCore.Qt.TextWrapAnywhere | QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft),
                         textDateTyme)
        textPath = index.data(QtCore.Qt.UserRole + 4)
        textPathElide = painter.fontMetrics().elidedText(textPath, QtCore.Qt.ElideLeft, option.rect.width() - 5)
        one_width = painter.fontMetrics().width(textPathElide)
        painter.drawText(option.rect.x() + option.rect.width() - one_width - 6 - one_widthSize,
                         option.rect.y() + option.rect.height() - heit, option.rect.width(), option.rect.height(), (
                             QtCore.Qt.TextWrapAnywhere | QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft),
                         textPathElide)
        text = index.data(QtCore.Qt.DisplayRole)
        if editOptions[2] == "0":
            painter.setPen(QtCore.Qt.white)
        elif editOptions[2] == "1":
            painter.setPen(QtCore.Qt.red)
        painter.drawText(option.rect.x() + 5, option.rect.y() + heit + 5, option.rect.width(),
                         option.rect.height() - heit,
                         (QtCore.Qt.TextWordWrap | QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft), text)
        if option.state & QtGui.QStyle.State_Selected:
            colr = QtGui.QBrush(option.palette.highlight())
            ccc = QtGui.QColor(colr.color())
            ccc.setAlphaF(.2)
            colr.setColor(ccc)
            painter.fillRect(option.rect, colr)
        if editOptions[0] == "C":
            # Edit applied in current scene
            pass
        elif editOptions[0] == "U":
            # Edit is not applied in any scene
            colr = QtGui.QBrush(QtCore.Qt.yellow)
            ccc = QtGui.QColor(colr.color())
            ccc.setAlphaF(.03)
            colr.setColor(ccc)
            painter.fillRect(option.rect, colr)
            pass
        elif editOptions[0] == "Z":
            # Edit is not applied in any scene
            colr = QtGui.QBrush(option.palette.dark())
            ccc = QtGui.QColor(colr.color())
            ccc.setAlphaF(.5)
            colr.setColor(ccc)
            painter.fillRect(option.rect, colr)
        elif editOptions[0] == "R":
            # Edit applied in reference scene
            colr = QtGui.QBrush(option.palette.dark())
            ccc = QtGui.QColor(colr.color())
            ccc.setAlphaF(.5)
            colr.setColor(ccc)
            painter.fillRect(option.rect, colr)
        if editOptions[1] == "T":
            # Edit valid
            pass
        elif editOptions[1] == "N":
            # Edit need to check
            colr = QtGui.QBrush(QtCore.Qt.red)
            ccc = QtGui.QColor(colr.color())
            ccc.setAlphaF(.03)
            colr.setColor(ccc)
            painter.fillRect(option.rect, colr)
        painter.restore()
        # m_item.setData( m_edits[i][4], QtCore.Qt.UserRole + 2 )
        # m_item.setData( m_edits[i][1].split( "|" )[-1], QtCore.Qt.UserRole + 3 )
        # m_item.setData( m_edits[i][2], QtCore.Qt.UserRole + 5 )
