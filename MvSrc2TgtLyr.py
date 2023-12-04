# MergeSrc2TgtLyr - Merge Source to Target Layer
#
# * Merges the selected selected OSM elements in the "source" layer to the "target"
#   layer.
# * Makes the "target" layer visible.
# * Makes the "source" layer not visible.
# * Makes the "target" layer active
# * Selects the features in the "target" layer that were just merged

import math
from javax.swing import JOptionPane
from org.openstreetmap.josm.tools import Geometry
from org.openstreetmap.josm.data.osm import QuadBuckets
from org.openstreetmap.josm.data.osm.visitor import MergeSourceBuildingVisitor
from org.openstreetmap.josm.gui import MainApplication
from org.openstreetmap.josm.data.osm import OsmPrimitiveType

def nodes_equal(node1, node2):
    if node1.lon() != node2.lon():
        return False
    if node1.lat() != node2.lat():
        return False
    return True
    
def ways_equal(way1, way2):
    nodes_count_1 = way1.getNodesCount()
    nodes_count_2 = way2.getNodesCount()
    if nodes_count_1 != nodes_count_2:
        return False
    for node_idx in range(nodes_count_1):
        if not nodes_equal(way1.getNode(node_idx), way2.getNode(node_idx)):
            return False
    return True

def relations_equal(rel1, rel2):
    members_count_1 = rel1.getMembersCount()
    members_count_2 = rel2.getMemberssCount()
    if members_count_1 != members_count_2:
        return False
    for member_idx in range(member_count_1):
        mbr1 = rel1.getMember(member_idx)
        mbr2 = rel2.getMember(member_idx)
        if mbr1.getType() != mbr2.getType():
            return False
        if mbr1.getType() == OsmPrimitiveType.NODE:
            if not nodes_equal(mbr1, mbr2):
                return False
        if mbr1.getType() == OsmPrimitiveType.WAY:
            if not ways_equal(mbr1, mbr2):
                return False
        if mbr1.getType() == OsmPrimitiveType.RELATION:
            if not relations_equal(mbr1, mbr2):
                return False
    return True
    
source_layer = None
target_layer = None
for layer in MainApplication.getLayerManager().getLayers():
    print(layer.getName())
    if layer.getName() == 'source':
        source_layer = layer
    if layer.getName() == 'target':
        target_layer = layer

msg = None
if source_layer is None and target_layer is None:
    msg = 'Neither source nor target layers found'
elif source_layer is None:
    msg = 'Source layer not found'
elif target_layer is None:
    msg = 'Target layer not found'
if msg:
    msg = msg + '\nYou must have a layers named "source" and "target"'
    JOptionPane.showMessageDialog(MainApplication.getMainFrame(), msg)
else:
        
    source_dataset = source_layer.getDataSet()
    target_dataset = target_layer.getDataSet()
    target_dataset.clearSelection()
     
    builder = MergeSourceBuildingVisitor(source_dataset)
    target_dataset.mergeFrom(builder.build());
    source_layer.setVisible(False)
    MainApplication.getLayerManager().setActiveLayer(target_layer)
    target_layer.setVisible(True)
     
    # Select the nodes that were explicitly merged
    for target_node in target_dataset.getNodes():
        if target_node.isNew():
            for source_node in source_dataset.getSelectedNodes():
                if nodes_equal(target_node, source_node):
                    target_dataset.addSelected(target_node)
     
    # Select the ways that were merged
    for target_way in target_dataset.getWays():
        if target_way.isNew():
            for source_way in source_dataset.getSelectedWays():
                if ways_equal(target_way, source_way):
                    target_dataset.addSelected(target_way)
            
     
    # Select the relations that were merged
    for target_rel in target_dataset.getRelations():
        if target_rel.isNew():
            for source_rel in source_dataset.getSelectedRelations():
                if relations_equal(target_rel, source_rel):
                    target_dataset.addSelected(target_rel)
                    
    for osm_primitive in source_dataset.getSelected():
        #source_dataset.deleteWay(osm_primitive)
        osm_primitive.setNodes(None)
        osm_primitive.setDeleted(True);
        #for node in osm_primitive.getNodes():
        #    if not node.isReferredByWays(1) and not node.isTagged():
        #        node.setDeleted(True)
    
