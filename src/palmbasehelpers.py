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
import palmbase as pb

def apply_palm_geometry(shape, transform, translate_fn, rotate_x_fn, rotate_y_fn, rotate_z_fn):
    xrad = cbh.deg2rad(-44)  
    yrad = cbh.deg2rad(-6) 
    zrad = cbh.deg2rad(244) 
    
    shape = translate_fn(shape, transform.translation)
    #shape = translate_fn(shape, [0, 0, 10])
    #shape = rotate_y_fn(shape, yrad)
    #shape = rotate_z_fn(shape, zrad)
    #shape = rotate_x_fn(shape, xrad)
    
    #rest = rotate(rest, [-44, -6, 244])
    #rest = translate(rest, [30, -75, -5])
    
    #shape = translate_fn(shape, [30, -75, -5])
    
    return shape

def palm_bottom_hull_left(p, height=0.001):
    shape = None
    vertices = []
    for item in p:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0] - 15, v0[1], -10]
        vertices.append(np.array(v0))
        vertices.append(np.array(v1))
        vertices.append(np.array(v2))

    t_shape = cbh.hull_from_points(vertices)
    shape = t_shape 
    return shape

def palm_bottom_hull_left_to_default(p, height=0.001):
    shape = None
    vertices1 = []
    vertices2 = []
    subp = p[2:]
    for item in subp:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0] -15, v0[1], -10]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
        vertices1.append(np.array(v2))
    
    for item in p[0:2]:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0], v0[1], -10]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
        vertices1.append(np.array(v2))

    shape = cbh.hull_from_points(vertices1)
    return shape

# def getHexGrid():
#     return [ ( 0,6 ),(0, -1),(0, -8),
#             ( 6,9.5 ),(6, 2.5),(6, -4.5),(6, -11.5),(6, -18.5),(6, -25),
#             ( -6,9.5 ),(-6, 2.5),(-6, -4.5),
#             ( -12,6 ),(-12, -1),
#             ( 12,6 ),(12, -1),(12, -8),(12, -15)]

def getHexGrid():
   return [ ( 0,6 ),(0, -1),(0, -8),(0, -15),(0, -22),(0, -29),
           ( 6,9.5 ),(6, 2.5),(6, -4.5),(6, -11.5),(6, -18.5),(6, -25),
           ( -6,9.5 ),(-6, 2.5),(-6, -4.5),(-6, -25),
           ( -12,6 ),(-12, -1),
           ( 12,6 ),(12, -1),(12, -8),(12, -15)]

# def getHexGrid():
#    return [ ( 0,6 ),(0, -1),(0, -8),(0, -15),(0, -22),(0, -29),
#            ( 6,9.5 ),(6, 2.5),(6, -4.5),(6, -11.5),(6, -18.5),(6, -25),
#            ( -6,9.5 ),(-6, 2.5),(-6, -4.5),(-6, -11.5),(-6, -18.5),(-6, -25),
#            ( -12,6 ),(-12, -1),(-12, -8),(-12, -15),
#            ( 12,6 ),(12, -1),(12, -8),(12, -15)]