import maya.cmds as cmds
import maya.OpenMaya as om
import re

def listFromView( camera, nodes="", ignoreNodes="", nodeType="", ignoreType="", outside=False, animation=False, start=0, end=0, frameSpacing=1, frustum=0, aspect=1 ):
    """
    camera - Camera shape name.
    nodes - List nodes for more fastest search.
    nodeType - Return nodes by user specified type.
    ignoreType - Ignore nodes by user specified type.
    outside - Return nodes not visible in camera.
    frustum - Camera frustum mode ( 0:Viewing, 1:Rendering, 2:Film )
    aspect - Aspect mode ( 0:Camera, 1:Device )
    animation - List all nodes from camera view with animation.
    start - Animation start time.
    end - Animation end time.
    frameSpacing - Skip every frame.
    """
    if not cmds.nodeType( camera ) in [ "camera", "stereoRigCamera" ]:
        print "%s is not camera" % camera
        return None
    m_result = []
    m_nodes = nodes == "" and cmds.ls( dag=True, shapes=True ) or ( type( nodes ) is list and nodes or [ nodes ] )
    #Read settings.
    m_time = int( cmds.currentTime( query=True ))
    if animation is True:
        m_start = start == 0 and cmds.playbackOptions( query=True, animationStartTime=True ) or start
        m_end = end == 0 and cmds.playbackOptions( query=True, animationEndTime=True ) or end
        m_start = int( m_start )
        m_end = int( m_end ) + 1
        m_range = range( m_start, m_end )
        if frameSpacing > 1:
            m_range = [ m_range[f] for f in range( 0, len( m_range )) if f%frameSpacing == 0 ]
    else:
        m_start = int( cmds.currentTime( query=True ))
        m_end = m_start + 1
        m_range = range( m_start, m_end )
    #Read camera.
    m_selection= om.MSelectionList()
    m_dag= om.MDagPath()
    m_selection.add( camera )
    m_selection.getDagPath( 0, m_dag )
    m_cameraDag = om.MFnCamera( m_dag )
    if aspect == 1:
        m_globals = cmds.ls( renderGlobals=True )
        m_rezolution = cmds.listConnections( "%s.resolution" % m_globals[0] )
        m_aspect = cmds.getAttr( "%s.deviceAspectRatio" % m_rezolution[0] )
    else:
        m_aspect = m_cameraDag.aspectRatio()
    for f in m_range:
        cmds.currentTime( f )
        #Read camera settings.
        m_focalLenght = m_cameraDag.focalLength()
        m_cameraIMatrix = m_dag.inclusiveMatrixInverse()
        m_nearClip = m_cameraDag.nearClippingPlane()
        m_farClip =  m_cameraDag.farClippingPlane()
        m_left = om.MScriptUtil()
        m_left.createFromDouble( 0.0 )
        m_leftPtr = m_left.asDoublePtr()
        m_right = om.MScriptUtil()
        m_right.createFromDouble( 0.0 )
        m_rightPtr = m_right.asDoublePtr()
        m_bottom = om.MScriptUtil()
        m_bottom.createFromDouble( 0.0 )
        m_bottomPtr = m_bottom.asDoublePtr()
        m_top = om.MScriptUtil()
        m_top.createFromDouble( 0.0 )
        m_topPtr = m_top.asDoublePtr()
        if frustum == 1:
            m_cameraDag.getRenderingFrustum( m_aspect, m_leftPtr, m_rightPtr, m_bottomPtr, m_topPtr )
        if frustum == 2:
            m_cameraDag.getFilmFrustum( m_focalLenght, m_leftPtr, m_rightPtr, m_bottomPtr, m_topPtr )
        else:
            m_cameraDag.getViewingFrustum( m_aspect, m_leftPtr, m_rightPtr, m_bottomPtr, m_topPtr, False, True )
        m_left = m_left.getDoubleArrayItem( m_leftPtr, 0 )
        m_right = m_right.getDoubleArrayItem( m_rightPtr, 0 )
        m_bottom = m_bottom.getDoubleArrayItem( m_bottomPtr, 0 )
        m_top = m_top.getDoubleArrayItem( m_topPtr, 0 )
        #Make planes.
        m_planes = []
        a = om.MVector( m_right, m_top, -m_nearClip )
        b = om.MVector( m_right, m_bottom, -m_nearClip )
        c = ( a ^ b ).normal()
        m_planes.append( [ c, 0.0 ] )
        a = om.MVector( m_left, m_bottom, -m_nearClip )
        b = om.MVector( m_left, m_top, -m_nearClip )
        c = ( a ^ b ).normal()
        m_planes.append( [ c, 0.0 ] )
        a = om.MVector( m_right, m_bottom, -m_nearClip )
        b = om.MVector( m_left, m_bottom, -m_nearClip )
        c = ( a ^ b ).normal()
        m_planes.append( [ c, 0.0 ] )
        a = om.MVector( m_left, m_top, -m_nearClip )
        b = om.MVector( m_right, m_top, -m_nearClip )
        c = ( a ^ b ).normal()
        m_planes.append( [ c, 0.0 ] )
        c = om.MVector(0, 0, 1)
        m_planes.append( [ c, m_farClip ] )
        c = om.MVector(0, 0, -1)
        m_planes.append( [ c, m_nearClip ] )
        for i in range( 0, len( m_nodes )):
            m_type = cmds.nodeType( m_nodes[i] )
            if m_nodes[i] not in m_result and ( nodeType != "" and m_type in nodeType or nodeType == "" ):
                m_points = []
                m_selectionListS = om.MSelectionList()
                m_dagS = om.MDagPath()
                m_selectionListS.add( m_nodes[i] )
                m_selectionListS.getDagPath( 0, m_dagS )
                m_dagEMatrix = m_dagS.exclusiveMatrix()
                m_fnDag = om.MFnDagNode( m_dagS )
                m_bbox = m_fnDag.boundingBox()
                m_bboxMin = m_bbox.min()
                m_bboxMax = m_bbox.max()
                m_points.append( m_bboxMin * m_dagEMatrix * m_cameraIMatrix )
                m_points.append( om.MPoint( m_bboxMax.x, m_bboxMin.y, m_bboxMin.z ) * m_dagEMatrix * m_cameraIMatrix )
                m_points.append( om.MPoint( m_bboxMax.x, m_bboxMin.y, m_bboxMax.z ) * m_dagEMatrix * m_cameraIMatrix )
                m_points.append( om.MPoint( m_bboxMin.x, m_bboxMin.y, m_bboxMax.z ) * m_dagEMatrix * m_cameraIMatrix )
                m_points.append( om.MPoint( m_bboxMin.x, m_bboxMax.y, m_bboxMin.z ) * m_dagEMatrix * m_cameraIMatrix )
                m_points.append( om.MPoint( m_bboxMax.x, m_bboxMax.y, m_bboxMin.z ) * m_dagEMatrix * m_cameraIMatrix )
                m_points.append( m_bboxMax * m_dagEMatrix * m_cameraIMatrix )
                m_points.append( om.MPoint( m_bboxMin.x, m_bboxMax.y, m_bboxMax.z ) * m_dagEMatrix * m_cameraIMatrix )
                #Validate node position.
                m_inside = 0
                m_len = len( m_points )
                m_bool = True
                for n in range( 0, 6 ):
                    m_behind = 0
                    if m_behind == m_len:
                        m_bool = False
                        break
                    for p in range( 0, m_len ):
                        m_vectorPoint = om.MVector( m_points[p].x, m_points[p].y, m_points[p].z )
                        m_value = ( m_planes[n][0] * m_vectorPoint ) + m_planes[n][-1]
                        if m_value < 0.0:
                            m_behind += 1
                        if m_behind == m_len:
                            m_bool = False
                            break
                        elif m_behind == 0 :
                            m_inside += 1
                if m_inside == 6 or m_bool is True:
                    m_result.append( m_nodes[i] )
    cmds.currentTime( m_time )
    if outside is True:
        m_result = [ m_nodes[i] for i in range( 0, len( m_nodes )) if m_nodes[i] not in m_result and cmds.nodeType( m_nodes[i] ) not in ignoreType and m_nodes[i] not in ignoreNodes ]
    return m_result
    
def clipPlaneCamera( camera, nodes="", ignoreNodes="", nodeType="", ignoreType="", frameSpacing=1 ):
    m_result = []
    m_nodes = listFromView( camera, nodes=nodes, ignoreNodes=ignoreNodes, nodeType=nodeType, ignoreType=ignoreType, outside=True, animation=True, start=cmds.playbackOptions( query=True, animationStartTime=True ), end=cmds.playbackOptions( query=True, animationEndTime=True ), frameSpacing=frameSpacing, frustum=0, aspect=1 )
    for i in range( 0, len( m_nodes )):
        if cmds.attributeQuery( "visibility", n=m_nodes[i], exists=True ) and not cmds.listConnections( "%s.visibility" % m_nodes[i] ) and cmds.getAttr( "%s.visibility" % m_nodes[i] ) != 0 and not cmds.getAttr( "%s.visibility" % m_nodes[i], lock=True ):
            cmds.setAttr( "%s.visibility" % m_nodes[i], 0 )
            m_result.append( m_nodes[i] )
    return m_result
    
def clipPlaneScene( ignoreNodes="" ):
    m_cache = cmds.ls( type="camera" )
    m_cameras = []
    m_expression = re.compile( "[Ee][Pp][0-9]+(Shape|shape|)[Ss][Cc](Shape|shape|)[0-9]+(Shape|shape|)" )
    for i in range( 0, len( m_cache )):
        if m_expression.findall( m_cache[i] ):
            m_cameras.append( m_cache[i] )
    if m_cameras:
        print "Hide all not visible nodes from camera: %s" % m_cameras[0]
        m_result = clipPlaneCamera( m_cameras[0], ignoreNodes=ignoreNodes, frameSpacing=1, ignoreType=[ "stereoRigCamera", "stereoRigFrustum", "stereoRigTransform", "camera", "ambientLight", "pointLight", "directionalLight", "spotLight", "areaLight", "volumeLight", "RMSGeoAreaLight", "RMSGeoLightBlocker", "RMSAreaLight", "RMSEnvLight", "RMSGILight", "RMSGIPtcLight", "RMSCausticLight", "RMSPointLight" ] )
    else:    
        m_result = None
        print "No camera finded."
    return m_result