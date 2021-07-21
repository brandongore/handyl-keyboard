from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from jupyter_cadquery import set_sidecar, set_defaults, reset_defaults
from cqkit import *
import numpy as np
from numpy import pi, math
import os.path as path
from scipy.spatial import ConvexHull as sphull

import corebase as cb
import corebasehelpers as cbh
import coreparameters as cp
import keybase as kb
import keybasehelpers as kbh

def model_right():
    print('model_right()')
    shape = cq.Workplane('XY')
    shape = shape.union(key_holes(), tol=.01)
    shape = shape.union(connectors(), tol=.01)
    shape = shape.union(case_walls(), tol=.01)

    if cp.show_caps:
        shape = shape.add(caps(), tol=.01)

    print('end of model right')
    return shape

def key_holes():
    #print('key_holes()')
    hole = cb.single_plate(padding=True, padding_amount=0.007)
    holes = []
    for column in range(cp.ncols):
        for row in range(cp.nrows):
            if (not row == cp.lastrow):
                if not((column == 3 and row == 0) or (column == 3 and row == 1)):
                    holes.append(kb.key_place(hole, column, row))
    shape = cbh.union(holes)

    return shape

def connectors():
    #print('connectors()')
    hulls = []
    #shape = cq.Workplane('XY')
    for column in range(cp.ncols - 1):
        for row in range(cp.lastrow):  # need to consider last_row?
            #print("pos: "+ str(kb.key_position(cb.webposttl, column + 1, row)))
            places = []
            places.append(kb.key_position(cb.webposttl, column + 1, row))
            places.append(kb.key_position(cb.webposttr, column, row))
            places.append(kb.key_position(cb.webpostbl, column + 1, row))
            places.append(kb.key_position(cb.webpostbr, column, row))
            hulls.append(cbh.triangle_hulls(places))
    
    for column in range(cp.ncols):
        # for row in range(nrows-1):
        for row in range(cp.cornerrow):
            places = []
            places.append(kb.key_position(cb.webpostbl, column, row))
            places.append(kb.key_position(cb.webpostbr, column, row))
            places.append(kb.key_position(cb.webposttl, column, row + 1))
            places.append(kb.key_position(cb.webposttr, column, row + 1))
            hulls.append(cbh.triangle_hulls(places))
    
    for column in range(cp.ncols - 1):
        # for row in range(nrows-1):  # need to consider last_row?
        for row in range(cp.cornerrow):  # need to consider last_row?
            places = []
            places.append(kb.key_position(cb.webpostbr, column, row))
            places.append(kb.key_position(cb.webposttr, column, row + 1))
            places.append(kb.key_position(cb.webpostbl, column + 1, row))
            places.append(kb.key_position(cb.webposttl, column + 1, row + 1))
            hulls.append(cbh.triangle_hulls(places))
            
    for column in range(cp.ncols):
        for row in range(cp.nrows-1):
            if (column == 3 and row == 1):
                places = []
                places.append(kb.key_position(cb.webpostbl, column, row))
                places.append(kb.key_position(cb.webpostbr, column, row))
                places.append(kb.key_position(cb.webposttl, column, row ))
                places.append(kb.key_position(cb.webposttr, column, row))
                hulls.append(cbh.triangle_hulls(places))
            if (column == 3 and row == 0):
                places = []
                places.append(kb.key_position(cb.webpostbl, column, row))
                places.append(kb.key_position(cb.webpostbr, column, row))
                places.append(kb.key_position(cb.webposttl, column, row ))
                places.append(kb.key_position(cb.webposttr, column, row))
                hulls.append(cbh.triangle_hulls(places))

    return cbh.union(hulls)

##########
## Case ##
##########

def back_wall():
    #print("back_wall()")
    x = 0
    shape = cq.Workplane('XY')
    shape = shape.union(kb.key_wall_brace_position_thin_back_extended(0, 0, 0, 1, cb.webposttl, 0, 0, 0, 1, cb.webposttr))

    shape = shape.union(kb.key_wall_brace_position_thin_back(1, 0, 1, 0.55, cb.webposttl, 1, 0, 0.5, 1, cb.webposttr))
    shape = shape.union(kb.key_wall_brace_position_thin_back_to_thin_back_extended(1, 0, 1, 0.55, cb.webposttl, 0, 0, 0, 1, cb.webposttr))
    # for i in range(cp.ncols -3):
    #     x = i + 1
    #     shape = shape.union(kb.key_wall_brace_position_thin_back(x, 0, 0, 1, cb.webposttl, x, 0, 0, 1, cb.webposttr))
    #     shape = shape.union(kb.key_wall_brace_position_thin_back(x, 0, 0, 1, cb.webposttl, x - 1, 0, 0, 1, cb.webposttr))
        
    shape = shape.union(kb.key_wall_brace_position_thin_back(2, 0, 0, 1, cb.webposttl, 2, 0, -1, 1, cb.webposttr))
    shape = shape.union(kb.key_wall_brace_position_thin_back(2, 0, 0, 1, cb.webposttl, 1, 0, 0.5, 1, cb.webposttr))
        
    shape = shape.union(kb.key_wall_brace_position_thin_back(3, 0, 0, 1, cb.webposttl, 3 - 1, 0, -1, 1, cb.webposttr))
    shape = shape.union(kb.key_wall_brace_position_thin_back(3, 0, 0, 1, cb.webposttl, 3, 0, 0, 1, cb.webposttr))
    
    return shape

def right_wall():
    print("right_wall()")
    y = 0
    shape = cq.Workplane('XY')

    shape = shape.union(kb.wall_brace_thin_back(
        (lambda sh: kb.key_position(sh, 3, 0)),
        0,
        1,
        cb.webposttr,
        (lambda sh: kb.right_key_place(sh, 3, 0, 1)),
        0,
        1,
        cb.wbpost,
    ))

    shape = shape.union(kb.wall_brace_short_to_thin_back(
        (lambda sh: kb.right_key_place(sh, 3, 0, 1)),
        0,
        1,
        cb.wbpost,
        (lambda sh: kb.right_key_place(sh, 3, 0, 1)),
        1,
        0,
        cb.wbpost,
    ))

    for i in range(cp.lastrow):
        y = i 
        temp_shape1 = kb.wall_brace_short(
            (lambda sh: kb.right_key_place(sh, 3, y, -1)),
            1,
            0,
            cb.wbpost,
            (lambda sh: kb.right_key_place(sh, 3, y, 1)),
            1,
            0,
            cb.wbpost,
        )
        temp_shape2 = cbh.hull_from_shapes((
            kb.key_position(cb.webposttr, 3, y),
            kb.key_position(cb.webpostbr, 3, y),
            kb.right_key_place(cb.wbpost, 3, y, -1),
            kb.right_key_place(cb.wbpost, 3, y, 1),
        ))
        shape = shape.union(temp_shape1)
        shape = shape.union(temp_shape2)
        
    for i in range(cp.lastrow - 1):
        y = i + 1
        temp_shape1 = kb.wall_brace_short(
            (lambda sh: kb.right_key_place(sh, 3, y, 1)),
            1,
            0,
            cb.wbpost,
            (lambda sh: kb.right_key_place(sh, 3, y-1, -1)),
            1,
            0,
            cb.wbpost,
        )
        temp_shape2 = cbh.hull_from_shapes((
            kb.key_position(cb.webposttr, 3, y),
            kb.key_position(cb.webpostbr, 3, y - 1),
            kb.right_key_place(cb.wbpost, 3, y -1 , -1),
            kb.right_key_place(cb.wbpost, 3, y, 1),
        ))
        shape = shape.union(temp_shape1)
        shape = shape.union(temp_shape2)
    
    
    shape = shape.union(kb.wall_brace_thin(
        (lambda sh: kb.key_position(sh, 3, cp.lastrow-1)),
        1,
        -2,
        cb.webpostbr,
        (lambda sh: kb.right_key_place(sh, 3, cp.lastrow-1, -1)),
        0.5,
        -1,
        cb.wbpost,
    ))

    shape = shape.union(kb.wall_brace_short_to_thin(
        (lambda sh: kb.right_key_place(sh, 3, cp.lastrow-1, -1)),
        0.5,
        -1,
        cb.wbpost,
        (lambda sh: kb.right_key_place(sh, 3, cp.lastrow-1, -1)),
        1,
        0,
        cb.wbpost,
    ))
    return shape

def left_wall():
    #print('left_wall()')
    shape = cq.Workplane('XY')
    shape = shape.union(kb.wall_brace_thin_back_to_thin_back_extended(
        (lambda sh: kb.left_key_place(sh, 0, 1)),
        0,
        2,
        cb.wbpost,
        (lambda sh: kb.key_position(sh, 0, 0)),
        0, 
        1,
        cb.webposttl,
    ))

    # shape = shape.union(kb.wall_brace_left_to_thin_back(
    #     (lambda sh: kb.left_key_place(sh, 0, 1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    #     (lambda sh: kb.left_key_place(sh, 0, 1)),
    #     0,
    #     1,
    #     cb.wbpost,
    # ))

    y = cp.lastrow - 4
    # temp_shape1 = kb.wall_brace_left(
    #     (lambda sh: kb.left_key_place(sh, y, 1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    #     (lambda sh: kb.left_key_place(sh, y, -1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    # )
    temp_shape2 = cbh.hull_from_shapes((
        kb.key_position(cb.webposttl, 0, y),
        kb.key_position(cb.webpostbl, 0, y),
        kb.left_key_place(cb.wbpost, y, 1),
        kb.left_key_place(cb.wbpost, y, -1),
    ))
    #shape = shape.union(temp_shape1)
    shape = shape.union(temp_shape2)
 
    y = cp.lastrow - 3
    # temp_shape1 = kb.wall_brace_left(
    #     (lambda sh: kb.left_key_place(sh, y, 1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    #     (lambda sh: kb.left_key_place(sh, y, -1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    # )
    temp_shape2 = cbh.hull_from_shapes((
        kb.key_position(cb.webposttl, 0, y),
        kb.key_position(cb.webpostbl, 0, y),
        kb.left_key_place(cb.wbpost, y, 1),
        kb.left_key_place(cb.wbpost, y, -1),
    ))
    #shape = shape.union(temp_shape1)
    shape = shape.union(temp_shape2)

    y = cp.lastrow - 3
    # temp_shape1 = kb.wall_brace_left(
    #     (lambda sh: kb.left_key_place(sh, y - 1, -1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    #     (lambda sh: kb.left_key_place(sh, y, 1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    # )
    temp_shape2 = cbh.hull_from_shapes((
        kb.key_position(cb.webposttl, 0, y),
        kb.key_position(cb.webpostbl, 0, y - 1),
        kb.left_key_place(cb.wbpost, y, 1),
        kb.left_key_place(cb.wbpost, y - 1, -1),
    ))
    #shape = shape.union(temp_shape1)
    shape = shape.union(temp_shape2)     
   
    y = cp.lastrow - 2
    temp_shape2 = cbh.hull_from_shapes((
        kb.key_position(cb.webposttl, 0, y),
        kb.key_position(cb.webpostbl, 0, y),
        kb.left_key_place(cb.wbpost, y, 1),
        kb.left_key_place(cb.wbpost, y, -1),
    ))
    shape = shape.union(temp_shape2)

    y = cp.lastrow - 2
    temp_shape2 = cbh.hull_from_shapes((
        kb.key_position(cb.webposttl, 0, y),
        kb.key_position(cb.webpostbl, 0, y - 1),
        kb.left_key_place(cb.wbpost, y, 1),
        kb.left_key_place(cb.wbpost, y - 1, -1),
    ))
    shape = shape.union(temp_shape2)
        
        
    y = cp.lastrow - 1
    temp_shape2 = cbh.hull_from_shapes((
        kb.key_position(cb.webposttl, 0, y),
        kb.key_position(cb.webpostbl, 0, y),
        kb.left_key_place(cb.wbpost, y, 1),
        kb.left_key_place(cb.wbpost, y, -1),
    ))
    shape = shape.union(temp_shape2)

    y = cp.lastrow - 1
    temp_shape2 = cbh.hull_from_shapes((
        kb.key_position(cb.webposttl, 0, y),
        kb.key_position(cb.webpostbl, 0, y - 1),
        kb.left_key_place(cb.wbpost, y, 1),
        kb.left_key_place(cb.wbpost, y - 1, -1),
    ))
    shape = shape.union(temp_shape2)

    shape = shape.union(kb.wall_brace_thin_extended(
        (lambda sh: kb.key_position(sh, 0, 3)),
        2.5, 
        -1.5,
        cb.webpostbl,
        (lambda sh: kb.left_key_place(sh, cp.cornerrow, -1)),
        3,
        -1.9,
        cb.wbpost,
    ))
    return shape

def front_wall():
    #print('front_wall()')
    x = 0
    shape = cq.Workplane('XY')
    shape = shape.union(kb.key_wall_brace_position_thin_extended(0, cp.cornerrow, 1.5, -1.2, cb.webpostbr, 0, cp.cornerrow, 2.5, -1.5, cb.webpostbl))

    shape = shape.union(kb.key_wall_brace_position_thin_to_thin_extended(1, cp.cornerrow, 1, -1.35, cb.webpostbl, 0, cp.cornerrow, 1.5, -1.2, cb.webpostbr))
    shape = shape.union(kb.key_wall_brace_position_thin(1, cp.cornerrow, 1, -1.35, cb.webpostbl, 1, cp.cornerrow, 0, -1.25, cb.webpostbr))
    
    shape = shape.union(kb.key_wall_brace_position_thin(2, cp.cornerrow, 0.5, -1.25, cb.webpostbl, 1, cp.cornerrow, 0, -1.25, cb.webpostbr))  
    shape = shape.union(kb.key_wall_brace_position_thin(2, cp.cornerrow, 0.5, -1.25, cb.webpostbl, 2, cp.cornerrow, -1, -1, cb.webpostbr))
    
    shape = shape.union(kb.key_wall_brace_position_thin(3, cp.cornerrow, 3, -2, cb.webpostbl, 2, cp.cornerrow, -1, -1, cb.webpostbr)) 
    shape = shape.union(kb.key_wall_brace_position_thin(3, cp.cornerrow, 3, -2, cb.webpostbl, 3, cp.cornerrow, 1, -2, cb.webpostbr))      
    return shape

def case_walls():
    print('case_walls()')
    shape = cq.Workplane('XY')
    return (
        cbh.union([
            shape,
            back_wall(),
            left_wall(),
            right_wall(),
            front_wall(),
        ])
    )


def caps():
    cap = cb.sa_cap()
    caps = None
    for column in range(cp.ncols):
        for row in range(cp.nrows):
            if (not column == cp.lastcol and not row == cp.lastrow):
                if caps is None:
                    caps = kb.key_place(cap, column, row)
                else:
                    caps = caps.add(kb.key_place(cap, column, row))
                    
    caps.add(kb.key_place(cap, 3, 2))
    caps.add(kb.key_place(cap, 3, 3))

    return caps