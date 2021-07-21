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
import displaybase as db

def wall_brace_left_to_joystick(place1, dx1, dy1, post1, place2, dx2, dy2, post2, place3, dx3, dy3, post3):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))

    hulls.append(place2(post2))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))
    hulls.append(place2(post2))
    hulls.append(place3(post3))
    shape2 = cjbh.bottom_hull_left_to_joystick(hulls)

    return shape1.union(shape2)

def wall_brace_left_bottom_to_wall_brace(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))
    
    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3(dx2, dy2))))

    shape1 = cjbh.bottom_hull_left_bottom_to_wall_brace(hulls)

    return shape1

def wall_brace_thin_to_default(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_thin_extended_to_default(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_extended(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_extended(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def thumb_wall_brace_post_position_to_joystick_position(x1, y1, dx1, dy1, post1, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: tb.thumb_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: jb.joystick_position(shape)),
        dx2,
        dy2,
        post2,
    )

def thumb_wall_brace_joystick_position_to_joystick_position(dx1, dy1, post1, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: jb.joystick_position(shape)),
        dx1,
        dy1,
        post1,
        (lambda shape: jb.joystick_position(shape)),
        dx2,
        dy2,
        post2,
    )

def wall_brace_display_position_to_joystick_position(dx1, dy1, post1, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: db.display_position(shape)),
        dx1,
        dy1,
        post1,
        (lambda shape: jb.joystick_position(shape)),
        dx2,
        dy2,
        post2,
    )