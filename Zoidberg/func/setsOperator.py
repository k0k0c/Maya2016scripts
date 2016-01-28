import maya.cmds as cmds

class setsOperator(object):
    def __init__(self, setname):
        self.sel = cmds.ls(sl=True, l=True)
        self.setname = setname
        self.exprExist = cmds.objExists(self.setname)

    def add(self):
        if self.exprExist != 1:
            cmds.sets(n=self.setname)
        print self.sel
        cmds.sets(self.sel, include=self.setname)

    def exclude(self):
        if self.exprExist == 1:
            cmds.sets(self.sel, rm=self.setname)

    def select(self):
        if self.exprExist == 1:
            nodes = cmds.sets(self.setname, nodesOnly=True, query=True)
            cmds.select(nodes)

    def visibility(self):
        if self.exprExist == 1:
            nodes = cmds.sets(self.setname, nodesOnly=True, query=True)
            for node in nodes:
                vis = cmds.getAttr("%s.%s" % (node, "visibility"))
                lock = cmds.getAttr("%s.%s" % (node, "visibility"), se=True)
                if lock != 1:
                    continue
                elif vis == 1:
                    cmds.setAttr("%s.%s" % (node, "visibility"), 0)
                elif vis == 0:
                    cmds.setAttr("%s.%s" % (node, "visibility"), 1)

    def merge(self):
        pass