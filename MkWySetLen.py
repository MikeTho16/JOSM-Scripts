
from org.openstreetmap.josm.data.coor import LatLon
from org.openstreetmap.josm.data.osm import Node;
from org.openstreetmap.josm.data.osm import Way;
from org.openstreetmap.josm.gui import MainApplication
from javax.swing import JOptionPane

earth_circumference = 40075017.0

length = float(JOptionPane.showInputDialog("Length of way:"))

# Get the center of the screen
scrn_ctr = MainApplication.getMap().mapView.getRealBounds().getCenter()
# Make the starting node
st_node = Node(scrn_ctr)
activeDataSet = MainApplication.getLayerManager().getActiveDataSet()
activeDataSet.addPrimitive(st_node)
end_lat = scrn_ctr.lat() + (length / earth_circumference) * 360
end_lat_lon = LatLon(end_lat, scrn_ctr.lon())
end_node = Node(end_lat_lon)
activeDataSet.addPrimitive(end_node)
new_way = Way()
new_way.addNode(st_node)
new_way.addNode(end_node)
activeDataSet.addPrimitive(new_way)
