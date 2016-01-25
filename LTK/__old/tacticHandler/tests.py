def sel_prnt_trgt_shapes():
    selTransform = cmds.ls(os=True, l=True)
    if selTransform:
        selParent = cmds.listRelatives(selTransform[0], ad=True, f=True, typ='transform')
        selTarget = cmds.listRelatives(selTransform[1:], ad=True, f=True, typ='transform')
        if not selParent:
            selParent = selTransform[0]
        if not selTarget:
            selTarget = selTransform[1:]
        selParentS = cmds.listRelatives(selParent, ad=True, s=True, f=True, ni=True)
        selTargetS = cmds.listRelatives(selTarget, ad=True, s=True, f=True, ni=True)
        return [selParentS, selTargetS]
    else:
        return [0, 0]

print sel_prnt_trgt_shapes()