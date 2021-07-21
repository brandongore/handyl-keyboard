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
import joystickbasehelpers as jbh

def joystick_position(position):
    return jbh.apply_joystick_geometry(position, cbh.post_translate, cbh.rotate_around_x, cbh.rotate_around_y, cbh.rotate_around_z)

def joystick_position_single(position):
    return jbh.apply_joystick_geometry(position, cbh.add_translate, cbh.rotate_around_x_single, cbh.rotate_around_y_single, cbh.rotate_around_z_single)

def thumb_wall_brace_joystick_position_to_joystick_position(dx1, dy1, post1, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: joystick_position(shape)),
        dx1,
        dy1,
        post1,
        (lambda shape: joystick_position(shape)),
        dx2,
        dy2,
        post2,
    )