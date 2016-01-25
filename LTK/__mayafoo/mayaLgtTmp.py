import maya.cmds as cmds

def copy_user_attr(selparentshapes, seltargetshapes, copyUV=True):
    listattrvalue = {}
    listdatatype = {}
    userattr = cmds.listAttr(selparentshapes, ud=True)
    if copyUV and cmds.nodeType(seltargetshapes) == 'mesh' and cmds.nodeType(selparentshapes) == 'mesh':
            cmds.transferAttributes(selparentshapes, seltargetshapes, transferUVs=1, transferColors=2, searchMethod=3, sampleSpace=5, flipUVs=False)
    if userattr:
        for attr in userattr:
            nodetype = cmds.nodeType(selparentshapes)
            checkrendershape = cmds.getAttr(selparentshapes + '.intermediateObject')
            if checkrendershape != 1 or nodetype != 'mesh':
                key = attr
                value = cmds.getAttr("%s.%s" % (selparentshapes, key))
                data = cmds.getAttr("%s.%s" % (selparentshapes, key), typ=True)
                listattrvalue[key] = value
                listdatatype[key] = data
    checkrendershape = cmds.getAttr(seltargetshapes + '.intermediateObject')
    if checkrendershape != 1:
        for key in listattrvalue:
            if not cmds.attributeQuery(key, node=seltargetshapes, ex=True):
                if listdatatype[key] == 'string':
                    cmds.addAttr(seltargetshapes, longName=key, dataType=listdatatype[key])
                    cmds.setAttr("%s.%s" % (seltargetshapes, key), listattrvalue[key], type=listdatatype[key])
                else:
                    cmds.addAttr(seltargetshapes, longName=key)
                    cmds.setAttr("%s.%s" % (seltargetshapes, key), listattrvalue[key])
            else:
                cmds.warning('Attribute ' + key + ' already on ' + seltargetshapes)
                if cmds.getAttr("%s.%s" % (seltargetshapes, key), se=True):
                    if listdatatype[key] == 'string':
                        cmds.setAttr("%s.%s" % (seltargetshapes, key), listattrvalue[key], type=listdatatype[key])
                    else:
                        cmds.setAttr("%s.%s" % (seltargetshapes, key), listattrvalue[key])

def compare_shape_name():
    selTransform = cmds.ls(os=True, l=True)
    selParent = cmds.listRelatives(selTransform[0], ad=True, f=True, typ='transform')
    selTarget = cmds.listRelatives(selTransform[1:], ad=True, f=True, typ='transform')
    selParentS = cmds.listRelatives(selParent, ad=True, s=True, f=True)
    selTargetS = cmds.listRelatives(selTarget, ad=True, s=True, f=True)

    # selParentSCount = len(selParentS)
    # selTargetSCount = len(selTargetS)

    for nodeP in selParentS:
        curPname = nodeP.split(':')[-1]
        curPname = curPname.split('|')[-1]
        for nodeT in selTargetS:
            curTname = nodeT.split(':')[-1]
            curTname = curTname.split('|')[-1]
            if curPname == curTname:
                copy_user_attr(nodeP, nodeT)

compare_shape_name()


def disconnectShaveAttr(node):
    shaveShapeNode = cmds.listRelatives(node, ad=True, f=True, type="shaveHair")
    sahveAttrList = ['hairCount', 'hairSegments', 'rootThickness', 'tipThickness', 'randScale', 'active']
    for shape in shaveShapeNode:
        for attr in sahveAttrList:
            connectionList = cmds.listConnections(shape + '.' + attr, p=True)
            if connectionList:
                for connect in connectionList:
                    cmds.disconnectAttr(connect, (shape + '.' + attr))
                    print connect

disconnectShaveAttr(cmds.ls(sl=True))


def delete_attr(nodelist=None, attrlist=None):
    """
    Delete all attr from attrlist
    """
    if not nodelist and not attrlist:
        selCur = cmds.ls(sl=True, l=True)
        selCurH = cmds.listRelatives(ad=True, f=True)
        nodelist = selCur + selCurH
        attrlist = ['ml_jsFile', 'rman__torattr___preShapeScript', 'rman__torattr___postShapeScript']
    for node in nodelist:
        for attr in attrlist:
            if cmds.attributeQuery(attr, n=node, exists=True):
                cmds.deleteAttr(node, at=attr)


delete_attr()

def set_attr(nodelist=None, attrlist=None):
    """
    Set all attr from attrlist
    """
    if not nodelist and not attrlist:
        selCur = cmds.ls(sl=True, l=True)
        selCurH = cmds.listRelatives(ad=True, f=True)
        nodelist = selCur + selCurH
        attrlist = ['active']
        value = 0
        nodetype = 'shaveHair'
    for node in nodelist:
        if cmds.nodeType(node) == nodetype:
            for attr in attrlist:
                if cmds.attributeQuery(attr, n=node, exists=True):
                    cmds.setAttr("%s.%s" % (node, attr), value)

set_attr()


def delete_user_attr(nodelist=None, attrlist=None):
    """
    Delete all user attrs
    """
    if not nodelist and not attrlist:
        selCur = cmds.ls(sl=True, l=True)
        selCurH = cmds.listRelatives(ad=True, f=True)
        nodelist = selCur + selCurH
    for node in nodelist:
        attrlist = cmds.listAttr(node, ud=True)
        if attrlist:
            for attr in attrlist:
                connectionList = cmds.listConnections(node + '.' + attr, p=True)
                if cmds.getAttr("%s.%s" % (node, attr), l=True):
                    cmds.setAttr("%s.%s" % (node, attr), l=False)
                elif connectionList:
                    for con in connectionList:
                        try:
                            cmds.disconnectAttr((node + '.' + attr), con)
                        except:
                            cmds.disconnectAttr(con, (node + '.' + attr))
                cmds.deleteAttr(node, at=attr)

delete_user_attr()


def autoUndoOn():
    undoStatus = cmds.undoInfo(q=True, st=True)
    if not undoStatus:
        print 'Undo status OFF. Change to ON.'
        cmds.undoInfo(st=True)
    else:
        print 'Undo status ON.'


autoUndoOn()


def select_samename_node(name):
    sel = cmds.ls(sl=True)
    cmds.select(cl=True)
    sel_hr = cmds.listRelatives(sel, ad=True) + sel
    for node in sel_hr:
        if node.count(name):
            cmds.select(node, add=True)

select_samename_node('body_geo')


def select_node_by_type(nodeType):
    sel = cmds.ls(sl=True, l=True)
    sel_ad = cmds.listRelatives(sel, ad=True, f=True) + sel
    cmds.select(cl=True)
    for node in sel_ad:
        if cmds.nodeType(node) == nodeType:
            cmds.select((cmds.listRelatives(node, p=True)), add=True)

# remove slim shader
# pymel.mayautils.source
# "//server-3d/Project/lib/setup/maya/maya_scripts_rfm3/plugInSlim/RemoveSlimSurfaceAtr.mel";
# cmds.evalDeferred()RemoveShaderAttr slim_coshader;
# RemoveShaderAttr slim_shader;
# RemoveShaderAttr slim_ensemble;


def select_node_by_attr(attr, nodelist=None):
    """
    Select node by attr and value
    """
    if not nodelist:
        selCur = cmds.ls(sl=True, l=True)
        selCurH = cmds.listRelatives(ad=True, f=True)
        nodelist = selCur + selCurH
    cmds.select(cl=True)
    for node in nodelist:
        for key in attr:
            if cmds.attributeQuery(key, node=node, ex=True):
                attrValueCur = cmds.getAttr(node + '.' + key)
                if attrValueCur == attr[key]:
                    cmds.select(node, add=True)

select_node_by_attr({'intermediateObject':1, 'visibility':0})