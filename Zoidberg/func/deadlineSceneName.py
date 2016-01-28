import maya.cmds as cmds
import os


def renderPath(add=None):
    renderPath = "//SAMBA/Space_Academy/Render/"
    sceneName = cmds.file(q=True, sn=True, shn=True).split(".")[0]
    finalPath = ""
    if add:
        addPatch = add + "/"
    else:
        addPatch = ""
    try:
        sceneName = sceneName.split("_")
        ser = sceneName[0].split("s")[1]
        ep = sceneName[1].split("ep")[1]
        sc = sceneName[2].split("sc")[1]
        dirs = os.listdir(renderPath)
        for s in dirs:
            temp = s.split("_")
            for i in temp:
                if ser in i:
                    ser = s
        finalPath = renderPath + ser + "/ep_" + ep + "/sc_" + sc + "/" + addPatch
    except:
        pass
    if finalPath == "":
        finalPath = cmds.workspace(q=True, fn=1) + "/images" + "/" + addPatch

    if not os.path.exists(os.path.dirname(finalPath)):
        os.makedirs(os.path.dirname(finalPath))

    finalPathRight = finalPath.replace("/", "\\")

    return finalPathRight
