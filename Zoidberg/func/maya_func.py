from maya import cmds as cmds


class MayaFoo(object):
    def __init__(self):
        self.parents = []
        self.targets = []
        self.found_matches = {}
        self.non_found_parent = []
        self.non_found_target = []
        self.sel = cmds.ls(os=True, l=True)

    def selected_prnt_trgt_nodes(self):
        if len(self.sel) > 0:
            self.parents = cmds.listRelatives(cmds.listRelatives(self.sel[0], ad=True, f=True, pa=True) +
                                              self.sel[:1],
                                              s=True, f=True, ni=True)
            self.targets = cmds.listRelatives(cmds.listRelatives(self.sel[1:], ad=True, f=True, pa=True) +
                                              self.sel[1:],
                                              s=True, f=True, ni=True)
        return self.parents, self.targets

    def check_name_match(self, parents=None, targets=None, topology=None):
        target_events_list = {}
        for parent in parents:
            parent_name = parent.split('|')[-1].split(':')[-1]
            copy_event_parent = False
            target_match = []
            for target in targets:
                copy_event_target = False
                target_name = target.split('|')[-1].split(':')[-1]
                if parent_name == target_name:
                    if cmds.nodeType(parent) == cmds.nodeType(target) == 'mesh':
                        tp = [parent]
                        tt = [target]
                        topocheck = self.check_topology_match(parents=tp, targets=tt, globout=False)
                        if parent in topocheck and target in topocheck[parent]:
                            target_match.append(target)
                            self.found_matches[parent] = target_match
                            copy_event_target = True
                    else:
                        target_match.append(target)
                        self.found_matches[parent] = target_match
                        copy_event_target = True
                if not copy_event_target and target_events_list.get(target) != True:
                    target_events_list[target] = False
                if copy_event_target:
                    target_events_list[target] = True
                    copy_event_parent = True
            if not copy_event_parent:
                self.non_found_parent.append(parent)
        for target in target_events_list:
            if not target_events_list[target]:
                self.non_found_target.append(target)
        self.non_found_target = list(set(self.non_found_target))
        self.non_found_parent = list(set(self.non_found_parent))
        return self.found_matches, self.non_found_parent, self.non_found_target

    def check_topology_match(self, parents=None, targets=None, globout=False):
        if parents is None and targets is None:
            parents, targets = self.selected_prnt_trgt_nodes()
        match = {}
        parents_nf = list(self.non_found_parent)
        targets_nf = list(self.non_found_target)
        target_events_list = {}
        target_match_list = []
        for prnt in parents:
            copy_event_parent = False
            parent_target_match = []
            for trgt in targets:
                copy_event_target = False
                if cmds.nodeType(prnt) == cmds.nodeType(trgt) == 'mesh':
                    tp = cmds.polyEvaluate(prnt, v=True, e=True, f=True, t=True, s=True)
                    tt = cmds.polyEvaluate(trgt, v=True, e=True, f=True, t=True, s=True)
                    if tp == tt and trgt not in target_match_list:
                        copy_event_target = True
                        target_match_list.append(trgt)
                        parent_target_match.append(trgt)
                        parent_target_match = list(set(parent_target_match))
                        if globout:
                            self.found_matches[prnt] = parent_target_match
                        else:
                            match[prnt] = parent_target_match
                if not copy_event_target and target_events_list.get(trgt) != True:
                    target_events_list[trgt] = False
                if copy_event_target:
                    target_events_list[trgt] = True
                    copy_event_parent = True
            if not copy_event_parent:
                parents_nf.append(prnt)
            if copy_event_parent and prnt in parents_nf:
                parents_nf.remove(prnt)
        for target in target_events_list:
            if not target_events_list[target]:
                targets_nf.append(target)
            if target_events_list[target] and target in targets_nf:
                targets_nf.remove(target)
        if globout:
            self.non_found_parent = parents_nf
            self.non_found_target = targets_nf
            return self.found_matches, self.non_found_parent, self.non_found_target
        else:
            return match

    def find_match(self,
                   shapename=None,
                   topology=None,
                   sets=None,
                   colorsets=None,
                   unlock=None):
        sel = self.selected_prnt_trgt_nodes()
        fparent = []
        ftarget = []
        if self.parents:
            if unlock:
                self.unlock_attr(nodes=cmds.listRelatives(self.sel, ad=True, f=True))
            if colorsets:
                self.delete_colorsets(nodes=self.targets + self.parents)
            if shapename:
                self.check_name_match(self.parents, self.targets)
            if topology:
                if shapename:
                    self.check_topology_match(self.non_found_parent, self.non_found_target, globout=True)
                else:
                    self.check_topology_match(globout=True)
            if not topology and not shapename:
                self.found_matches[sel[0][0]] = sel[1]
            if sets:
                for i in self.found_matches:
                    fparent.append(i)
                    ftarget.extend(self.found_matches[i])
                self.create_sets(parentnf=self.non_found_parent,
                                 targetnf=self.non_found_target,
                                 parentf=fparent,
                                 targetf=ftarget)
        return self.found_matches

    def create_sets(self, parentnf=None, targetnf=None, parentf=None, targetf=None):
        nf_parent_set = 'nonFoundParent_set'
        nf_target_set = 'nonFoundTarget_set'
        f_parent_set = 'foundParent_set'
        f_target_set = 'foundTarget_set'
        if parentnf:
            if cmds.objExists(nf_parent_set):
                cmds.delete(nf_parent_set)
            cmds.sets(cmds.listRelatives(parentnf, p=True, f=True), n=nf_parent_set)
        if targetnf:
            if cmds.objExists(nf_target_set):
                cmds.delete(nf_target_set)
            cmds.sets(cmds.listRelatives(targetnf, p=True, f=True), n=nf_target_set)
        if parentf:
            if cmds.objExists(f_parent_set):
                cmds.delete(f_parent_set)
            cmds.sets(cmds.listRelatives(parentf, p=True, f=True), n=f_parent_set)
        if targetf:
            if cmds.objExists(f_target_set):
                cmds.delete(f_target_set)
            cmds.sets(cmds.listRelatives(targetf, p=True, f=True), n=f_target_set)

    def unlock_attr(self, nodes=None):
        if nodes:
            for node in nodes:
                attrlist = cmds.listAttr(node, k=True, l=True)
                if attrlist:
                    for attr in attrlist:
                        cmds.setAttr('%s.%s' % (node, attr), l=False)

    def delete_colorsets(self, nodes=None):
        if nodes:
            for node in nodes:
                colorsets = cmds.polyColorSet(node, query=True, acs=True)
                if colorsets:
                    for cset in colorsets:
                        cmds.polyColorSet(node, d=True, cs=cset)
        else:
            cmds.polyColorSet(d=True, acs=True)

    def transfer_uv(self, parent=None, target=None):
        '''
        transfer UV from parent to target
        '''
        if cmds.nodeType(parent) == cmds.nodeType(target) == 'mesh':
            cmds.transferAttributes(parent, target,
                                    transferUVs=1, transferColors=0, searchMethod=3,
                                    sampleSpace=5, flipUVs=0, transferPositions=0,
                                    transferNormals=0, colorBorders=0)

    def transfer_get_attr(self, userattr=None, parent=None):
        '''
        get attributes data list from parent
        '''
        attrlist = []
        for attr_name in userattr:
            nodetype = cmds.nodeType(parent)
            checkrendershape = cmds.getAttr(parent + '.intermediateObject')
            if checkrendershape != 1 or nodetype != 'mesh':
                attr_type = cmds.getAttr("%s.%s" % (parent, attr_name), typ=True)
                attr_enum = cmds.attributeQuery(attr_name, n=parent, le=True)
                attr_value = cmds.getAttr("%s.%s" % (parent, attr_name))
                attr_parent = cmds.attributeQuery(attr_name, n=parent, lp=True)
                attr_children = cmds.attributeQuery(attr_name, n=parent, nc=True)
                attrlist.append([attr_name, attr_type, attr_value, attr_parent, attr_children, attr_enum])
        return attrlist

    def transfer_add_attr(self, attrlist=None, target=None):
        '''
        add atributes on target from attrlist
        '''
        for i in range(len(attrlist)):
            attr_name = attrlist[i][0]
            attr_type = attrlist[i][1]
            try:
                attr_parent = str(attrlist[i][3][0])
            except:
                attr_parent = None
            attr_children = attrlist[i][4]
            if attr_type == 'enum':
                attr_enum = attrlist[i][5][0]
            if not cmds.attributeQuery(attr_name, node=target, ex=True):
                if attr_children:
                    cmds.addAttr(target, ln=attr_name, at=attr_type)
                    continue
                if attr_parent:
                    cmds.addAttr(target, ln=attr_name, at=attr_type, p=attr_parent)
                    continue
                if attr_type == 'string':
                    cmds.addAttr(target, ln=attr_name, dataType=attr_type)
                elif attr_type == 'enum':
                    cmds.addAttr(target, ln=attr_name, at=attr_type, en=attr_enum)
                else:
                    cmds.addAttr(target, ln=attr_name, at=attr_type)

    def transfer_set_attr(self, attrlist=None, target=None):
        '''
        set attributes values on target from attrlist
        '''
        for i in range(len(attrlist)):
            attr_name = attrlist[i][0]
            attr_type = attrlist[i][1]
            attr_value = attrlist[i][2]
            attr_children = attrlist[i][4]
            if cmds.attributeQuery(attr_name, node=target, ex=True):
                if attr_children:
                    continue
                if attr_type == 'string':
                    cmds.setAttr("%s.%s" % (target, attr_name), attr_value, type=attr_type)
                else:
                    cmds.setAttr("%s.%s" % (target, attr_name), attr_value)

    def delete_history(self, parent=None, target=None):
        cmds.delete((parent, target), ch=True)

    def transfer(self, shapename=None, topology=None, atr=None, uv=None, sets=None, history=None, colorsets=None,
                 unlock=None):
        match_list = self.find_match(shapename=shapename, topology=topology, sets=sets, colorsets=colorsets,
                                     unlock=unlock)
        if match_list:
            for parent in match_list:
                userattr = cmds.listAttr(parent, ud=True)
                targets = match_list[parent]
                for target in targets:
                    # transfer UV from parent to target
                    if uv:
                        self.transfer_uv(parent=parent, target=target)
                    # delete history for parent and target
                    if history:
                        cmds.delete((parent, target), ch=True)
                    # get attributes data list from parent
                    if userattr and atr == True:
                        attrlist = self.transfer_get_attr(userattr=userattr, parent=parent)
                        # add atributes on target from attrlist
                        self.transfer_add_attr(attrlist=attrlist, target=target)
                        # set attributes values on target from attrlist
                        self.transfer_set_attr(attrlist=attrlist, target=target)
        else:
            cmds.warning("No matching objects found!")

    @staticmethod
    def delete_user_attr(nodelist=None, attrlist=None):
        """
        Delete all user attrs
        """
        if not nodelist and not attrlist:
            selCur = cmds.ls(sl=True, l=True)
            selCurH = cmds.listRelatives(ad=True, f=True)
            nodelist = selCur + selCurH
        for node in nodelist:
            attrlist = cmds.listAttr(node, ud=True)
            if attrlist:
                for attr in attrlist:
                    connectionList = cmds.listConnections(node + '.' + attr, p=True)
                    if cmds.getAttr("%s.%s" % (node, attr), l=True):
                        cmds.setAttr("%s.%s" % (node, attr), l=False)
                    elif connectionList:
                        for con in connectionList:
                            try:
                                cmds.disconnectAttr((node + '.' + attr), con)
                            except:
                                cmds.disconnectAttr(con, (node + '.' + attr))
                    cmds.deleteAttr(node, at=attr)

    @staticmethod
    def select_node_by_attr(attr, nodelist=None):
        """
        Select node by attr and value
        select_node_by_attr(attr = {'visibility':0, 'intermediateObject':1})
        """
        if not nodelist:
            selCur = cmds.ls(sl=True, l=True)
            selCurH = cmds.listRelatives(ad=True, f=True)
            nodelist = selCur + selCurH
        cmds.select(cl=True)
        for node in nodelist:
            for key in attr:
                if cmds.attributeQuery(key, node=node, ex=True):
                    attrValueCur = cmds.getAttr(node + '.' + key)
                    if attrValueCur == attr[key]:
                        cmds.select(node, add=True)