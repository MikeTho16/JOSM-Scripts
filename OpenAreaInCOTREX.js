/*
Launches the COTREX site/app in a new browser window/tab with it's map zoomed
to approximately the same location as is displayed in JOSM.  COTREX is the Colorado 
Trail Explorer, and is a project of the State of Colorado (US).  The purpose of this
script is to more easily provide feedback to the people that run COTREX, since to 
provide feedback, one must right click on the map location where the issue exists within COTREX.
The COTREX data is already available under the Colorado Open Records Act (CORA), and
can be brought into JOSM using the open layers plugin. This allows the COTREX data 
to be easily compared to OSM data.  Note it has not been yet determined whether the
COTREX data has a license that is compatible with OSM, so this script is only for
providing feedback to COTREX at this time.  
 

To Run:
* Install JOSM's Scripting Plugin (only necessary once)
* Place this file in a convenient location on your system (only necessary once)
* Navigate (e.g. zoom/pan) to area of interest on JOSM's map.
* Click "Scripting" (on top menu bar)
* Click "Run"
* Click "..." button and select this file.
* Click "Run"

This script is open source and licensed under GPL.

Original Author: Mike Thompson
*/


  var lat = org.openstreetmap.josm.gui.MainApplication.getMap().mapView.getRealBounds().getCenter().lat;
  var lon = org.openstreetmap.josm.gui.MainApplication.getMap().mapView.getRealBounds().getCenter().lon;
  var maxLon = org.openstreetmap.josm.gui.MainApplication.getMap().mapView.getRealBounds().getMax().lon;
  var minLon = org.openstreetmap.josm.gui.MainApplication.getMap().mapView.getRealBounds().getMin().lon;
  var zoomLevel = getBaseLog(2, 360 / (maxLon - minLon)) + 1;
  var url = "https://trails.colorado.gov/map/@"+lat+","+lon+","+zoomLevel+"z"
  org.openstreetmap.josm.tools.OpenBrowser.displayUrl(url);


function getBaseLog(x, y) 
  {
  return Math.log(y) / Math.log(x);
  }

