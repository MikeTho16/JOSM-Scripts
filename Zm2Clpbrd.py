# Zm2Clpbrd.py - Zoom to the coordinates on the clipboard.
#
# Zooms/pans the map view to the latitude and longitude on the clipboard.
# The latitude and longitude must be in the format lat,lon

from org.openstreetmap.josm.gui.datatransfer import ClipboardUtils
from org.openstreetmap.josm.gui import MainApplication
from org.openstreetmap.josm.data.coor import LatLon

LatLonStr = ClipboardUtils.getClipboardStringContent()
LatLonArr = LatLonStr.split(",")
Lat = float(LatLonArr[0])
Lon = float(LatLonArr[1])
LatLon = LatLon(Lat, Lon)
MainApplication.getMap().mapView.zoomTo(LatLon)
