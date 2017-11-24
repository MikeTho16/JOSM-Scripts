/*
Select Non Orthogonal Buildings 
Selects building which are not orthogonal, that is buildings where all corners
do no measure 90 degrees, with the following exceptions:
* Inline vertices (angles of 180 degrees) are ignored).
* Regular polygons are not selected as these are likely to be approximations of 
circles or otherwise valid.
* There is a tolerance of +/- 1 degree.

The selected buildings are added to the current selection.

To Run:
* Install JOSM's Scripting Plugin (only necessary once)
* Place this file in a convenient location on your system (only necessary once)
* Click "Scripting" (on top menu bar)
* Click "Run"
* Click "..." button and select this file.
* Click "Run"

This script is open source and licensed under GPL.
*/
    var geometry = org.openstreetmap.josm.tools.Geometry;        
   	var layers = require("josm/layers");
	var layer = layers.activeLayer;
   	var dataset = layer.data;
	var result = dataset.query("type:way");
    var halfPi = Math.PI / 2;
    var epsDegrees = 1.0;
    var eps = epsDegrees * Math.PI / 180; 
	for (j = 0; j < result.length; j++)
	{
	    var way = result[j];
	    if(way.isArea && way.tags.building)
	    {   
            nodes = way.nodes;
            count = way.getNodesCount();
            var lastAngle = NaN;
            var firstNode = true;
            // First and last are the same, so do not have to examine the last
            for (k = 0; k < (count - 1); k++)
            {
                middleNode = nodes[k];
                if (k == 0)
                {
                    previousNode = nodes[count - 2];
                } 
                else 
                {
                    previousNode = nodes[k - 1];
                }                    
                if (k == (count - 2))
                {
                    nextNode = nodes[0];
                }
                else
                {
                    nextNode = nodes[k + 1];
                }
                angle = Math.abs(geometry.getCornerAngle(previousNode.getEastNorth(), middleNode.getEastNorth(), nextNode.getEastNorth()));
                // Ignore 180 degree (pi radians) angles
                if (Math.abs(angle - Math.PI) > eps)
                {
                    if (firstNode) 
                    {
                        lastAngle = angle;
                        firstNode = false;
                    }
                    else
                    {
                        if (Math.abs(angle - lastAngle) > eps)
                        {
                            dataset.selection.add(way);
                            break;
                        }    
                    }
                }
            }
	    }
	}

