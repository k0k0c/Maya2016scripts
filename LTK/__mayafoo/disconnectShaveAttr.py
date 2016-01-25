import maya.cmds as cmds


def disconnect_shave_attr(node):
    if node:
        shave_shape_node = cmds.listRelatives(node, ad=True, f=True, type="shaveHair")
        shave_attr_list = ['hairCount', 'hairSegments', 'rootThickness', 'tipThickness', 'randScale']
        if shave_shape_node:
            for shape in shave_shape_node:
                for attr in shave_attr_list:
                    connection_list = cmds.listConnections(shape + '.' + attr, p=True)
                    if connection_list:
                        for connect in connection_list:
                            cmds.disconnectAttr(connect, (shape + '.' + attr))
        else:
            cmds.warning('Shave not found!')
    else:
        cmds.warning('Select transform with shave before run script!')


disconnect_shave_attr(cmds.ls(sl=True))
