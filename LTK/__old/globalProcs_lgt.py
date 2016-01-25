#! /usr/bin/env python
# -*- coding: utf-8 -*-

# module gPrc
# file gPrc.py
# Global Procedures Module

import sip
import maya.OpenMayaUI as mayaUi
from PyQt4 import QtCore, QtGui
import maya.cmds as cmds


def getMayaWindow():
    """ Getting Maya Window"""
    dWindow = mayaUi.MQtUtil.mainWindow()
    return sip.wrapinstance(long(dWindow), QtCore.QObject)


def version(major=0, minor=0, build=0, revision=0):
    return str(str(major) + '.' + str(minor) + '.' + str(build) + '.' + str(revision))


class CharRenderBuild(object):
    def __init__(self):
        self.parent_shapes = self.sel_prnt_trgt_shapes()[0]
        self.target_shapes = self.sel_prnt_trgt_shapes()[1]
        self.copy_event = False
        self.found_match = {}
        self.non_found_parent = []
        self.non_found_target = []

    def sel_prnt_trgt_shapes(self):
        selTransform = cmds.ls(os=True, l=True)
        if selTransform:
            selParent = cmds.listRelatives(selTransform[0], ad=True, f=True, typ='transform')
            selTarget = cmds.listRelatives(selTransform[1:], ad=True, f=True, typ='transform')
            if not selParent:
                selParent = selTransform[0]
            if not selTarget:
                selTarget = selTransform[1:]
            selParentS = cmds.listRelatives(selParent, ad=True, s=True, f=True, ni=True)
            selTargetS = cmds.listRelatives(selTarget, ad=True, s=True, f=True, ni=True)
            return [selParentS, selTargetS]
        else:
            return [0, 0]

    def find_match(self, shapename=False, topology=False, uv=False, sets=True):
        # search parent ident
        if self.parent_shapes:
            for nodeP in self.parent_shapes:
                curPname = nodeP.split(':')[-1].split('|')[-1]
                self.copy_event = False
                for nodeT in self.sel_prnt_trgt_shapes()[1]:
                    curTname = nodeT.split(':')[-1].split('|')[-1]
                    if topology is True or uv is True:
                        compareId = cmds.polyCompare(nodeP, nodeT, v=1, e=1, fd=1)
                        if compareId <= 1:
                            self.found_match[nodeP] = nodeT
                            self.copy_event = True
                    elif curPname == curTname and shapename is True:
                        self.found_match[nodeP] = nodeT
                        self.copy_event = True
                    elif shapename is False and topology is False:
                        self.found_match[nodeP] = nodeT
                if not self.copy_event:
                    self.non_found_parent.append(nodeP)  # not found ident for paren shape and add to list
        # search target ident
        if self.target_shapes:  # loop for found not ident by name target shapes
            for nodeT in self.target_shapes:
                curTname = nodeT.split(':')[-1].split('|')[-1]
                self.copy_event = False
                for nodeP in self.sel_prnt_trgt_shapes()[0]:
                    curPname = nodeP.split(':')[-1].split('|')[-1]
                    if curTname == curPname and shapename is True and topology is False:
                        self.copy_event = True
                    if shapename is False and topology is True:
                        compareId = cmds.polyCompare(nodeP, nodeT, v=1, e=1, fd=1)
                        if compareId <= 1:
                            self.copy_event = True
                if not self.copy_event:
                    self.non_found_target.append(nodeT)  # not found ident for target shape and add to list
        if sets is True:
            self.create_non_found_sets()
        return self.found_match  # return sets with not fount ident shapes

    def create_non_found_sets(self):
        parent_set = 'nonFoundParent_set'
        target_set = 'nonFoundTarget_set'
        if self.non_found_parent:
            if cmds.objExists(parent_set):
                cmds.delete(parent_set)
            cmds.sets(self.non_found_parent, n=parent_set)
        if self.non_found_target:
            if cmds.objExists(target_set):
                cmds.delete(target_set)
            cmds.sets(self.non_found_target, n=target_set)

    def copy_user_attr(self, shapename=False, topology=False, uv=True, sets=True, history=True):
        match_list = self.find_match(shapename=shapename, topology=topology, uv=uv, sets=sets)
        if match_list:
            for parent in match_list:
                listattrvalue = {}
                listdatatype = {}
                userattr = cmds.listAttr(parent, ud=True)
                target = match_list[parent]
                if uv and cmds.nodeType(target) == 'mesh' and cmds.nodeType(parent) == 'mesh':
                    cmds.transferAttributes(parent, target,
                                            transferUVs=1, transferColors=0, searchMethod=3,
                                            sampleSpace=5, flipUVs=0, transferPositions=0,
                                            transferNormals=0, colorBorders=0)
                if history is True:
                    cmds.delete([parent, target], ch=True)
                if userattr:
                    for attr in userattr:
                        nodetype = cmds.nodeType(parent)
                        checkrendershape = cmds.getAttr(parent + '.intermediateObject')
                        if checkrendershape != 1 or nodetype != 'mesh':
                            value = cmds.getAttr("%s.%s" % (parent, attr))
                            data = cmds.getAttr("%s.%s" % (parent, attr), typ=True)
                            listattrvalue[attr] = value
                            listdatatype[attr] = data
                for attr in listattrvalue:
                    if not cmds.attributeQuery(attr, node=target, ex=True):
                        if listdatatype[attr] == 'string':
                            cmds.addAttr(target, longName=attr, dataType=listdatatype[attr])
                            cmds.setAttr("%s.%s" % (target, attr), listattrvalue[attr], type=listdatatype[attr])
                        else:
                            cmds.addAttr(target, longName=attr)
                            cmds.setAttr("%s.%s" % (target, attr), listattrvalue[attr])
                    else:
                        # cmds.warning('Attribute ' + attr + ' already on ' + seltargetshapes)
                        if cmds.getAttr("%s.%s" % (target, attr), se=True):
                            if listdatatype[attr] == 'string':
                                cmds.setAttr("%s.%s" % (target, attr), listattrvalue[attr], type=listdatatype[attr])
                            else:
                                cmds.setAttr("%s.%s" % (target, attr), listattrvalue[attr])
        else:
            cmds.warning("No matching objects found!")