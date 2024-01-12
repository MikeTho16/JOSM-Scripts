""" If the selected element (node, way, relation) has a wikidata tag, open
Wikidata and go to the entry for that element.
"""
import math
from javax.swing import JOptionPane

from org.openstreetmap.josm.gui import MainApplication
from org.openstreetmap.josm.tools import OpenBrowser

def getBaseLog(x, y):
  return math.log(y) / math.log(x)

active_data_set = MainApplication.getLayerManager().getActiveDataSet()
selected_elements = active_data_set.getAllSelected()
#selected_elements = active_data_set.currentSelectedPrimitives()
if len(selected_elements) != 1:
    JOptionPane.showMessageDialog(MainApplication.getMainFrame(),
                                  'Exactly one element must be selected')
else:
    selected_element = None
    for selected_element_1 in selected_elements:
        selected_element = selected_element_1
    #selected_element = selected_elements[0]
    if not selected_element.hasKey('wikidata'):
        JOptionPane.showMessageDialog(MainApplication.getMainFrame(),
                                    'Selected element must have a "wikidata" tag')
    else:
        wikidata = selected_element.get('wikidata')
        url = 'https://www.wikidata.org/wiki/{}'.format(wikidata)
        OpenBrowser.displayUrl(url)
