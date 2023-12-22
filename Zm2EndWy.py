# Zm2EndWy.py - Zoom to the end of the selected way
#
# Zooms/pans the start of the selected way.

from org.openstreetmap.josm.gui import MainApplication
from javax.swing import JOptionPane

activeDataSet = MainApplication.getLayerManager().getActiveDataSet()
allSelected = activeDataSet.getAllSelected()
waysSelected = activeDataSet.getSelectedWays()
if len(waysSelected) != 1 or len(allSelected) != len(waysSelected):
    msg = 'You must have one, and only one, way selected'
    JOptionPane.showMessageDialog(MainApplication.getMainFrame(), msg)
else:
    waySel = next(waysSelected.__iter__())
    MainApplication.getMap().mapView.zoomTo(waySel.lastNode().getCoor())
