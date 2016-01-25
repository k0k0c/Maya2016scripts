import maya.cmds as cmds

selectionList = ['eyesMouthRender_geo']
selectionListOne = ('eyesMouthRender_geoShape')
cmds.select (selectionListOne)
cmds.addAttr (shortName='rman__torattr___preShapeScript', longName='rman__torattr___preShapeScript',dataType="string")
cmds.setAttr ('eyesMouthRender_geoShape.rman__torattr___preShapeScript',"sendMatrix(\"coordsys\");sendMatrix(\"coordsys2\");sendMatrix(\"coordsys3\");sendMatrix(\"coordsys4\");",type="string")

l_eyeProj = 'l_eye_3dTex_coordsys'
r_eyeProj = 'r_eye_3dTex_coordsys'
lo_teeth = 'lo_teeth_3dTex_coordsys'
up_teeth = 'up_teeth_3dTex_coordsys'



#make coordsys for eyesMouthRender_geo

coordsys = cmds.group( empty = True, name = 'coordsys' )

parentCnstr = cmds.parentConstraint( l_eyeProj, coordsys, maintainOffset = False)
scaleCnstr = cmds.scaleConstraint( l_eyeProj, coordsys, maintainOffset = False)

cmds.delete( parentCnstr, scaleCnstr )

cmds.parent( coordsys, selectionList )

cmds.parentConstraint( l_eyeProj, coordsys, maintainOffset = False)

#make coordsys2 for eyesMouthRender_geo 

coordsys2 = cmds.group( empty = True, name = 'coordsys2' )

parentCnstr = cmds.parentConstraint( r_eyeProj, coordsys2, maintainOffset = False)
scaleCnstr = cmds.scaleConstraint( r_eyeProj, coordsys2, maintainOffset = False)

cmds.delete( parentCnstr, scaleCnstr )

cmds.parent( coordsys2, selectionList )

cmds.parentConstraint( r_eyeProj, coordsys2, maintainOffset = False)

#make coordsys3 for eyesMouthRender_geo 

coordsys3 = cmds.group( empty = True, name = 'coordsys3' )

parentCnstr = cmds.parentConstraint( lo_teeth, coordsys3, maintainOffset = False)
scaleCnstr = cmds.scaleConstraint( lo_teeth, coordsys3, maintainOffset = False)

cmds.delete( parentCnstr, scaleCnstr )

cmds.parent( coordsys3, selectionList )

cmds.parentConstraint( lo_teeth, coordsys3, maintainOffset = False)

#make coordsys4 for eyesMouthRender_geo 

coordsys4 = cmds.group( empty = True, name = 'coordsys4' )

parentCnstr = cmds.parentConstraint( up_teeth, coordsys4, maintainOffset = False)
scaleCnstr = cmds.scaleConstraint( up_teeth, coordsys4, maintainOffset = False)

cmds.delete( parentCnstr, scaleCnstr )

cmds.parent( coordsys4, selectionList )

cmds.parentConstraint( up_teeth, coordsys4, maintainOffset = False)
