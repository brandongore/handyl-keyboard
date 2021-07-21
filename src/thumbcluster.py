from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from jupyter_cadquery import set_sidecar, set_defaults, reset_defaults
from cqkit import *

import corebase as cb
import corebasehelpers as cbh
import coreparameters as cp
import thumbbase as tb
import thumbbasehelpers as tbh

def thumb_right():
    shape = cq.Workplane('XY').union(thumb_holes())
    shape = shape.union(thumb_walls(), tol=.01)
    shape = shape.union(thumb_connectors(), tol=.01)

    if cp.show_caps:
        shape = shape.add(thumb_caps())

    print('end of thumb right')
    return shape

def thumb_holes():
    #print('key_holes()')
    #padding_amount=0.013
    #padding=True
    hole = cb.single_plate(padding=True, padding_amount=0.007)
    holes = []
    for column in range(2):
        for row in range(3):
            # if (not row == lastrow):
            #     if(not row == 2 or not column == lastcol):
            if column == 0 or (column == 1 and row == 0):
                holes.append(tb.thumb_place(hole, column, row))
    
    shape = cbh.union(holes)

    return shape

def thumb_walls():
    #print('thumb_walls()')
    shape = cq.Workplane('XY')
    
    shape = shape.union(tb.thumb_wall_brace_position(0, 0, 1, 0, cb.webpostbr, 0, 0, 1.25, 0.25, cb.webposttr))
    shape = shape.union(tb.thumb_wall_brace_position(0, 0, 1, 0, cb.webpostbr, 0, 1, 1, 0, cb.webposttr))
    
    shape = shape.union(tb.thumb_wall_brace_position(0, 1, 1, 0, cb.webpostbr, 0, 1, 1, 0, cb.webposttr))
    shape = shape.union(tb.thumb_wall_brace_position(0, 1, 1, 0, cb.webpostbr, 0, 2, 1, 0, cb.webposttr))
    
    shape = shape.union(tb.thumb_wall_brace_position(0, 2, 1, 0, cb.webpostbr, 0, 2, 1, 0, cb.webposttr))

    shape = shape.union(tb.thumb_wall_brace_position(0, 2, 0, -1.5, cb.webpostbl, 0, 2, 0, -1.5, cb.webpostbr))
    
    shape = shape.union(tb.thumb_wall_brace_position(0, 2, 1, 0, cb.webpostbr, 0, 2, 0, -1.5, cb.webpostbr))   

    return shape

def thumb_connectors():
    #print('connectors()')
    hulls = []

    for column in range(1):
        for row in range(2):
            places = []
            places.append(tb.thumb_position(cb.webpostbl, column, row))
            places.append(tb.thumb_position(cb.webpostbr, column, row))
            places.append(tb.thumb_position(cb.webposttl, column, row + 1))
            places.append(tb.thumb_position(cb.webposttr, column, row + 1))
            hulls.append(cbh.triangle_hulls(places))
                
    places = []
    places.append(tb.thumb_position(cb.webposttr, 1, 0))
    places.append(tb.thumb_position(cb.webpostbr, 1, 0))
    places.append(tb.thumb_position(cb.webposttl, 0, 0))
    places.append(tb.thumb_position(cb.webpostbl, 0, 0))
    hulls.append(cbh.triangle_hulls(places))

    return cbh.union(hulls)

def thumb_caps():
    cap = cb.sa_cap()
    caps = None
    for column in range(1):
        for row in range(4):
            if (not column == cp.lastcol and not row == cp.lastrow):
                if caps is None:
                    caps = tb.thumb_place(cap, column, row)
                else:
                    caps = caps.add(tb.thumb_place(cap, column, row))

    return caps
