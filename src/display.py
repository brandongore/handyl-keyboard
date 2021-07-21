from cadquery import Wire, Edge
from cadquery import selectors
from cadquery import Shape
from cadquery import occ_impl
from cadquery import Workplane
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from jupyter_cadquery import set_sidecar, set_defaults, reset_defaults
from cqkit import *

import corebase as cb
import corebasehelpers as cbh
import coreparameters as cp
import thumbbase as tb
import thumbbasehelpers as tbh
import displaybase as db
import displaybasehelpers as dbh

def display_right():
    shape = cq.Workplane('XY').union(display_holder())
    shape = shape.union(display_walls(), tol=.01)
    print('end of display right')
    return shape

def display_cube():
    #print('display_cube()')
    shape = cq.Workplane("XY").box(88, 39, 12.1).fillet(1)

    return shape

def display_hole(addPinCutout = True):
    #3.73 bottom pin height to top of processor  3.9   -> 5.8   3.03
    shape = cq.Workplane("XY").box(65.87, 30.94, 8.66).translate((-(88-65.87)/2 + 4, 0 , (12.1-8.66)/2))
    top_brace = cq.Workplane("XY").box(28, 5, 5.56 - 1.61).translate((-(88-65.87)/2 + 4, (30.94-5)/2 , (12.1-8.66)/2 - 4.71/2))

    bottom_brace_1 = cq.Workplane("XY").box(7.5, 7.5, 5.56 - 1.61).translate((-(88-65.87)/2 + 4 +65.87/2 -7.5/2, -(30.94-7.5)/2 , (12.1-8.66)/2 - 4.71/2))
    bottom_brace_2 = cq.Workplane("XY").box(7.5, 7.5, 5.56 - 1.61).translate((-(88-65.87)/2 + 4 -65.87/2 +7.5/2, -(30.94-7.5)/2 , (12.1-8.66)/2 - 4.71/2))


    # shape = cq.Workplane("XY").box(65.76, 30.83, 5.56).translate((-(88-65.76)/2 + 4, 0 , (12.1-5.56)/2))
    # top_brace = cq.Workplane("XY").box(28, 5, 5.56 - 1.61).translate((-(88-65.76)/2 + 4, (30.83-5)/2 , (12.1-5.56)/2 - 1.61/2))

    # bottom_brace_1 = cq.Workplane("XY").box(7.5, 7.5, 5.56 - 1.61).translate((-(88-65.76)/2 + 4 +65.76/2 -7.5/2, -(30.83-7.5)/2 , (12.1-5.56)/2 - 1.61/2))
    # bottom_brace_2 = cq.Workplane("XY").box(7.5, 7.5, 5.56 - 1.61).translate((-(88-65.76)/2 + 4 -65.76/2 +7.5/2, -(30.83-7.5)/2 , (12.1-5.56)/2 - 1.61/2))

    # pin_cutout = cq.Workplane("XY").box(27, 18.1, 12.1-1.61).translate((-(88-65.76)/2 + 4 +65.76/2, (30.83-18.1)/2 - 3.2 , -1.61/2))




    shape = shape.cut(top_brace)
    shape = shape.cut(bottom_brace_1)
    shape = shape.cut(bottom_brace_2)

    if addPinCutout:
        pin_cutout = cq.Workplane("XY").box(27, 18.1, 12.1-1.61).translate((-(88-65.87)/2 + 4 +65.87/2, (30.94-18.1)/2 - 3.2 , -4.71/2))
        shape = shape.union(pin_cutout)

    return shape   

def display_mount_screws():
    hole1 = cq.Workplane("XY").circle(1.5).extrude(15)
    hole2 = cq.Workplane("XY").circle(1.5).extrude(15)

    hole1 = hole1.translate((-(88-65.87)/2 + 4 +65.85/2 - 3.79 , -(30.94)/2 + 3.61, -8))
    hole2 = hole2.translate((-(88-65.87)/2 + 4 -65.85/2 + 3.79 , -(30.94)/2 + 3.61, -8))

    shape = cq.Workplane("XY")
    shape = shape.union(hole1)
    shape = shape.union(hole2)
    shape = shape.translate((0, 0, 0))
    return shape

def display_holder():
    shape = cq.Workplane('XY').union(display_cube())
    shape = shape.cut(display_hole())
    shape = shape.cut(display_mount_screws())

    xrad = cbh.deg2rad(cp.display_rotation[0])  
    yrad = cbh.deg2rad(cp.display_rotation[1]) 
    zrad = cbh.deg2rad(cp.display_rotation[2]) 
    
    shape = cbh.y_rot(shape, yrad)
    shape = cbh.x_rot(shape, xrad)
    shape = cbh.z_rot(shape, zrad)

    shape = shape.translate((cp.display_offset[0],cp.display_offset[1],cp.display_offset[2]))

    return shape

def display_walls():
    #print('thumb_walls()')
    shape = cq.Workplane('XY')
    
    shape = shape.union(db.display_wall_brace_position(-1, -1, dbh.displaywebpostbl, -1, 0, dbh.displaywebposttl))
    shape = shape.union(db.display_wall_brace_position(0, 1, dbh.displaywebposttl, -1, 0, dbh.displaywebposttl))

    return shape

def display_screw_holder():
    #6  2.6
    shape = cq.Workplane("XY").box(65.87, 6, 2.6).translate((-(88-65.87)/2 + 4, -(30.94)/2 + 3.61 , 0))
    shape = shape.cut(cq.Workplane("XY").box(15, 3.4, 2.9).translate((-(88-65.87)/2 + 4, -(30.94)/2 + 3.61 +3.4/2 , 0)))
    shape = shape.cut(display_mount_screws())

    # xrad = cbh.deg2rad(cp.display_rotation[0])  
    # yrad = cbh.deg2rad(cp.display_rotation[1]) 
    # zrad = cbh.deg2rad(cp.display_rotation[2]) 
    
    # shape = cbh.y_rot(shape, yrad)
    # shape = cbh.x_rot(shape, xrad)
    # shape = cbh.z_rot(shape, zrad)

    # shape = shape.translate((cp.display_offset[0],cp.display_offset[1],cp.display_offset[2]))

    return shape
