import maya.cmds as cmds

def renderSetup():
    maxFrame = cmds.playbackOptions(q=True, max=True)
    minFrame = cmds.playbackOptions(q=True, min=True)


    # Common
    cmds.setAttr("defaultRenderGlobals.animation", 1)
    cmds.setAttr("defaultRenderGlobals.startFrame", minFrame)
    cmds.setAttr("defaultRenderGlobals.endFrame", maxFrame)
    cmds.setAttr("defaultRenderGlobals.byFrameStep", 1)
    cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)

    cmds.setAttr("redshiftOptions.imageFormat", 1)
    cmds.setAttr("redshiftOptions.exrBits", 16)
    cmds.setAttr("redshiftOptions.exrCompression", 0)
    cmds.setAttr("redshiftOptions.exrIsTiled", 0)
    cmds.setAttr("defaultResolution.width", 960)
    cmds.setAttr("defaultResolution.height", 540)
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


renderSetup()