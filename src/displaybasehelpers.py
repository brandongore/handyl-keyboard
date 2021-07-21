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

def apply_display_geometry(shape, translate_fn, rotate_x_fn, rotate_y_fn, rotate_z_fn):
    xrad = cbh.deg2rad(cp.display_rotation[0])  
    yrad = cbh.deg2rad(cp.display_rotation[1]) 
    zrad = cbh.deg2rad(cp.display_rotation[2]) 
    
    shape = rotate_y_fn(shape, yrad)
    shape = rotate_x_fn(shape, xrad)
    shape = rotate_z_fn(shape, zrad)

    shape = translate_fn(shape, cp.display_offset)

    return shape

#########################
## Joystick Connectors ##
#########################

def display_post():
    #print('web_post()')
    p1 = [0,0,cp.web_thickness/2]
    p2 = [0,0,-cp.web_thickness/2]
    
    toppoint = cbh.add_translate(p1, (0, 0, 0))
    bottompoint = cbh.add_translate(p2, (0, 0, 0))
    post = [toppoint,bottompoint]

    return post

displaypost = display_post()

def display_web_post_tr():
    post = displaypost
    return cbh.post_translate(post, ((cp.display_width/2)- cp.display_horizontal_adj, (cp.display_length / 2)- cp.display_horizontal_adj, cp.display_height / 2 -(cp.web_thickness / 2) - cp.display_vertical_adj))

def display_web_post_tl():
    post = displaypost
    return cbh.post_translate(post, (-(cp.display_width/2)+ cp.display_horizontal_adj, (cp.display_length / 2)- cp.display_horizontal_adj, cp.display_height / 2 -(cp.web_thickness / 2)- cp.display_vertical_adj))
                      
def display_web_post_bl():
    post = displaypost
    return cbh.post_translate(post, (-(cp.display_width/2)+ cp.display_horizontal_adj, -(cp.display_length / 2)+ cp.display_horizontal_adj, cp.display_height / 2 -(cp.web_thickness / 2)- cp.display_vertical_adj))

def display_web_post_br():
    post = displaypost
    return cbh.post_translate(post, ((cp.display_width/2)- cp.display_horizontal_adj, -(cp.display_length / 2) + cp.display_horizontal_adj, cp.display_height / 2 -(cp.web_thickness / 2)- cp.display_vertical_adj))

# def display_web_post_tr():
#     post = displaypost
#     return cbh.post_translate(post, ((cp.display_width/2)-(cp.mount_width / 2) , (cp.display_length / 2) - cp.display_adj, (cp.display_height / 2) - cp.display_adj))

# def display_web_post_tl():
#     post = displaypost
#     return cbh.post_translate(post, ((cp.display_width/2)-(cp.mount_width / 2) , (cp.display_length / 2) - cp.display_adj, -(cp.display_height / 2) + cp.display_adj))
                      
# def display_web_post_bl():
#     post = displaypost
#     return cbh.post_translate(post, ((cp.display_width/2)-(cp.mount_width / 2) , -(cp.display_length / 2) + cp.display_adj, -(cp.display_height / 2) + cp.display_adj))

# def display_web_post_br():
#     post = displaypost
#     return cbh.post_translate(post, ((cp.display_width/2)-(cp.mount_width / 2) , -(cp.display_length / 2) + cp.display_adj, (cp.display_height / 2) - cp.display_adj))


# def display_post_tr_to_tl():
#     post = displaypost
#     return cbh.post_translate(post, ((cp.display_width/2)- cp.display_horizontal_adj, ((cp.display_length / 2) - cp.display_adj), (-cp.display_adj)))

# def display_post_tl_to_bl():
#     post = displaypost
#     return cbh.post_translate(post, ((cp.display_width/2)- cp.display_horizontal_adj, (-cp.display_adj), (-(cp.display_height / 2) + cp.display_adj)))
                      
# def display_post_bl_to_br():
#     post = displaypost
#     return cbh.post_translate(post, ((cp.display_width/2)- cp.display_horizontal_adj, (-(cp.display_length / 2) + cp.display_adj), (cp.display_adj)))

# def display_post_br_to_tr():
#     post = displaypost
#     return cbh.post_translate(post, ((cp.display_width/2)- cp.display_horizontal_adj, (cp.display_adj), ((cp.display_height / 2) - cp.display_adj)))

# def web_post_tr():
#     post = wbpost
#     return cbh.post_translate(post, ((cp.mount_width / 2) - cp.post_adj, (cp.mount_height / 2) - cp.post_adj, 0))

# def web_post_tl():
#     post = wbpost
#     return cbh.post_translate(post, (-(cp.mount_width / 2) + cp.post_adj, (cp.mount_height / 2) - cp.post_adj, 0))
        
# def web_post_bl():
#     post = wbpost
#     return cbh.post_translate(post, (-(cp.mount_width / 2) + cp.post_adj, -(cp.mount_height / 2) + cp.post_adj, 0))

# def web_post_br():
#     post = wbpost
#     return cbh.post_translate(post, ((cp.mount_width / 2) - cp.post_adj, -(cp.mount_height / 2) + cp.post_adj, 0))





displaywebpostbr = display_web_post_br()
displaywebposttr = display_web_post_tr()
displaywebpostbl = display_web_post_bl()
displaywebposttl = display_web_post_tl()

# displaypostbrtotr = display_post_br_to_tr()
# displayposttrtotl = display_post_tr_to_tl()
# displaypostbltobr = display_post_bl_to_br()
# displayposttltobl = display_post_tl_to_bl()
