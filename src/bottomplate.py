###### import cadquery as cq
from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from jupyter_cadquery import set_sidecar, set_defaults, reset_defaults
from cqkit import *

def bottom_plate_right(mainbody):
    shape = mainbody
    shape = shape.translate((0, 0, -0.1))

    square = cq.Workplane('XY').rect(1000, 1000)
    for wire in square.wires().objects:
        plane = cq.Workplane('XY').add(cq.Face.makeFromWires(wire))
    shape = shape.intersect(plane)
    
    for wire in shape.wires().objects[1:2]:
        centerplate = (cq.Workplane("XY").add(cq.Face.makeFromWires(wire)).workplane())
        centerplate = centerplate.add(wire).toPending().extrude(3)

    print(str(centerplate))
    outer = (cq.Workplane("XY").add(shape.faces("<Z")).workplane())
    outer = outer.add(shape.wires()).toPending().extrude(2.5)
    shape = outer.union(centerplate, tol=.01)

    return shape