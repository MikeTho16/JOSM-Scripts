# JOSM-Scripts
Scripts for use with OpenStreetMap's JOSM editor.

* You must have the JOSM Scripting Plugin installed.
* Scripting (on the top menu) -> Run -> select this file

## MvSrc2TgtLyr.py
- Moves the the elements that are selected in the "source" layer to the "target" layer.
- Deletes the elements from the "source" layer
- Selects the elements in the "target" layer
- Sets the active layer to the "target" layer and makes it visible
- Makes the "source" layer not visible
- You must have one layer named "sorce" and one named "target"

## Zm2Clpbrd.py
- Zooms/pans the map to the coordinates currently on the clipboard.
- The coordinates must be in the format latitude, longitude
