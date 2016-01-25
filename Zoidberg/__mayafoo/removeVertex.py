import maya.cmds as cmds
import maya.OpenMaya as om
import subprocess

def queryNonVertex( geometry=[], remove=False, debug=True ):
    result = []
    geometry = geometry and ( type( geometry ) is list and geometry or [ geometry ]) or cmds.ls( sl=True, dag=True, type="mesh" )
    for i in range( 0, len( geometry )):
        if debug is True:
            print geometry[i]
        selectionList = om.MSelectionList()
        selectionList.add( geometry[i] )
        dagPath = om.MDagPath()
        selectionList.getDagPath(0, dagPath )
        iterator = om.MItMeshVertex( dagPath )
        while not iterator.isDone():
            array = om.MIntArray()
            iterator.getConnectedEdges( array )
            vtx = iterator.index()
            if array.length() < 1:
                result.append( "%s.vtx[%s]" % ( geometry[i], vtx ))
            iterator.next()
    if remove is True:
        if result:
            cmds.polyDelVertex( result, constructionHistory=False )
    return result