from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from cqkit import *
import numpy as np

import keybasehelpers as kbh
import coreparameters as cp
import corebasehelpers as cbh
import corebase as cb
import joystickbase as jb
import clusterjoinbasehelpers as cjbh
import thumbbase as tb

def bottom_hull_left_to_joystick(p, height=0.001):
    shape = None
    vertices1 = []
    vertices2 = []
    subp = p[2:]
    for item in subp:
        v0 = item[0]
        v1 = item[1]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
    
    for item in p[0:2]:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0] - 60, v0[1], -10]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
        vertices1.append(np.array(v2))

    t_shape1 = cbh.hull_from_points(vertices1)
    shape = t_shape1 

    return shape

def bottom_hull_left_bottom_to_wall_brace(p, height=0.001):
    shape = None
    vertices1 = []
    vertices2 = []
    subp = p[2:]
    for item in subp:
        v0 = item[0]
        v1 = item[1]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
    
    subp2 = p[3:]
    for item in subp2:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0], v0[1], -10]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
        vertices1.append(np.array(v2))
    
    for item in p[0:2]:
        v0 = item[0]
        v2 = [v0[0] - 60, v0[1], -10]
        vertices1.append(np.array(v2))

    t_shape1 = cbh.hull_from_points(vertices1)
    shape = t_shape1 
    
    return shape

def bottom_hull_left_to_display(p, height=0.001):
    shape = None
    vertices1 = []
    vertices2 = []
    subp = p[2:]
    # for item in subp:
    #     v0 = item[0]
    #     v1 = item[1]
    #     v2 = [v0[0]-60, v0[1], -10]
    #     vertices1.append(np.array(v0))
    #     vertices1.append(np.array(v1))
    #     vertices1.append(np.array(v2))
    
    for item in p[0:2]:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0], v0[1], -10]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
        vertices1.append(np.array(v2))

    for item in p[0:2]:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0] -95, v0[1], -10]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
        vertices1.append(np.array(v2))
    
    for item in p[0:2]:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0] -95, v0[1], -10]
        vertices2.append(np.array(v0))
        vertices2.append(np.array(v1))
        vertices2.append(np.array(v2))
        
    for item in subp:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0], v0[1], -10]
        vertices2.append(np.array(v0))
        vertices2.append(np.array(v1))
        vertices2.append(np.array(v2))

    t_shape1 = cbh.hull_from_points(vertices1)
    t_shape2 = cbh.hull_from_points(vertices2)
    shape = t_shape1 
    shape = shape.union(t_shape2)
    
    return shape
