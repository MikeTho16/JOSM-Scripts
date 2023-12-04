# Moves the selected selected OSM elements from the current layer
# to a new layer.
#
# Specifically:
#   * Downloads a new layer from the OSM server over the area covered by the selected elements in this layer.
#   * Copies the selected elements from the current layer to the new layer.
#   * Deletes the selected elements from the current layer
#   * Makes the new layer the current layer
#   * Selects the features which were copied.

import math

#import static org.openstreetmap.josm.tools.I18n.tr;

#import java.awt.event.ActionEvent;
#import java.awt.event.KeyEvent;
#import java.awt.geom.Rectangle2D;
#import java.util.ArrayList;
#import java.util.Collection;
#import java.util.List;
#import java.util.concurrent.Future;

#import org.openstreetmap.josm.actions.JosmAction;
#import org.openstreetmap.josm.actions.downloadtasks.DownloadTaskList;
#import org.openstreetmap.josm.data.coor.LatLon;
#import org.openstreetmap.josm.data.osm.BBox;
#import org.openstreetmap.josm.data.osm.DataSet;
#import org.openstreetmap.josm.data.osm.Node;
#import org.openstreetmap.josm.data.osm.OsmPrimitive;
from org.openstreetmap.josm.data.osm import QuadBuckets;
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



# Find the bbox of the selection
activeDataSet = MainApplication.getLayerManager().getActiveDataSet()
exit()
allSelected = activeDataSet.getAllSelected();
#    BBox selBBox = new BBox();
#    QuadBuckets<OsmPrimitive> qb = new QuadBuckets<>();
#    for (OsmPrimitive osmPrim : allSelected) {
#      selBBox.addPrimitive(osmPrim, 0);
#      qb.add(osmPrim);
#    }

    # Expand the BBox so that selected OSM primitives are not right on the edge of the
    # download area.
    metersPerDegLat = 100000.0;
    avglat = (selBBox.getTopLeftLat() + selBBox.getBottomRightLat()) / 2;
    scale = math.cos(Utils.toRadians(avglat));
    bufferDist = 100; # Meters
    final double bufferY = bufferDist / metersPerDegLat;
    final double bufferX = bufferY / scale;
    LatLon upperLeft = new LatLon(selBBox.getTopLeftLat() + bufferY, selBBox.getTopLeftLon() - bufferX);
    LatLon bottomRight = new LatLon(selBBox.getBottomRightLat() - bufferY, selBBox.getBottomRightLon() + bufferX);
    BBox bufSelBBox = new BBox(upperLeft, bottomRight);

    // Divide BBox into parts if too large
    double maxDim = 0.05;
    double rows = Math.ceil(bufSelBBox.height() / maxDim);
    double cols = Math.ceil(bufSelBBox.width() / maxDim);
    double height = bufSelBBox.height() / rows;
    double width = bufSelBBox.width() / cols;
    List<Rectangle2D> toDownload = new ArrayList<>();
    for (int row = 0; row < rows; row++) {
      for (int col = 0; col < cols; col++) {
        // Check if there are any selected osm primitives withing this specific rectangle
        List<OsmPrimitive> interPrims = qb.search(new BBox(bufSelBBox.getTopLeftLon() + width * col, bufSelBBox.getBottomRightLat() + height * row,
          bufSelBBox.getTopLeftLon() + width * (col + 1), bufSelBBox.getBottomRightLat() + height * (row + 1)));
        if (interPrims.size() > 0) {
          toDownload.add(new Rectangle2D.Double(bufSelBBox.getTopLeftLon() + width * col, bufSelBBox.getBottomRightLat() + height * row, width, height));
        }
      }
    }

    // Download the data
    final boolean osmDownload = true;
    final boolean gpxDownload = false;
    final boolean newLayer = true;
    final boolean zoomAfterDownload = true;
    final PleaseWaitProgressMonitor monitor = new PleaseWaitProgressMonitor(tr("Download data"));
    final Future<?> future = new DownloadTaskList(zoomAfterDownload)
            .download(newLayer, toDownload, osmDownload, gpxDownload, monitor);
    waitFuture(future, monitor);

    // Merge the data
    OsmDataLayer targetDataSet = getLayerManager().getEditLayer();
    MergeSourceBuildingVisitor builder = new MergeSourceBuildingVisitor(activeDataSet);
    targetDataSet.mergeFrom(builder.build());

    // Select the data just merged
    DataSet ds = getLayerManager().getActiveDataSet();
    for (Node node : ds.getNodes()) {
      if (node.isNew()) {
        ds.addSelected(node);
      }
    }
    for (Way way : ds.getWays()) {
      if (way.isNew()) {
        ds.addSelected(way);
      }
    }
    for (Relation relation : ds.getRelations()) {
      if (relation.isNew()) {
        ds.addSelected(relation);
      }
    }

    // Delete selected from original dataset
    for (OsmPrimitive o : activeDataSet.getSelected()) {
      o.setDeleted(true);
    }
  }
}

