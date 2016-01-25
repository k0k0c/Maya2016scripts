import maya.cmds as cmds
import os
import re
import sys
import subprocess
import time

def listReferenceLevels( node ):
    """
    List all name levels for current referenced node.
    """
    result = []
    node = node.split( "." )
    attr = ""
    if len( node ) > 1:
        attr = node[-1]
    node = node[0]
    if cmds.nodeType( node ) != "reference" and cmds.referenceQuery( node, isNodeReferenced=True ):
        rfn = cmds.referenceQuery( node, rfn=True )
        mcache = []
        while rfn:
            m_prefixname = cmds.referenceQuery( rfn, filename=True )
            m_prefix = cmds.file( m_prefixname, query=True, renamingPrefix=True )
            m_next = cmds.referenceQuery( rfn, rfn=True, parent=True )
            if m_next:
                filename = cmds.referenceQuery( m_next, filename=True )
            else:
                filename = cmds.file( query=True, sceneName=True )
                filename = filename != "" and filename or "untitled"
            mcache.insert( 0, "(" + m_prefix + "[:_]|)" )
            m_expr = re.compile( "".join( mcache ))
            m_rnode = ""
            for m_part in node.split( "|" ):
                m_temp = m_expr.split( m_part )[0] + mcache[0]
                m_temp = re.split( m_temp, m_part )
                m_temp = "".join( [ namespace for namespace in m_temp if namespace != "" ] )
                if m_temp != "":
                    m_rnode = m_rnode + "|" + m_temp
            result.append( [ m_rnode + attr, filename ] )
            if m_next:
                rfn = m_next
                continue
            else:
                break
    return result

def listReferenceEdits( rfn ):
    """
    List all edits for current reference node.
    """
    result = []
    successfull = []
    if cmds.nodeType( rfn ) == "reference":
        rfn = rfn
    else:
        rfn = cmds.referenceQuery( rfn, rfn=True ) 
    edits = cmds.referenceQuery( rfn, failedEdits=True, successfulEdits=True, editStrings=True )
    if edits:
        edits = [ "".join( [ m_part for m_part in re.split( "\|:[A-z0-9:]+", edits[i] ) if m_part != "" ] ) for i in range( 0, len( edits )) ]
        m_content = cmds.ls( cmds.referenceQuery( rfn, nodes=True, dagPath=True ), long=True )
        for c in range( 0, len( m_content )):
            m_levels = listReferenceLevels( m_content[c] )
            for l in range( 0, len( m_levels )):
                m_expr = re.compile( "(\A|\s|\||\")+([A-z0-9_|]+|){0}(\Z|\s|\$|\"|\.)+".format( "(\||)".join( m_levels[l][0].split( "|" ))))
                for e in range( 0, len( edits )):
                    if edits[e] not in successfull:
                        if m_expr.findall( edits[e] ):
                            m_temp = [ rfn, m_content[c], m_levels[l][-1], m_levels[l][0], edits[e].split( " " )[0], edits[e] ]
                            result.append( m_temp )
                            successfull.append( edits[e] )
        for e in range( 0, len( edits )):
            if edits[e] not in successfull:
                m_temp = [ rfn, "unknown", "unknown", "unknown", edits[e].split( " " )[0], edits[e] ]
                result.append( m_temp )
    return result

def removeEdits( rfn, editStrings ):
    """
    Remove edits strings.
    """
    rfn = type( rfn ) is list and str( rfn[0] ) or str( rfn ) 
    editStrings = type( editStrings ) is list and editStrings or [ editStrings ]
    unloadReference( rfn )
    filename = cmds.referenceQuery( rfn, filename=True )
    m_isdeferred = cmds.file( filename, query=True, deferReference=True )
    #Remove edits.
    for i in range( 0, len( editStrings )):
        string = str( editStrings[i] )
        buffer = string.split( " " )
        #Edit command.
        m_command = buffer[0]
        #Edit node.
        if m_command == "addAttr": 
            node = buffer[-1] + "." + buffer[2] 
        elif m_command == "deleteAttr": 
            node = buffer[1]
        elif m_command == "connectAttr": 
            node = buffer[1]
        elif m_command == "disconnectAttr":
            if m_isdeferred:
                node = buffer[-2]
            else:
                node = buffer[-1]
        elif m_command == "setAttr": 
            node = buffer[1]
        elif m_command == "relationship": 
            node = buffer[2]
        elif m_command == "parent":
            if buffer[-2] == "-w":
                node = buffer[-1]
            else:
                node = buffer[-2]
        if "\"" in node:
            node = node.split( "\"" )[1]
        cmds.referenceEdit( node, failedEdits=True, successfulEdits=True, editCommand=m_command, removeEdits=True )
    cmds.file( loadReference=rfn )
 
def cleanupReference( rfn ):
    #Get reference node.
    if cmds.nodeType( rfn ) == "reference":
        rfn = rfn
    elif os.path.isfile( rfn ):
        rfn = cmds.referenceQuery( rfn, rfn=True )
    else:
        print "%s is not reference" % rfn
        return None
    references = []
    pm = cmds.listConnections( rfn, type="proxyManager" )
    if pm:
        references = cmds.listConnections( "%s.proxyList" % pm[0], type="reference" )
    if not references:
        references = [ rfn ]
        m_words = "|".join( references )
    else:
        references = [ rfn ]
        m_words = rfn
    edits = []
    if references:
        for i in range( 0, len( references )):
            strings = cmds.referenceQuery( references[i], failedEdits=True, successfulEdits=True, editStrings=True )
            if strings:
                for i in range( 0, len( strings )):
                    if strings[i] not in edits:
                        if not re.findall( m_words, strings[i] ):
                            edits.append( strings[i] )
    if edits:
        removeEdits( rfn, edits )

def loadReference( rfn, loadReferenceDepth="", loadCrashedReferences=False ):
    """
    Load existing reference.
    """
    #Get reference node.
    if cmds.nodeType( rfn ) == "reference":
        rfn = rfn
    elif os.path.isfile( rfn ):
        rfn = cmds.referenceQuery( rfn, rfn=True )
    else:
        print "%s is not reference" % rfn
        return None
    #Setup proxyManager.
    pm = cmds.listConnections( rfn, type="proxyManager" )
    references = []
    if pm:
        pm = pm[0]
        mcache = cmds.listConnections( "%s.proxyList" % pm, type="reference", source=False, destination=True )
        for i in range( 0, len( mcache )):
            if mcache[i] not in references:
                references.append( mcache[i] )
        #Unload reference.
        m_count = len( references )
        if m_count > 1:
            for i in range( 0, m_count ):
                unloadReference( references[i] )
        #Setup active references.
        attrs = []
        active = cmds.listConnections( "%s.activeProxy" % pm, plugs=True )
        if active:
            for i in range( 0, len( active )):
                cmds.disconnectAttr( "%s.activeProxy" % pm, active[i] )
                attrs.append( active[i] )
        else:
            active = references[0]
            active = cmds.listConnections( "%s.proxyList" % pm, type="reference", connections=True, plugs=True )
            attrs.append( active[0] )
        activeRfn = cmds.listConnections( attrs, type="reference" )
        #Restore active state.
        if activeRfn:
            for i in range( 0, len( activeRfn )):
                connections = cmds.listConnections( "%s.associatedNode" % activeRfn[i], source=True, connections=True, plugs=True )
                if connections:
                    for c in range( 0, len( connections )):
                        cmds.disconnectAttr( connections[c+1], connections[c] )
                        cmds.connectAttr( connections[c+1], "%s.%s" % ( rfn, connections[c].split( "." )[-1]))
                connections = cmds.connectionInfo( "%s.msg" % activeRfn[i], dfs=True )
                if connections:
                    for c in range( 0, len( connections )):
                        node = connections[c].split( "." )[0]
                        if cmds.nodeType( node ) == "transform":
                            if cmds.isConnected( "%s.msg" % activeRfn[i], "%s.isHistoricallyInteresting" % node ):
                                cmds.disconnectAttr( "%s.msg" % activeRfn[i], "%s.isHistoricallyInteresting" % node )
                                cmds.connectAttr( "%s.msg" % rfn, "%s.isHistoricallyInteresting" % node )
        #Make target reference active.
        cmds.connectAttr( "%s.activeProxy" % pm, cmds.connectionInfo( "%s.proxyMsg" % rfn, sourceFromDestination=True ))
        #Trying to restore applied edits from other connected references.
        if m_count > 1:
            for i in range( 0, m_count ):
                m_previousConnection = cmds.listConnections( "%s.sharedEditsOwner" % pm, source=True, destination=False, plugs=True )
                if m_previousConnection:
                    cmds.disconnectAttr( m_previousConnection[0], "%s.sharedEditsOwner" % pm )
                cmds.connectAttr( "%s.proxyMsg" % references[i], "%s.sharedEditsOwner" % pm )
                print "transfer edits: %s to %s." % ( rfn, references[i] )
                cmds.file( loadReference=rfn, loadReferenceDepth="none" )
    else:
        references = [ rfn ]
    #Load target reference.
    if not cmds.referenceQuery( rfn, isLoaded=True ):
        if loadCrashedReferences is False and ( pm and len( references ) > 1 or not pm ) or loadCrashedReferences is True:
            print "load reference: %s" % rfn 
            if loadReferenceDepth == "":
                cmds.file( loadReference=rfn )
                makeActive( rfn )
            else:
                cmds.file( loadReference=rfn, loadReferenceDepth=loadReferenceDepth )
                makeActive( rfn )
        else:
            print "loading is paused, please check this reference: %s" % rfn
    return references
        
def addReference( rfn, reference ):
    """
    Add proxy to current reference.
    """
    if cmds.nodeType( rfn ) == "reference":
        rfn = rfn
    elif os.path.isfile( rfn ):
        rfn = cmds.referenceQuery( rfn, rfn=True )
    else:
        print "%s is not reference" % rfn
        return None
    #Validate current reference.
    filename = cmds.referenceQuery( rfn, filename=True )
    namespace = cmds.file( filename, query=True, namespace=True )
    parents = cmds.referenceQuery( rfn, parent=True, referenceNode=True )
    if parents:
        print "%s has reference parents, please open first parent if you want to add new proxy reference for current reference." % rfn
        return None
    if cmds.file( filename, query=True, usingNamespaces=True ) is False:
        print "%s is not using namespaces." % rfn
        return None
    #Validate target reference.
    if cmds.objExists( reference ) and cmds.nodeType( reference ) == "reference":
        parents = cmds.referenceQuery( reference, parent=True, referenceNode=True )
        if parents:
            print "%s has reference parents, please open first parent if you want to add new proxy reference for current reference." % reference
            return None
    elif os.path.isfile( reference ):
        if not re.findall( ".ma$|.mb$", reference ):
            print "%s is not maya scene file." % reference
            return None
    else:
        print "%s is not valid reference." % reference
        return None
    #Get current reference proxy manager.
    pm = cmds.listConnections( rfn, type="proxyManager" )
    if pm:
        pm = pm[0]
    else:
        name = cmds.referenceQuery( rfn, filename=True ).split( "/" )[-1].split( "." )[0]
        pm = cmds.createNode( "proxyManager", name=name + "PM" )
        cmds.connectAttr( "%s.activeProxy" % pm, "%s.proxyList[0]" % pm )
        cmds.connectAttr( "%s.proxyList[0]" % pm, "%s.proxyMsg" % rfn )
        cmds.connectAttr( "%s.proxyMsg" % rfn, "%s.sharedEditsOwner" % pm )
    #Get empty proxy attribute.
    pmProxy = "{0}.proxyList[%s]".format( pm )
    pmIndex = 0
    while pmIndex < 1000:
        if cmds.listConnections( pmProxy % pmIndex, type="reference" ):
            pmIndex = pmIndex + 1
            continue
        else:
            pmProxy = pmProxy % pmIndex
            break
    #Load new reference.
    if not cmds.objExists( reference ) and os.path.isfile( reference ):
        reference = cmds.file( reference, reference=True, mergeNamespacesOnClash=True, options="v=0;", namespace=namespace, loadReferenceDepth="none" )
        reference = cmds.referenceQuery( reference, rfn=True )
    else:
        reference = reference
    if cmds.nodeType( reference ) == "reference":
        cmds.connectAttr( pmProxy, "%s.proxyMsg" % reference )
        return reference
    else:
        print "%s is not reference." % reference
        return None

def switchProxy( rfn, to="" ):
    if cmds.nodeType( rfn ) == "reference":
        pm = cmds.listConnections( rfn, type="proxyManager" )
    else:
        print "%s has not any connected proxy references." % rfn
        return None
    if pm:
        pm = pm[0]
        if to == "":
            references = cmds.listConnections( "%s.proxyList" % pm, type="reference", source=False, destination=True )
            active = cmds.listConnections( "%s.activeProxy" % pm, source=False, destination=True, plugs=True )
            if active:
                for i in range( 0, len( references )):
                    connections = cmds.listConnections( "%s.proxyMsg" % references[i], type="proxyManager", source=True, destination=False, plugs=True )
                    if connections and active[0] in connections:
                        return loadReference( references[i-1] )
                        break 
            else:
                return loadReference( references[0] )
        else:
            if cmds.objExists( to ) and cmds.nodeType( to ) == "reference":
                tm = cmds.listConnections( to, type="proxyManager" )
                if tm and pm == tm[0]:
                    return loadReference( to )
                else:
                    print "%s is not proxy reference for current reference." % to
                    return None
            else:
                print "%s is not proxy reference." % to
                return None

def openReference( rfn ):
    """
    Open current reference node in new maya window.
    """
    rfn = type( rfn ) is list and rfn or [ rfn ]
    for i in range( 0, len( rfn )):
        if cmds.nodeType( rfn[i] ) == "reference":
            node = rfn
        elif os.path.isfile( rfn ):
            node = cmds.referenceQuery( rfn[i], rfn=True )
        else:
            print "%s is not reference" % rfn[i]
            return None
        maya = sys.executable
        filename = cmds.referenceQuery( node, filename=True )
        expression = re.compile("^(/Server-3d/Project)|(/mnt/server-3d)|(P:)|(/home/.*/Project)|(D:/Work/Project)|(//Server-3d/Project)", re.IGNORECASE)
        filename = expression.sub("//Server-3d/Project", filename )
        if filename:
            filename = filename.split( "{" )[0]
            m_command = "python(\"import chekProject; chekProject.setMayaProject({0}); import melnik_setup; melnik_setup.updateScene();import maya.cmds as cmds; cmds.file({0}, force=True, open=True )\")".format( "'%s'" % filename )
            subprocess.Popen( [maya, "-command", m_command ])

def removeReference( rfn ):
    if cmds.nodeType( rfn ) == "reference":
        rfn = rfn
    elif os.path.isfile( rfn ):
        rfn = cmds.referenceQuery( rfn, rfn=True )
    else:
        print "%s is not reference" % rfn
        return None
    pm = cmds.listConnections( rfn, type="proxyManager" )
    if pm:
        references = cmds.listConnections( "%s.proxyList" % pm[0], type="reference", source=False, destination=True )
    else:
        references = [ rfn ]
    for i in range( 0, len( references )):
        filename = cmds.referenceQuery( references[i], filename=True )
        cmds.file( filename, removeReference=True )

def unloadReference( rfn ):
    #Get reference node.
    result = []
    if cmds.nodeType( rfn ) == "reference":
        rfn = rfn
    elif os.path.isfile( rfn ):
        rfn = cmds.referenceQuery( rfn, rfn=True )
    else:
        print "%s is not reference" % rfn
        return None
    relatives = referenceRelatives( rfn, onlyLoaded=True, parents=False )
    if cmds.referenceQuery( rfn, isLoaded=True ):
        if relatives:
            for i in range( len( relatives )-1, -1, -1 ):
                parent = cmds.referenceQuery( relatives[i], parent=True, filename=True )
                parent = parent and parent or "untitled"
                pm = cmds.listConnections( relatives[i], type="proxyManager" )
                if pm:
                    mcache = cmds.listConnections( "%s.proxyList" % pm[0], type="reference" )
                else:
                    mcache = [ relatives[i] ]
                for n in range( 0, len( mcache )):
                    if mcache[n] not in result:
                        result.append( mcache[n] )
                        pcache = cmds.referenceQuery( mcache[n], parent=True, filename=True )
                        pcache = pcache and pcache or "untitled"
                        if parent != pcache:
                            print "//Warning:\n//\treference is not valid:\n//\t{0} has parent {1}\n//\t{2} has parent {3}\n//\tplease check reference nodes connections.\n".format( relatives[i], parent, mcache[n], pcache )
                        if cmds.referenceQuery( mcache[n], isLoaded=True ):
                            print "unload reference: %s" % mcache[n]
                            cmds.file( unloadReference=mcache[n] )
    return result

def listReferences( onlyLoaded=False, referenceNodes=False, listUniqueReferences=False ):
    """
    List all currently loaded references in current scene.
    """
    result = []
    references = cmds.file( query=True, reference=True )
    if referenceNodes is True:
        rcache = references
        references = [] 
        for i in range( 0, len( rcache )):
            try:
                references.append( cmds.referenceQuery( rcache[i], rfn=True ))
            except:
                try:
                    print "\nFailed to find reference node by referenceQuery command for %s\nTry file command for request reference node." % rcache[i]
                    references.append( cmds.file( rcache[i], query=True, rfn=True ))
                    print "Result: %s\n" % references[-1]
                except:
                    print "Failed to find reference node by file and referenceQuery command for %s" % rcache[i]
                    continue
    if references:
        while references:
            mcache = []
            for i in range( 0, len( references )):
                if references[i] not in result and ( onlyLoaded is True and cmds.referenceQuery( references[i], isLoaded=True ) or onlyLoaded is not True ):
                    if listUniqueReferences is True and references[i].split( "{" )[0] not in result or listUniqueReferences is False:
                        result.append( references[i] )
                        if referenceNodes is False:
                            childs = cmds.file( references[i], query=True, reference=True )
                        else:
                            childs = cmds.referenceQuery( references[i], child=True, rfn=True )
                        if childs:
                            for n in range( 0, len( childs )):
                                if childs[n] not in result:
                                    mcache.append( childs[n] )
            if mcache:
                references = mcache
            else:
                break
    return result

def validateReferenceState( rfn ):
    """
    Validate reference loaded state.
    """
    isLoad = False
    if cmds.objExists( rfn ) and cmds.nodeType( rfn ) == "reference":
        rfn = rfn 
        if cmds.referenceQuery( rfn, isLoaded=True ):
            pm = cmds.listConnections( rfn, type="proxyManager" )
            if pm:
                mlist = cmds.listConnections( "%s.proxyList" % pm[0], type="reference" )
                active = cmds.listConnections( "%s.activeProxy" % pm[0], plugs=True )
                if mlist:
                    for n in range( 0, len( mlist )):
                        #Validate load state.
                        if mlist[n] != rfn and cmds.referenceQuery( mlist[n], isLoaded=True ):
                            isLoad = True
                            break
                        #Validate active state.
                        if mlist[n] != rfn:
                            for a in range( 0, len( active )):
                                if cmds.isConnected( active[a], "%s.proxyMsg" % mlist[n] ):
                                    isLoad = True
                                    break
                        else:
                            for a in range( 0, len( active )):
                                if not cmds.isConnected( active[a], "%s.proxyMsg" % mlist[n] ):
                                    isLoad = True
                                    break
                        if isLoad is True:
                            break
                        #Validate attribute state.
                        if mlist[n] == rfn and not cmds.isConnected( "%s.proxyMsg" % mlist[n], "%s.sharedEditsOwner" % pm[0] ):
                            isLoad = True
                            break
            else:
                isLoad=True                
        else:
            isLoad=True
    if isLoad is False:
        print "\n%s is not valid reference" % rfn
    return isLoad

def loadReferences( references, unloadUnused=True ):
    """
    Load all user specified references existing in current scene.
    """
    result = []
    #Unload unused references.
    if unloadUnused is True:
        mlist = listReferences( referenceNodes=True )
        for i in range( len( mlist )-1, -1, -1):
            if mlist[i] not in references:
                unloadReference( mlist[i] )
    #Load references.
    for i in range( 0, len( references )):
        if cmds.objExists( references[i] ) and cmds.nodeType( references[i] ) == "reference":
            if references[i] not in result:
                #Validate reference state.
                isLoad=validateReferenceState( references[i] )
                if isLoad is True:
                    mcache = loadReference( references[i], loadReferenceDepth="topOnly" )
                    for n in range( 0, len( mcache )):
                        if mcache[n] not in result: 
                            result.append( mcache[n] )
    return result

def loadContainer( rfn, index=0 ):
    """
    Load reference container with all nested references by proxy index.
    """
    result = []
    mlist =  type( rfn ) is list and rfn or [ rfn ]
    mcache = []
    while mlist:
        m_childrens = []
        for i in range( len( mlist )-1, -1, -1 ):
            if mlist[i] not in mcache and mlist[i] not in result:
                rfn = mlist[i] 
                #Get information about reference.
                pm = cmds.listConnections( mlist[i], type="proxyManager" )
                if pm:
                    references = cmds.listConnections( "%s.proxyList" % pm[0], type="reference" )
                    if references:
                        rfn = references[ index % len( references ) ]
                        mcache = mcache + references
                #Load reference.
                result.append( rfn )
                print "\nLoad container: %s" % rfn
                references = loadReference( rfn, loadReferenceDepth="topOnly" )
                if references:
                    mcache = mcache + references
                #Continue loading.
                if cmds.referenceQuery( rfn, isLoaded=True ):
                    relatives = cmds.referenceQuery( rfn, child=True, rfn=True )
                    if relatives:
                        for n in range( 0, len( relatives )):
                            if relatives[n] not in m_childrens:
                                m_childrens.append( relatives[n] )
        if m_childrens:
            mlist = m_childrens
        else:
            break
    print "result: %s\n" % str( result )
    return result

def makeActive( rfn ):
    """
    Make active all nested references.
    """
    result = []
    references = referenceRelatives( rfn, onlyLoaded=False, parents=False )
    if references:
        m_count = len( references )
        if m_count > 1:
            for i in range( 0, m_count ):
                if references[i] not in result:
                    result.append( references[i] )
                    pm = cmds.listConnections( "%s.proxyMsg" % references[i], type="proxyManager" )
                    if pm:
                        pm = pm[0]
                        #Get active reference.
                        rfn = ""
                        proxy = cmds.listConnections( "%s.proxyList" % pm, type="reference", source=False, destination=True )
                        if proxy:
                            for n in range( 0, len( proxy )):
                                if cmds.referenceQuery( proxy[n], isLoaded=True ):
                                    rfn = proxy[n]
                                    break
                        if rfn == "":
                            rfn = proxy[0]
                        #Deactivate all non active references.
                        active = cmds.listConnections( "%s.activeProxy" % pm, plugs=True )
                        if active:
                            for n in range( 0, len( active )):
                                cmds.disconnectAttr( "%s.activeProxy" % pm, active[n] )
                        #Make active reference.
                        lproxy = cmds.connectionInfo( "%s.proxyMsg" % rfn, sourceFromDestination=True )
                        if lproxy:
                            cmds.connectAttr( "%s.activeProxy" % pm, lproxy )
    return result

def listReferenceContentAssemblies():
    """
    List assemblies transforms from all loaded references.
    """
    def listReferenceContentAssemblies_exec( reference ):
        reference_short = reference.split( "{" )[0]
        transforms = []
        if reference == sceneName:
            nodes = cmds.ls( long=True, assemblies=True )
            if nodes:
                for i in range( 0, len( nodes )):
                    if not cmds.referenceQuery( nodes[i], isNodeReferenced=True ):
                        transforms.append( nodes[i] )
        else:
            nodes = cmds.ls( cmds.referenceQuery( reference, nodes=True, dagPath=True ), long=True, type="transform", ni=True )
            for i in range( 0, len( nodes )):
                parent = cmds.listRelatives( nodes[i], parent=True, fullPath=True )
                if ( parent and ( cmds.referenceQuery( parent, isNodeReferenced=True ) and cmds.referenceQuery( parent, filename=True ) != reference ) or ( parent and not cmds.referenceQuery( parent, isNodeReferenced=True ))) or not parent:
                    transforms.append( nodes[i] )
        result_keys = result.keys()
        if reference_short not in result_keys:
            result.update( { reference_short:transforms } )
    result = {}
    sceneName = cmds.file( query=True, sceneName=True )
    references = listReferences( onlyLoaded=True )
    references.append( sceneName )
    for i in range( 0, len( references )):
        listReferenceContentAssemblies_exec( references[i] )
    return result
    
def referenceRelatives( rfn, onlyLoaded=False, parents=False ):
    """
    List all currently loaded references in current scene.
    """
    result = []
    references = [ rfn ]
    if references:
        while references:
            mcache = []
            for i in range( 0, len( references )):
                if references[i] not in result and ( onlyLoaded is True and cmds.referenceQuery( references[i], isLoaded=True ) or onlyLoaded is not True ):
                    result.append( references[i] )
                    if parents is False:
                        relatives = cmds.referenceQuery( references[i], child=True, rfn=True )
                    else:
                        relatives = cmds.referenceQuery( references[i], parent=True, rfn=True )
                    if relatives:
                        relatives = type( relatives ) is not list and [ relatives ] or relatives
                        for n in range( 0, len( relatives )):
                            if relatives[n] not in result:
                                mcache.append( relatives[n] )
            if mcache:
                references = mcache
            else:
                break
    return result

def findReference( path="", expression="", force=False, dialog=False ):
    """
    List similar files for current file .
    """
    result = ""
    if os.path.isfile( path ):
        filename = path.split( "/" )
        directory = "/".join( filename[0:-1] ) + "/"
        filename = filename[-1].split( "." )[0]
        files = os.listdir( directory )
        expression = re.compile( expression, re.IGNORECASE )
        if expression.findall( filename ):
            ignore = True
        else:
            ignore = False
        for i in range( 0, len( files )):
            if re.findall( ".ma|.mb", files[i] ):
                mfiletemp = files[i].split( "/" )[-1].split( "." )[0]
                if filename != mfiletemp:
                    if ignore is True:
                        if mfiletemp == expression.sub( "", filename ):
                            return os.path.join( directory, files[i] )
                    else:
                        if filename == expression.sub( "", mfiletemp ):
                            return os.path.join( directory, files[i] )
        if result != "" and force is True and dialog is False:
            result = cmds.fileDialog2( caption="Reference", fileFilter="Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)", startingDirectory=directory, fileMode=1 )
        elif dialog is True:
            result = cmds.fileDialog2( caption="Reference", fileFilter="Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)", startingDirectory=directory, fileMode=1 )
        if result:
            result = result[-1]
    return result

def makeReferenceSet( node, name="", fromFile="" ):
    """
    Save current loaded references list.
    """
    name = name != "" and "_" + name or ""
    attributes = listReferenceSets( node )
    version = re.compile( "ver([0-9]+)" )
    msets = []
    #Get reference sets data.
    if fromFile != "":
        mfile = file( fromFile, "r" )
        msets = mfile.read()
        msets = msets.split( "\n" )
    else:
        references = listReferences( onlyLoaded=True, referenceNodes=True )
        if references:
            msets = [ "|".join( references ) ]
    #Make new reference sets
    if msets:
        referenceSets = []
        index = 0
        for s in range( 0, len( msets )):
            if msets[s] != "":
                if attributes:
                    mlast = []
                    for a in range( 0, len( attributes )):
                        current = version.findall( attributes[a] )
                        if current:
                            mlast.append( current[0] )
                    if mlast:
                        index = index + 1
                        mlast = str( int( max( mlast )) + index )
                        mlast = "0" * ( 3 - len( mlast)) + mlast
                        attrName = "referenceSet_ver" + mlast + name
                        cmds.addAttr( node, longName=attrName, dt="string" )
                        cmds.setAttr( "%s.%s" % ( node, attrName ), msets[s], type="string" )
                        referenceSets.append( attrName )
                    else:
                        print "%s is not valid." % node
                        return None
                else:
                    attrName = "referenceSet_ver000" + name
                    cmds.addAttr( node, longName=attrName, dt="string" )
                    cmds.setAttr( "%s.%s" % ( node, attrName ), msets[s], type="string" )
                    referenceSets.append( attrName )
        return referenceSets
    return None

def listReferenceSets( node ):
    """
    List all reference sets in current scene.
    """
    mcache = cmds.listAttr( node )
    result = []
    base = re.compile( "referenceSet_ver[0-9]+" )
    for i in range( 0, len( mcache )):
            if base.findall( mcache[i] ):
                result.append( mcache[i] )
    return result

def readReferenceSet( node, attribute ):
    """
    Read references list from reference set.
    """
    if "referenceSet_" not in attribute:
        attribute = "referenceSet_" + attribute
    else:
        attribute = str( attribute )
    if cmds.attributeQuery( attribute, n=node, exists=True ):
        value = cmds.getAttr( "%s.%s" % ( node, attribute ))
    else:
        print "%s has not attribute %s." % ( node, attribute )
        value = ""
    value = value.split( "|" )
    return value
        
def removeReferenceSet( node, attribute ):
    """
    Remove reference set.
    """
    if "referenceSet_" not in attribute:
        attribute = "referenceSet_" + attribute
    else:
        attribute = attribute
    if cmds.attributeQuery( attribute, n=node, exists=True ):
        cmds.deleteAttr( "%s.%s" % ( node, attribute ))
        return "%s.%s" % ( node, attribute )
    else:
        print "%s has not attribute %s." % ( node, attribute )
        return None
    
def exportReferenceSet( node, path ):
    """
    Export reference sets to file.
    """
    msets = listReferenceSets( node )
    if msets:
        mfile = file( path, "w" )
        string = ""
        for i in range( 0, len( msets )):
            value = readReferenceSet( node, msets[i] )
            if value:
                string = ( i != 0 and "\n" or "" ) + "|".join( value )
                mfile.write( string )
        mfile.close()
    else:
        print "No reference sets to export"
        return None
    
class log():
    def __init__( self, path ):
        self.create( path )
        
    def create( self, path ):
        self.path = path.split( "." )[0] + ".log"
        self.text = file( self.path, "w" )
        self.string = "{0}-|-{1}".format( self.time(), self.path )
        self.text.write( self.string )
        self.text.close()
        
    def write( self, string, debug=False ):
        try:
            if os.path.isfile( self.path ):
                self.text = file( self.path, "a" )
                self.string = "\n{0}-|-{1}".format( self.time(), str( string ))
                if debug is True:
                    print self.string
                self.text.write( self.string )
                self.text.close()
        except:
            print "Failed to write log: %s" % self.path
            
    def time( self ):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    
    def read( self ):
        try:
            self.text = file( self.path, "r" )
            self.result = self.text.read()
            self.text.close()
            return self.result 
        except:
            print "Failed to read log: %s" % self.path
            return None
        
    def remove( self ):
        try:
            os.remove( self.path )
            self = ""
        except:
            print "Failed to remove log: %s" % self.path