#! /usr/bin/env python
# -*- coding: utf-8 -*-

# module gPrc
# file gPrc.py
# Global Procedures Module

import shiboken as sip
from PySide import QtCore, QtGui

import maya.OpenMayaUI as mayaUi


def getMayaWindow():
    """ Getting Maya Window"""
    dWindow = mayaUi.MQtUtil.mainWindow()
    return sip.wrapInstance(long(dWindow), QtGui.QMainWindow)


def version(major=0, minor=0, build=0, revision=0):
    return str(str(major) + '.' + str(minor) + '.' + str(build) + '.' + str(revision))