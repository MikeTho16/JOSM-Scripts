/*
Select Duplicate Buildings 
Selects duplicate, or near duplicate, area buildings in JOSM's active datalayer.
A "near duplicate" is a building whose bounding box overlaps another building's
bounding box by more than 50%. Only the first building encountered of an 
overlapping pair is selected. The selected buildings are added to the current
selection.

To Run:
* Install JOSM's Scripting Plugin (only necessary once)
* Place this file in a convenient location on your system (only necessary once)
* Click "Scripting" (on top menu bar)
* Click "Run"
* Click "..." button and select this file.
* Click "Run"

This script is open source and licensed under GPL.
*/
	var layers = require("josm/layers");
    var geometry = org.openstreetmap.josm.tools.Geometry;        
	var layer = layers.activeLayer;
   	var dataset = layer.data;
	var result = dataset.query("type:way");
	for (j = 0; j < result.length; j++)
	{
	    var way = result[j];
	    if(way.isArea && way.tags.building)
	    { 
            area1 = geometry.getArea(way.nodes);
            area1_measure = area1.getBounds().getHeight() * area1.getBounds().getHeight()
            for (k = j + 1; k < result.length; k++)
            {
                var way2 = result[k];
                if (way2.isArea && way2.tags.building)
                {
                    area2 = geometry.getArea(way2.nodes);
                    area2_measure = area2.getBounds().getHeight() * area2.getBounds().getHeight()
                    area2.intersect(area1);
                    area3_measure = area2.getBounds().getHeight() * area2.getBounds().getHeight()
                    if (area3_measure / area1_measure > 0.5 || area3_measure / area2_measure > 0.5)
                    {
                        dataset.selection.add(way);
                    }
                }
            }
	    }
	}
