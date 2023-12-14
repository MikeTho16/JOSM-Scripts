# Gets the elevation of the selected node from the USGS 3D Elevation Program Data
#

import math
import json
#import static org.openstreetmap.josm.tools.I18n.tr;

#import java.awt.event.ActionEvent;
#import java.awt.event.KeyEvent;
#import java.awt.geom.Rectangle2D;
#import java.util.ArrayList;
#import java.util.Collection;
#import java.util.List;
#import java.util.concurrent.Future;
from java.io import BufferedReader
from java.io import DataOutputStream
from java.io import InputStreamReader
from java.net import HttpURLConnection
from java.net import URL
from java.net import URLEncoder

from javax.swing import JOptionPane

#import org.openstreetmap.josm.actions.JosmAction;
#import org.openstreetmap.josm.actions.downloadtasks.DownloadTaskList;
#import org.openstreetmap.josm.data.coor.LatLon;
#import org.openstreetmap.josm.data.osm.BBox;
#import org.openstreetmap.josm.data.osm.DataSet;
#import org.openstreetmap.josm.data.osm.Node;
#import org.openstreetmap.josm.data.osm.OsmPrimitive;
#from org.openstreetmap.josm.data.osm import QuadBuckets;
#import org.openstreetmap.josm.data.osm.Relation;
#import org.openstreetmap.josm.data.osm.Way;
#import org.openstreetmap.josm.data.osm.visitor.MergeSourceBuildingVisitor;
from org.openstreetmap.josm.gui import MainApplication;
#import org.openstreetmap.josm.gui.layer.OsmDataLayer;
#import org.openstreetmap.josm.gui.progress.swing.PleaseWaitProgressMonitor;
#import org.openstreetmap.josm.tools.Shortcut;
#import org.openstreetmap.josm.tools.Utils;

# ref: https://docs.oracle.com/javase/8/docs/api/overview-summary.html
#      https://josm.openstreetmap.de/wiki/DevelopersGuide/DevelopingPlugins
#      https://josm.openstreetmap.de/doc/overview-summary.html
#      http://locationtech.github.io/jts/javadoc/index.html
#
FEET_PER_METER = 3.28084

# Get the easting and northing of the selected node
active_dataset = MainApplication.getLayerManager().getActiveDataSet()
selected_nodes = active_dataset.getSelectedNodes()
if len(selected_nodes) == 1:
    for node in selected_nodes:
        selected_node = node 
    #selected_node = selected_nodes[0]
    east_north = selected_node.getEastNorth()
    east = east_north.east()
    north = east_north.north()
    url = URL('https://elevation.nationalmap.gov/arcgis/rest/services/3DEPElevation/ImageServer/identify')
    #con = HttpURLConnection(URL)
    con = url.openConnection()
    con.setRequestMethod('GET')
    con.setDoOutput(True)
    out = DataOutputStream(con.getOutputStream())
    geometry = URLEncoder.encode(json.dumps({"x":east,"y":north,"spatialReference":{"wkid":102100}}))
    #rendering_rules = URLEncoder.encode(json.dumps([{"rasterFunction": "None"},{"rasterFunction": "Slope Degrees"},{"rasterFunction": "Aspect Degrees"},{"rasterFunction": "Height Ellipsoidal"}]))
    rendering_rules = URLEncoder.encode(json.dumps([{"rasterFunction": "Height Ellipsoidal"}]))
    parameters = 'geometry=' + geometry + '&geometryType=esriGeometryPoint&returnGeometry=false&returnCatalogItems=false&renderingRules=' + rendering_rules + '&f=json&wab_dv=1.5'
    out.writeBytes(parameters)
    out.flush()
    out.close()
    in_ = BufferedReader(InputStreamReader(con.getInputStream()))
    input_line = in_.readLine()
    in_.close()
    con.disconnect()
    height = json.loads(input_line)['value']
    height_feet = float(height) * FEET_PER_METER
    JOptionPane.showMessageDialog(MainApplication.getMainFrame(), 'Height (meters) = ' + str(height) + '\nHeight (feet) = ' + str(height_feet))

                                        
    
    
    
                            
#                            ?geometry=%7B%22x%22%3A-11756125.560217619%2C%22y%22%3A4902747.194148677%2C%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%7D&geometryType=esriGeometryPoint&returnGeometry=false&returnCatalogItems=false&renderingRules=%5B%7B%22rasterFunction%22%3A%20%22None%22%7D%2C%7B%22rasterFunction%22%3A%20%22Slope%20Degrees%22%7D%2C%7B%22rasterFunction%22%3A%20%22Aspect%20Degrees%22%7D%2C%7B%22rasterFunction%22%3A%20%22Height%20Ellipsoidal%22%7D%5D&f=json&wab_dv=1.5' \
#  -H 'authority: elevation.nationalmap.gov' \
#  -H 'accept: */*' \
#  -H 'accept-language: en-US,en;q=0.9' \
#  -H 'content-type: application/x-www-form-urlencoded' \
#  -H 'origin: https://apps.nationalmap.gov' \
#  -H 'referer: https://apps.nationalmap.gov/' \
#  -H 'sec-ch-ua: "Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
#  -H 'sec-ch-ua-mobile: ?0' \
#  -H 'sec-ch-ua-platform: "Linux"' \
#  -H 'sec-fetch-dest: empty' \
#  -H 'sec-fetch-mode: cors' \
#  -H 'sec-fetch-site: same-site' \
#  -H 'sec-gpc: 1' \
#  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
#  --compressed

