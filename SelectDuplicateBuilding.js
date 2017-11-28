/*
Select Duplicate Buildings 
Selects duplicate, or near duplicate, area buildings in JOSM's active datalayer.
A "near duplicate" is a building whose area overlaps another building's
area by more than 50%. Only the first building encountered of an 
overlapping pair is selected. This is done so the issue does not have to be 
looked at twice. The selected buildings are added to the current selection.  
Currently only works with buildings that are ways (not multipolygons).

To Run:
* Install JOSM's Scripting Plugin (only necessary once)
* Place this file in a convenient location on your system (only necessary once)
* Click "Scripting" (on top menu bar)
* Click "Run"
* Click "..." button and select this file.
* Click "Run"

This script is open source and licensed under GPL.
*/
    var main = org.openstreetmap.josm.main;
    var eastnorth = org.openstreetmap.josm.data.coor.EastNorth;
	var layers = require("josm/layers");
    var geometry = org.openstreetmap.josm.tools.Geometry;  
    var way = org.openstreetmap.josm.data.osm.Way;
    var node = org.openstreetmap.josm.data.osm.Node;
    var quadbuckets = org.openstreetmap.josm.data.osm.QuadBuckets;
	var layer = layers.activeLayer;
   	var dataset = layer.data;
	var result = dataset.query("type:way");
    var PathIterator = java.awt.geom.PathIterator;
    var minOverlap = 0.5;
    // Make a spatial index
    qb = new quadbuckets;
	for (j = 0; j < result.length; j++)
	{
	    var way1 = result[j];
	    if(way1.isArea && way1.tags.building)
        {
            qb.add(way1);
        }
    }
	for (j = 0; j < result.length; j++)
	{
	    var way1 = result[j];
        // Only check area buildings that are not already selected.
	    if(way1.isArea && way1.tags.building && !dataset.isSelected(way1))
	    { 
            var result2 = qb.search(way1.getBBox());
            // It should always find 1 (itself), we are only interested if it 
            // finds more than 1.
            if (result2.size() > 1)
            {
                area1 = geometry.getArea(way1.nodes);
                area1_measure = geometry.computeArea(way1);
                for (k = 0; k < result2.size(); k++)
                {
                    var way2 = result2.get(k);
                    // Don't check self and don't check if already selected.
                    if (way2 != way1 && !dataset.isSelected(way2))
                    {
                        area2 = geometry.getArea(way2.nodes);
                        area2_measure = geometry.computeArea(way2);
                        area2.intersect(area1);
                        area3Vertices = pointsFromArea(area2);
                        if (area3Vertices.numCoords > 0)
                        {
                            area3_measure = polygonArea(area3Vertices.Xs, area3Vertices.Ys, area3Vertices.numCoords, dataset);
                            if (area3_measure / area1_measure > minOverlap || area3_measure / area2_measure > minOverlap)
                            {
                                dataset.selection.add(way1);
                                break;
                            }
                        }
                    }
                }
            }
	    }
	}

    
function pointsFromArea(area)
{
    var Xs = [];
    var Ys = [];
    var coords = java.lang.reflect.Array.newInstance(java.lang.Double.TYPE, 6);
    var numCoords = 0;
    var segType;
    var j = area.getPathIterator(null);
    for (; !j.isDone(); j.next()) 
    {
        segType = j.currentSegment(coords);
        switch (segType)
        {
            case PathIterator.SEG_LINETO:
            case PathIterator.SEG_MOVETO:
                Xs[numCoords] = coords[0];
                Ys[numCoords] = coords[1];
                numCoords++;
                break;
        }
    }    
    return{ 
	    Xs: Xs,
	    Ys: Ys,
	    numCoords : numCoords
	}
}


function polygonArea(X, Y, numPoints, dataset) 
{ 
  // We don't want the final node if it is the same as the first. We will add it
  // back in later.
  if (X[0] == X[numPoints - 1] && Y[0] == Y[numPoints - 1])
  {
      numPoints = numPoints - 1;
  }
  var newWay = way();
  for (i = 0; i < numPoints; i++)
    { 
        var newNode = node(eastnorth(X[i], Y[i]));
        newWay.addNode(newNode);
    }
  newWay.addNode(newWay.nodes[0]);
  area = geometry.computeArea(newWay);
  return area;
}
