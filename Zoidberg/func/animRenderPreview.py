# coding=utf-8
import maya.cmds as cmds
import maya.mel as mel

from deadlineSceneName import *
from PySide import QtCore, QtGui
import shiboken
import maya.OpenMayaUI as mayaUi


def getMayaWindow():
    """ Getting Maya Window"""
    dWindow = mayaUi.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(dWindow), QtGui.QMainWindow)


class ChooseCamForRender(object):
    def __init__(self, submit):
        self.cam = None
        self.cams = []
        self.submit = submit
        self.listCam()

    def listCam(self):
        camsTMP = cmds.listCameras()
        for i in camsTMP:
            cmds.setAttr(i + ".renderable", 0)
            if i != 'front' and i != 'persp' and i != 'side' and i != 'top':
                self.cams.append(i)
        if len(self.cams) == 1:
            self.cam = self.cams[0]
            self.lockTroughtCamera(self.cam)
        if len(self.cams) > 1:
            self.windowChooseCam()

    def addIntoTextScrollList(self):
        for i in self.cams:
            cmds.textScrollList("CamtexTScrollList", e=1, append=[i])

    def lockTroughtCamera(self, cam=None):
        if not cam:
            self.cam = cmds.textScrollList("CamtexTScrollList", q=1, si=1)[0]
            cmds.lookThru(self.cam)
        else:
            cmds.lookThru(self.cam)

    def windowChooseCam(self):
        if cmds.window('ChooseRenderCam', exists=True):
            cmds.deleteUI('ChooseRenderCam', window=True)
        try:
            cmds.windowPref('ChooseRenderCam', r=True)
        except:
            pass

        chooseCamWin = cmds.window('ChooseRenderCam', h=220, w=300, te=300, le=900, s=1, title="Choose Camera")

        AllrowColumnLayout = cmds.columnLayout(w=200)

        CamtexTScrollList = cmds.textScrollList("CamtexTScrollList", allowMultiSelection=False, showIndexedItem=4,
                                                dcc=self.lockTroughtCamera, sc=self.lockTroughtCamera)
        renderButton = cmds.button("Render", c=self.submitRender)

        self.addIntoTextScrollList()

        cmds.setParent('..')
        cmds.showWindow(chooseCamWin)

    def submitRender(self, *args, **kwargs):
        if self.cam:
            cmds.setAttr(self.cam + ".renderable", 1)
            self.submit(self.cam)
            cmds.deleteUI("ChooseRenderCam")
            # cmds.deleteUI("unifiedRenderGlobalsWindow")
        else:
            cmds.warning("Select camera!!!")


class AnimPreviwRender(object):
    def __init__(self):
        self.lightName = "rsDome_preRenderShape"
        self.renderPatch = renderPath("preview")
        self.scenePatch = cmds.file(q=True, sn=True)[0:32]
        self.sceneName = cmds.file(q=True, sn=True, shn=True).split(".")[0]

    def checkPatch(self):
        if self.scenePatch == "//samba/Space_Academy/Animation/":
            return True
        else:
            mesage = QtGui.QMessageBox(parent=getMayaWindow())
            mesage.setText("""Save scene to the server""")
            mesage.show()
            return False

    def checkCamera(self):
        ChooseCamForRender(self.submitJob)

    def remake_render_settings_ui(self, renderer="mayaSoftware"):
        """ Remakes the render settings window """
        # Unlock the render globals' current renderer attribute
        cmds.setAttr("defaultRenderGlobals.currentRenderer", l=False)

        # Sets the current renderer to given renderer
        cmds.setAttr("defaultRenderGlobals.currentRenderer", renderer, type="string")

        # Deletes the render settings window UI completely
        if cmds.window("unifiedRenderGlobalsWindow", exists=True):
            cmds.deleteUI("unifiedRenderGlobalsWindow")
        # Remake the render settings UI
        mel.eval('unifiedRenderGlobalsWindow;')

    def renderSetup(self):
        self.remake_render_settings_ui(renderer="redshift")
        maxFrame = cmds.playbackOptions(q=True, max=True)
        minFrame = cmds.playbackOptions(q=True, min=True)


        # Common
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", self.sceneName + "_preview", type="string")
        cmds.setAttr("defaultRenderGlobals.animation", 1)
        cmds.setAttr("defaultRenderGlobals.startFrame", minFrame)
        cmds.setAttr("defaultRenderGlobals.endFrame", maxFrame)
        cmds.setAttr("defaultRenderGlobals.byFrameStep", 1)
        cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)

        cmds.setAttr("redshiftOptions.imageFormat", 4)
        cmds.setAttr("redshiftOptions.jpegQuality", 95)

        cmds.setAttr("defaultResolution.width", 1280)
        cmds.setAttr("defaultResolution.height", 720)
        cmds.setAttr("defaultResolution.deviceAspectRatio", 1.777)

        # Output
        cmds.setAttr("redshiftOptions.unifiedMinSamples", 4)
        cmds.setAttr("redshiftOptions.unifiedMaxSamples", 64)
        cmds.setAttr("redshiftOptions.unifiedAdaptiveErrorThreshold", 0.050)

        # AOV
        cmds.setAttr("redshiftOptions.aovGlobalEnableMode", 0)

        # Opt
        cmds.setAttr("redshiftOptions.reflectionMaxTraceDepth", 1)
        cmds.setAttr("redshiftOptions.refractionMaxTraceDepth", 3)
        cmds.setAttr("redshiftOptions.combinedMaxTraceDepth", 4)

        cmds.setAttr("redshiftOptions.diffuseRayCutOffThreshold", 0.02)
        cmds.setAttr("redshiftOptions.reflectionRayCutOffThreshold", 0.02)
        cmds.setAttr("redshiftOptions.refractionRayCutOffThreshold", 0.02)
        cmds.setAttr("redshiftOptions.directLightingShadowCutOffThreshold", 0.02)
        cmds.setAttr("redshiftOptions.directLightingCutOffThreshold", 0.02)

        cmds.setAttr("redshiftOptions.russianRouletteImportanceThreshold", 0.005)

        cmds.setAttr("redshiftOptions.textureSamplingTechnique", 2)

        # GI
        cmds.setAttr("redshiftOptions.primaryGIEngine", 0)
        cmds.setAttr("redshiftOptions.secondaryGIEngine", 0)
        cmds.setAttr("redshiftOptions.bruteForceGINumRays", 1)
        cmds.setAttr("redshiftOptions.photonCausticsEnable", 0)

        # SSS
        cmds.setAttr("redshiftOptions.subsurfaceScatteringRate", -2)
        cmds.setAttr("redshiftOptions.subsurfaceScatteringInterpolationQuality", 4)
        cmds.setAttr("redshiftOptions.subsurfaceScatteringNumGIRays", 32)

        # deadline
        if cmds.attributeQuery("deadlineJobName", node="defaultRenderGlobals", ex=True):
            jobName = cmds.getAttr("defaultRenderGlobals.deadlineJobName").split("_preview")[0] + "_preview"
            cmds.setAttr("defaultRenderGlobals.deadlineJobName", jobName, type="string")
        cmds.setAttr("defaultRenderGlobals.deadlineGroup", "preview", typ="string")
        cmds.setAttr("defaultRenderGlobals.deadlineJobPriority", 20)
        cmds.setAttr("defaultRenderGlobals.deadlineOutputFilePath", self.renderPatch, typ="string")
        cmds.setAttr("defaultRenderGlobals.imfPluginKey", "jpg", typ="string")

    def setAovEnable(self, set=0, sw=None):
        redshiftAOVnodes = cmds.ls(typ="RedshiftAOV")
        for node in redshiftAOVnodes:
            curval = cmds.getAttr(node + ".enabled")
            if sw == True:
                if curval == 0:
                    cmds.setAttr(node + ".enabled", 1)
                if curval == 1:
                    cmds.setAttr(node + ".enabled", 0)
            else:
                cmds.setAttr(node + ".enabled", set)

    def lightSetup(self):
        # Hide existing lights
        rsLights = []
        existLights = cmds.ls(lt=True)
        rsTypeList = ["RedshiftDomeLight", "RedshiftPortalLight", "RedshiftIESLight", "RedshiftPhysicalLight"]
        for type in rsTypeList:
            lgtCurrentType = cmds.ls(typ=type)
            rsLights.extend(lgtCurrentType)

        existLights.extend(rsLights)

        for node in existLights:
            if node != self.lightName:
                n = cmds.listRelatives(node, p=True)
                cmds.setAttr(n[0] + ".visibility", 0)

        # Create a new rsDome light
        if not cmds.objExists(self.lightName):
            cmds.shadingNode("RedshiftDomeLight", name=self.lightName, asLight=True)
        else:
            cmds.setAttr(self.lightName + ".samples", 8)
            cmds.setAttr(self.lightName + ".viewportResolution", 512)
            cmds.setAttr(self.lightName + ".volumeNumSamples", 1)
            cmds.setAttr(self.lightName + ".background_enable", 0)

    def setProxy(self, value=0):
        for curv in cmds.ls(typ="transform"):
            if curv.split(":")[-1:][0] == "Main":
                if cmds.attributeQuery("Proxy", node=curv, ex=True):
                    cmds.setAttr(curv + ".Proxy", value)

    def submitJob(self, cam=None):
        mel.eval("SubmitJobToDeadline;")
        # cmds.deleteUI()
        self.renderSetup()
        self.setAovEnable()
        self.lightSetup()
        self.setProxy()
        mel.eval("SubmitJobToDeadline;DeadlineSubmitterOnOk();")
        cmds.delete(cmds.listRelatives(self.lightName, p=True))

    def startup(self):
        pathcheck = self.checkPatch()
        if pathcheck:
            self.choosecam = ChooseCamForRender(self.submitJob)