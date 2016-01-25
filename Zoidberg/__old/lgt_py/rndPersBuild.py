__author__ = 'korovkin_m'
import maya.cmds as cmds

class CharRenderBuild(object):
    def __init__(self):
        self.copy_event = False
        self.non_found_parent = []
        self.non_found_target = []

    def copy_user_attr(self, selparentshapes, seltargetshapes, copyUV=True):
        listattrvalue = {}
        listdatatype = {}
        userattr = cmds.listAttr(selparentshapes, ud=True)
        if copyUV and cmds.nodeType(seltargetshapes) == 'mesh' and cmds.nodeType(selparentshapes) == 'mesh':
            print "Copy UV from" + selparentshapes + " to " + seltargetshapes
            cmds.transferAttributes(selparentshapes, seltargetshapes,
                                    transferUVs=1, transferColors=0, searchMethod=3,
                                    sampleSpace=5, flipUVs=0, transferPositions=0,
                                    transferNormals=0, colorBorders=0)
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

    def sel_prnt_trgt_shapes(self):
        selTransform = cmds.ls(os=True, l=True)
        selParent = cmds.listRelatives(selTransform[0], ad=True, f=True, typ='transform')
        selTarget = cmds.listRelatives(selTransform[1:], ad=True, f=True, typ='transform')
        if not selParent:
            selParent = selTransform[0]
        if not selTarget:
            selTarget = selTransform[1:]
        selParentS = cmds.listRelatives(selParent, ad=True, s=True, f=True)
        selTargetS = cmds.listRelatives(selTarget, ad=True, s=True, f=True)
        return [selParentS, selTargetS]

    def do_copy_attr_uv(self, uv=False, singleMode=False):
        for nodeP in self.sel_prnt_trgt_shapes()[0]:
            curPname = nodeP.split(':')[-1].split('|')[-1]
            self.copy_event = False
            for nodeT in self.sel_prnt_trgt_shapes()[1]:
                curTname = nodeT.split(':')[-1].split('|')[-1]
                if curPname == curTname and not singleMode:
                    self.copy_user_attr(nodeP, nodeT, uv)
                    self.copy_event = True
                elif singleMode:
                    self.copy_user_attr(nodeP, nodeT, uv)
            if not self.copy_event:
                self.non_found_parent.append(nodeP)
        for nodeT in self.sel_prnt_trgt_shapes()[1]:
            curTname = nodeT.split(':')[-1].split('|')[-1]
            self.copy_event = False
            for nodeP in self.sel_prnt_trgt_shapes()[0]:
                curPname = nodeP.split(':')[-1].split('|')[-1]
                if curTname == curPname:
                    self.copy_event = True
            if not self.copy_event:
                self.non_found_target.append(nodeT)
        return [self.non_found_target, self.non_found_parent]