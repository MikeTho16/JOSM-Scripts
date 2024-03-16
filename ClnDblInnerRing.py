# ClnDblInnerRing - Clean Double Inner Ring. Fixes the case where the inner ring of a multipolygon has the
# same position as another way.
#
# * Select two closed ways that share the same position.
#   * Hint, in JOSM with one way selected, alt-shift click to select the second.
# * One (way1) must be the inner ring of a multipolygon, and must not have any tags
# * The other (way2) must not be a member of any relation, but may have tags
# * Run this script
# * The script copies the tags from way2 to way1 and deletes way2
#
# Reference:
# https://josm.openstreetmap.de/doc/overview-summary.html

import math
import sys
from javax.swing import JOptionPane
from org.openstreetmap.josm.tools import Geometry
from org.openstreetmap.josm.data.osm import QuadBuckets
from org.openstreetmap.josm.data.osm.visitor import MergeSourceBuildingVisitor
from org.openstreetmap.josm.gui import MainApplication
from org.openstreetmap.josm.data.osm import OsmPrimitiveType

def nodes_equal(node1, node2):
    if abs(node1.lon() - node2.lon()) > 0.000000001:
        return False
    if abs(node1.lat() - node2.lat()) > 0.000000001:
        return False
    return True

def ways_share_same_nodes(way1, way2):
    nodes_count_1 = way1.getNodesCount()
    nodes_count_2 = way2.getNodesCount()
    if nodes_count_1 != nodes_count_2:
        #JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'Node count of ways not equal')
        return False
    # Find out which node, if any, in the second way matches the first node of the first way
    node0_way1 = way1.getNode(0)
    offset = -1
    for node_idx in range(nodes_count_1):
        if node0_way1 is way2.getNode(node_idx):
            offset = node_idx
            break
    if offset == -1:
        #JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'couldnt find start node')
        return False
    # See if the nodes of the ways are ordered in the same direction...
    equal = True
    for node_idx in range(nodes_count_1):
        node_idx2 = node_idx + offset
        # Check if the node_idx2 index has wrapped around. Need to add "1" because in a closed
        # way the first and last nodes are the same.
        if node_idx2 >= nodes_count_1:
            node_idx2 = node_idx2 - nodes_count_1 + 1
        #JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'idx1={}, idx2={}'.format(node_idx, node_idx2))
        if way1.getNode(node_idx) is not way2.getNode(node_idx2):
            equal = False
            break
    if equal:
        return True
    # See if the nodes of the ways are ordered in opposite directions...
    for node_idx in range(nodes_count_1):
        node_idx2 = -node_idx + offset
        # Check if node_idx2 has wrapped around. Need to subtract "1" because in a closed way
        # the first and last nodes are the same
        if node_idx2 < 0:
            node_idx2 = node_idx2 + nodes_count_1 - 1
        #JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'idx1={}, idx2={}'.format(node_idx, node_idx2))     
        if way1.getNode(node_idx) is not way2.getNode(node_idx2):
            return False
    return True

def ways_equal(way1, way2):
    nodes_count_1 = way1.getNodesCount()
    nodes_count_2 = way2.getNodesCount()
    if nodes_count_1 != nodes_count_2:
        #JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'Node count of ways not equal')
        return False
    # Find out which node, if any, in the second way matches the first node of the first way
    node0_way1 = way1.getNode(0)
    offset = -1
    for node_idx in range(nodes_count_1):
        if nodes_equal(node0_way1, way2.getNode(node_idx)):
            offset = node_idx
            break
    if offset == -1:
        #JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'couldnt find start node')
        return False
    # See if the nodes of the ways are ordered in the same direction...
    equal = True
    for node_idx in range(nodes_count_1):
        node_idx2 = node_idx + offset
        if node_idx2 >= nodes_count_1:
            node_idx2 = node_idx2 - nodes_count_1 + 1
        #JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'idx1={}, idx2={}'.format(node_idx, node_idx2))     
        if not nodes_equal(way1.getNode(node_idx), way2.getNode(node_idx2)):
            equal = False
            break
    if equal:
        return True
    # See if the nodes of the ways are ordered in opposite directions...
    for node_idx in range(nodes_count_1):
        node_idx2 = -node_idx + offset
        if node_idx2 < 0:
            node_idx2 = node_idx2 + nodes_count_1 - 1
        #JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'idx1={}, idx2={}'.format(node_idx, node_idx2))     
        if not nodes_equal(way1.getNode(node_idx), way2.getNode(node_idx2)):
            return False
    return True

def nodes_have_other_referers(way):
    for node in way.getNodes():
        if len(node.getReferers()) > 1:
            return False

def fix(tgt_way, src_way):
    tgt_way.setKeys(src_way.getKeys())
    src_way.setDeleted(True)
    for node in src_way.getNodes():
        if not node.isReferredByWays(1) and not node.isTagged():
            node.setDeleted(True)
def main():
    active_dataset = MainApplication.getLayerManager().getActiveDataSet()
    selected_ways = list(active_dataset.getSelectedWays())
    if len(selected_ways) != 2:
        msg = 'You must select two, and only two, ways'
        JOptionPane.showMessageDialog(MainApplication.getMainFrame(), msg)
        return
    way1 = selected_ways[0]
    way2 = selected_ways[1]
    if not (way1.isClosed() and way2.isClosed()):
        JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'Both selected ways must be closed')
        return
    if not ways_equal(way1, way2):
        msg = 'Selected ways are not equal'
        JOptionPane.showMessageDialog(MainApplication.getMainFrame(), msg)
        return
    rels1 = way1.getParentRelations((way1,))
    rels2 = way2.getParentRelations((way2,))
    if len(rels1) == 1 and len(rels2) == 0 and not way1.hasKeys():
        if not ways_share_same_nodes(way1, way2) and nodes_have_other_referers(way2):
            msg = ("At least one node in the way that is not a member of the multipolygon has "
                   "another referrer. Can't fix")
            JOptionPane.showMessageDialog(MainApplication.getMainFrame(), msg)
            return
        fix(way1, way2)
    elif len(rels2) == 1 and len(rels1) == 0 and not way2.hasKeys():
        if not ways_share_same_nodes(way1, way2) and nodes_have_other_referers(way1):
            msg = ("At least one node in the way that is not a member of the multipolygon has "
                   "another referrer. Can't fix")
            JOptionPane.showMessageDialog(MainApplication.getMainFrame(), msg)
            return
        fix(way2, way1)
    else:
        msg = ('One way must be a member of a relation and must not have tags, the other way '
               'must not be a member of a relation')
        JOptionPane.showMessageDialog(MainApplication.getMainFrame(), msg)

main()            
