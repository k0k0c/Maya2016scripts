#! /usr/bin/env python
# -*- coding: utf-8 -*-

# module gPrc
# file gPrc.py
# Global Procedures Module

import sip
import maya.OpenMayaUI as mayaUi
from PyQt4 import QtCore, QtGui
# import maya.cmds as cmds

def getMayaWindow():
    """ Getting Maya Window"""
    dWindow = mayaUi.MQtUtil.mainWindow()
    return sip.wrapinstance(long(dWindow), QtCore.QObject)

def version(major = 0,minor = 0,build = 0,revision = 0):
    return str(str(major) + '.' + str(minor) + '.' + str(build) + '.' + str(revision))
