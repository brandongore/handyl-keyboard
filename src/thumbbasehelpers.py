from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from cqkit import *
import numpy as np
from numpy import pi

import keybase as kb
import keybasehelpers as kbh
import coreparameters as cp
import corebasehelpers as cbh
import corebase as cb
import joystickbase as jb
import clusterjoinbasehelpers as cjbh
import thumbbase as tb
import thumbbasehelpers as tbh

def apply_thumb_geometry(
        shape,
        translate_fn,
        rotate_x_fn,
        rotate_y_fn,
        rotate_z_fn,
        column,
        row,
        column_style=cp.column_style,
):
    column_angle = cp.beta

    thumb_row_angle = pi / 5
    thumb_row_radius = ((cp.mount_height + cp.extra_height) / 2) / (np.sin(thumb_row_angle / 2)) + cp.cap_top_height -1.3
    rowdiff = 1.5 - row

    shape = translate_fn(shape, [0, 0, -thumb_row_radius])
    
    if column == 1 :   
        if row == 0:
            shape = shape
            shape = rotate_z_fn(shape, cp.alpha * -0.3)
            shape = shape
            shape = rotate_x_fn(shape, cp.alpha * -0.9)
    
    if column == 0 :   
        if row == 0:
            shape = shape
            shape = rotate_z_fn(shape, cp.alpha * 0.076)
        else:
            shape = rotate_z_fn(shape, thumb_row_angle * row * 0.042)
        
    
    shape = rotate_x_fn(shape, thumb_row_angle * (1.5 - row))
    
    shape = translate_fn(shape, [0, 0, thumb_row_radius])
    
    shape = translate_fn(shape, [0, 0, -cp.column_radius])
    
    if column == 1 :
        shape = rotate_z_fn(shape, 0.35)

    shape = translate_fn(shape, [0, 0, cp.column_radius])  
    
    if column == 0 :        
        if(row == 0):
            shape = translate_fn(shape, [0, 1.6, 0])
        if(row == 1):
            shape = translate_fn(shape, [0, 0, 0])
        if(row == 2):
            shape = translate_fn(shape, [0, -1.2, 0])    
        if(row == 3):
            shape = translate_fn(shape, [0, -1.2, 0]) 
    
    if column == 1 :
        if(row == 0):
            shape = shape
            shape = rotate_y_fn(shape, 0.4 * cp.alpha)
            shape = translate_fn(shape, [-22, 12, 13])
    
    if column == 0 :  
        if row == 0:
            shape = shape
            shape = rotate_y_fn(shape, 0.05 * cp.alpha)
        else:
            shape = shape

    if row == 1:
        shape = translate_fn(shape, [(1.19), 0, 0])
    
    if row > 1 and row < 3:
        shape = translate_fn(shape, [(1.19 * row), 0, 0])
        
    if row == 3:
        shape = translate_fn(shape, [(1.3 * row), 0, 0])

    xrad = cbh.deg2rad(30)  
    yrad = cbh.deg2rad(-5) 
    zrad = cbh.deg2rad(289) 
    
    shape = rotate_x_fn(shape, xrad)
    shape = rotate_y_fn(shape, yrad)
    shape = rotate_z_fn(shape, zrad)

    shape = translate_fn(shape, [-49, -57.2, 23.6])

    return shape

def apply_symmetric_thumb_geometry(
        shape,
        translate_fn,
        rotate_x_fn,
        rotate_y_fn,
        rotate_z_fn,
        column,
        row,
        column_style=cp.column_style,
):
    column_angle = cp.beta

    rowdiff = 1.5 - row
    #print(rowdiff)
    shape = translate_fn(shape, [0, 0, -cp.row_radius])
    if np.absolute(rowdiff) > 0.5:
        
        shape = rotate_z_fn(shape, cp.alpha * (1.5 - row)* 1.8)
        shape = rotate_x_fn(shape, 0.15 * (1.5 - row))
    else:
        shape = rotate_z_fn(shape, cp.alpha * (1.5 - row)* 1.1)
        shape = rotate_x_fn(shape, 0.01 * (1.5 - row))
        
    shape = rotate_x_fn(shape, cp.alpha * (1.5 - row))
    shape = translate_fn(shape, [0, 0, cp.row_radius])
    
    shape = translate_fn(shape, [0, 0, -cp.column_radius])
   
    shape = translate_fn(shape, [0, 0, cp.column_radius])  
    
    
    if np.absolute(rowdiff) > 0.5:
        shape = rotate_y_fn(shape, -0.119)
        shape = translate_fn(shape, [-(20 * (np.absolute(1.5 - row))), 0, 0])
        shape = translate_fn(shape, [0, -(7 * (1.5 - row)), 0])
        shape = translate_fn(shape, [0, 0, -(15.7 * np.absolute(1.5 - row))])
    else:
        shape = rotate_y_fn(shape, -1)
        shape = translate_fn(shape, [0, (1.4 * (1.5 - row)), 0])
        shape = translate_fn(shape, [-(12 * (np.absolute(1.5 - row))), 0, 0])

    return shape


#######################
## Thumbs Connectors ##
#######################

def thumborigin():
    # print('thumborigin()')
    origin = kb.key_position([cp.mount_width / 2, -(cp.mount_height / 2), 0], 1, cp.cornerrow)
    for i in range(len(origin)):
        origin[i] = origin[i] + cp.thumb_offsets[i]
    return origin

def thumb_tr_place(shape):
    #print('thumb_tr_place()')
    shape = cbh.rotate(shape, [10, -23, 10])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-12, -16, 3])
    return shape

def thumb_tl_place(shape):
    #print('thumb_tl_place()')
    shape = cbh.rotate(shape, [10, -23, 10])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-32, -15, -2])
    return shape

def thumb_mr_place(shape):
    #print('thumb_mr_place()')
    shape = cbh.rotate(shape, [-6, -34, 48])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-29, -40, -13])
    return shape

def thumb_ml_place(shape):
    #print('thumb_ml_place()')
    shape = cbh.rotate(shape, [6, -34, 40])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-51, -25, -12])
    return shape

def thumb_br_place(shape):
    #print('thumb_br_place()')
    shape = cbh.rotate(shape, [-16, -33, 54])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-37.8, -55.3, -25.3])
    return shape

def thumb_bl_place(shape):
    #print('thumb_bl_place()')
    shape = cbh.rotate(shape, [-4, -35, 52])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-56.3, -43.3, -23.5])
    return shape

def thumb_post_tr():
    #print('thumb_post_tr()')
    post = cb.wbpost
    return cbh.post_translate(post, ((cp.mount_width / 2) - cp.post_adj, -(cp.mount_height / 2) - cp.post_adj, 0))

def thumb_post_tl():
    #print('thumb_post_tl()')
    post = cb.wbpost
    return cbh.post_translate(post, ((cp.mount_width / 2) + cp.post_adj, -(cp.mount_height / 2) - cp.post_adj, 0))

def thumb_post_bl():
    #print('thumb_post_bl()')
    post = cb.wbpost
    return cbh.post_translate(post, ((cp.mount_width / 2) + cp.post_adj, -(cp.mount_height / 2) + cp.post_adj, 0))

def thumb_post_br():
    #print('thumb_post_br()')
    post = cb.wbpost
    return cbh.post_translate(post, ((cp.mount_width / 2) - cp.post_adj, -(cp.mount_height / 2) + cp.post_adj, 0))
