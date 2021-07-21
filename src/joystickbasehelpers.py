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

def apply_joystick_geometry(shape, translate_fn, rotate_x_fn, rotate_y_fn, rotate_z_fn):
    xrad = cbh.deg2rad(cp.joystick_rotation[0])  
    yrad = cbh.deg2rad(cp.joystick_rotation[1]) 
    zrad = cbh.deg2rad(cp.joystick_rotation[2]) 
    
    shape = rotate_y_fn(shape, yrad)
    shape = rotate_z_fn(shape, zrad)
    shape = rotate_x_fn(shape, xrad)

    shape = translate_fn(shape, cp.joystick_offset)

    return shape

#########################
## Joystick Connectors ##
#########################

def joystick_post():
    #print('web_post()')
    p1 = [cp.web_thickness/2,0,0]
    p2 = [-cp.web_thickness/2,0,0]
    
    toppoint = cbh.add_translate(p1, (cp.plate_thickness - (cp.web_thickness / 2), 0, 0))
    bottompoint = cbh.add_translate(p2, (cp.plate_thickness - (cp.web_thickness / 2), 0, 0))
    post = [toppoint,bottompoint]

    return post

def joystick_web_post_tr():
    post = joypost
    return cbh.post_translate(post, ((cp.joystick_height/2)-(cp.mount_height / 2) + 5, (cp.joystick_width / 2) - cp.joy_adj, (cp.joystick_length / 2) - cp.joy_adj))

def joystick_web_post_tl():
    post = joypost
    return cbh.post_translate(post, ((cp.joystick_height/2)-(cp.mount_height / 2) + 5, (cp.joystick_width / 2) - cp.joy_adj, -(cp.joystick_length / 2) + cp.joy_adj))
                      
def joystick_web_post_bl():
    post = joypost
    return cbh.post_translate(post, ((cp.joystick_height/2)-(cp.mount_height / 2) + 5, -(cp.joystick_width / 2) + cp.joy_adj, -(cp.joystick_length / 2) + cp.joy_adj))

def joystick_web_post_br():
    post = joypost
    return cbh.post_translate(post, ((cp.joystick_height/2)-(cp.mount_height / 2) + 5, -(cp.joystick_width / 2) + cp.joy_adj, (cp.joystick_length / 2) - cp.joy_adj))

def joystick_post_tr_to_tl():
    post = joypost
    return cbh.post_translate(post, ((cp.joystick_height/2)-(cp.mount_height / 2) + 5, ((cp.joystick_width / 2) - cp.joy_adj), (-cp.joy_adj)))

def joystick_post_tl_to_bl():
    post = joypost
    return cbh.post_translate(post, ((cp.joystick_height/2)-(cp.mount_height / 2) + 5, (-cp.joy_adj), (-(cp.joystick_length / 2) + cp.joy_adj)))
                      
def joystick_post_bl_to_br():
    post = joypost
    return cbh.post_translate(post, ((cp.joystick_height/2)-(cp.mount_height / 2) + 5, (-(cp.joystick_width / 2) + cp.joy_adj), (cp.joy_adj)))

def joystick_post_br_to_tr():
    post = joypost
    return cbh.post_translate(post, ((cp.joystick_height/2)-(cp.mount_height / 2) + 5, (cp.joy_adj), ((cp.joystick_length / 2) - cp.joy_adj)))

joypost = joystick_post()

joystickwebpostbr = joystick_web_post_br()
joystickwebposttr = joystick_web_post_tr()
joystickwebpostbl = joystick_web_post_bl()
joystickwebposttl = joystick_web_post_tl()

joystickpostbrtotr = joystick_post_br_to_tr()
joystickposttrtotl = joystick_post_tr_to_tl()
joystickpostbltobr = joystick_post_bl_to_br()
joystickposttltobl = joystick_post_tl_to_bl()
