###### import cadquery as cq
from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from cqkit import *

import numpy as np
import coreparameters as cp
import corebasehelpers as cbh

def column_offset(column: int) -> list:
    # print('column_offset()')
    if column == 0:
        return cp.column_zero_offset
    elif column == 1:
        return cp.column_one_offset
    elif column == 2:
        return cp.column_two_offset
    elif column == 3:
        return cp.column_three_offset
    else:
        return cp.column_default_offset

def apply_key_geometry(
        shape,
        translate_fn,
        rotate_x_fn,
        rotate_y_fn,
        rotate_z_fn,
        column,
        row,
        column_style=cp.column_style,
):
    #print('apply_key_geometry()')
    column_angle = cp.beta * (cp.centercol - column)

    if column_style == "orthographic":
        column_z_delta = cp.column_radius * (1 - np.cos(column_angle))
        shape = translate_fn(shape, [0, 0, -cp.row_radius])
        shape = rotate_x_fn(shape, cp.alpha * (cp.centerrow - row))
        shape = translate_fn(shape, [0, 0, cp.row_radius])
        shape = rotate_y_fn(shape, column_angle)
        shape = translate_fn(
            shape, [-(column - cp.centercol) * cp.column_x_delta, 0, column_z_delta]
        )
        shape = translate_fn(shape, column_offset(column))

    elif column_style == "fixed":
        shape = rotate_y_fn(shape, cp.fixed_angles[column])
        shape = translate_fn(shape, [cp.fixed_x[column], 0, cp.fixed_z[column]])
        shape = translate_fn(shape, [0, 0, -(cp.row_radius + cp.fixed_z[column])])
        shape = rotate_x_fn(shape, cp.alpha * (cp.centerrow - row))
        shape = translate_fn(shape, [0, 0, cp.row_radius + cp.fixed_z[column]])
        shape = rotate_y_fn(shape, cp.fixed_tenting)
        shape = translate_fn(shape, [0, column_offset(column)[1], 0])

    else:
        shape = translate_fn(shape, [0, 0, -cp.row_radius])
        shape = rotate_x_fn(shape, cp.alpha * (cp.centerrow - row))
        shape = translate_fn(shape, [0, 0, cp.row_radius])
        
        shape = translate_fn(shape, [0, 0, -cp.column_radius])
        shape = rotate_y_fn(shape, column_angle)
        shape = translate_fn(shape, [0, 0, cp.column_radius])
        
        shape = translate_fn(shape, column_offset(column))   

        if column == 0:
            shape = rotate_x_fn(shape, 0.23)#check
            shape = rotate_y_fn(shape, -0.06)#check
            shape = rotate_z_fn(shape, 0.046)
            
        if column == 2:
            shape = rotate_z_fn(shape, -0.049)
            shape = rotate_y_fn(shape, 0.091)
        if column == 3:          
            shape = rotate_y_fn(shape, 0.44)
            shape = rotate_z_fn(shape, -0.11)
            if row == 2 or row == 3:
                shape = translate_fn(shape, [-6.7, 3.5, -8.8])  
                shape = rotate_x_fn(shape, 0.58)
                shape = rotate_z_fn(shape, 0.02)
                
            if row == 0:
                shape = translate_fn(shape, [-8.15, -5.8, -7.0]) 
                shape = rotate_x_fn(shape, -0.05)
                shape = rotate_y_fn(shape, 0.023)
                shape = rotate_z_fn(shape, 0.10)
                                    

            if row == 1:
                shape = translate_fn(shape, [-7.0, -1.2, -6.8])    
                shape = rotate_x_fn(shape, 0.007)
                shape = rotate_y_fn(shape, 0.005)              
                shape = rotate_z_fn(shape, 0.11)
    
    tentrad = cbh.deg2rad(cp.tenting_angle)
    
    shape = rotate_y_fn(shape, tentrad)
    shape = translate_fn(shape, cp.keyboard_offset)
    #shape = rotate_y_fn(shape, -0.5)
    #shape = rotate(shape, [0, 44.9, 0])
    #shape = rotate(shape, [0, -1, 0])
    #shape = rotatedshape

    return shape

##########
## Case ##
##########

def bottom_hull_left(p, height=0.001):
    shape = None
    vertices = []
    for item in p:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0] - 60, v0[1], -10]
        vertices.append(np.array(v0))
        vertices.append(np.array(v1))
        vertices.append(np.array(v2))

    t_shape = cbh.hull_from_points(vertices)
    shape = t_shape 
    return shape

def bottom_hull_left_to_thin(p, height=0.001):
    shape = None
    vertices1 = []
    vertices2 = []
    subp = p[2:]
    for item in subp:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0] - 60, v0[1], -10]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
        vertices1.append(np.array(v2))
    
    for item in p[0:2]:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0] - 60, v0[1], -10]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
        vertices1.append(np.array(v2))
    
    for item in subp:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0], v0[1], -10]
        vertices2.append(np.array(v0))
        vertices2.append(np.array(v1))
        vertices2.append(np.array(v2))
        
    for item in subp:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0] - 60, v0[1], -10]
        vertices2.append(np.array(v0))
        vertices2.append(np.array(v1))
        vertices2.append(np.array(v2))

    t_shape1 = cbh.hull_from_points(vertices1)
    t_shape2 = cbh.hull_from_points(vertices2)
    shape = t_shape1 
    shape = shape.union(t_shape2)
    
    return shape

def bottom_hull_left_flat(p, height=0.001):
    shape = None
    vertices1 = []
    vertices2 = []
    subp = p[4:]
    
    p1 = subp[0][0]
    p2 = subp[0][1]
    
    p3 = subp[1][0]
    p4 = subp[1][1]
    
    v0 = [p1[0],p1[1],p1[2]]
    v1 = [p2[0],p2[1],p2[2]]
    v2 = [v0[0] - 60, v0[1], -10]
    vertices1.append(np.array(v0))
    vertices1.append(np.array(v1))
    vertices1.append(np.array(v2))
    
    v0 = [p3[0],p3[1],p3[2]]
    v1 = [p4[0],p4[1],p4[2]]
    v2 = [v0[0] - 60, v0[1], -10]
    vertices1.append(np.array(v0))
    vertices1.append(np.array(v1))
    vertices1.append(np.array(v2))

    for item in p[1:3]:
        v0 = [item[0][0],item[0][1],item[0][2]]
        v1 = [item[1][0],item[1][1],item[1][2]]
        v2 = [v0[0] - 60, v0[1], -10]
        vertices1.append(np.array(v0))
        vertices1.append(np.array(v1))
        vertices1.append(np.array(v2))

    v0 = [p1[0]+3,p1[1],p1[2]]
    v1 = [p2[0]+3,p2[1],p2[2]]
    v2 = [v0[0] - 60, v0[1], -10]

    vertices2.append(np.array(v0))
    vertices2.append(np.array(v1))
    vertices2.append(np.array(v2))

    v0 = [p1[0]+3,p1[1]+1,p1[2]]
    v1 = [p2[0]+3,p2[1]+1,p2[2]]
    v2 = [v0[0] - 60, v0[1]+1, -10]

    vertices2.append(np.array(v0))
    vertices2.append(np.array(v1))
    vertices2.append(np.array(v2))

    v4 = [p3[0],p3[1],p3[2]]
    v0 = [p4[0]+3.43,p4[1],p4[2]]
    v1 = [p4[0]+3.1,p4[1],-10]
    v2 = [v4[0] - 60+0.2, v4[1], -10]

    vertices2.append(np.array(v0))
    vertices2.append(np.array(v1))
    vertices2.append(np.array(v2))
    
    v4 = [p3[0],p3[1]+1,p3[2]]
    v0 = [p4[0]+3.43,p4[1]+1,p4[2]]
    v1 = [p4[0]+3.1,p4[1]+1,-10]
    v2 = [v4[0] - 60+0.2, v4[1]+1, -10]

    vertices2.append(np.array(v0))
    vertices2.append(np.array(v1))
    vertices2.append(np.array(v2))
  
    for item in p[3:4]:
        v0 = [item[0][0]+0.3,item[0][1],item[0][2]+0.20]
        v1 = [item[1][0]+0.3,item[1][1],item[1][2]+0.20]
        v2 = [v0[0] - 60, v0[1], -10]

        vertices2.append(np.array(v0))
        vertices2.append(np.array(v1))
        vertices2.append(np.array(v2))
        
        v0 = [item[0][0]+0.3,item[0][1]+1,item[0][2]+0.20]
        v1 = [item[1][0]+0.3,item[1][1]+1,item[1][2]+0.20]
        v2 = [v0[0] - 60, v0[1]+1, -10]

        vertices2.append(np.array(v0))
        vertices2.append(np.array(v1))
        vertices2.append(np.array(v2))

    t_shape1 = cbh.hull_from_points(vertices1)
    t_shape2 = cbh.hull_from_points(vertices2)
    shape = t_shape1 
    shape = shape.union(t_shape2)
    
    return shape
