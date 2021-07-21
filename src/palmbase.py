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
import palmbasehelpers as pbh

def palm_position(position, transform):
    return pbh.apply_palm_geometry(position, transform, cbh.post_translate, cbh.rotate_around_x, cbh.rotate_around_y, cbh.rotate_around_z)

def palm_wall_brace_left(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_left(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_left(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_left(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_left(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_left(dx2, dy2))))
    shape2 = pbh.palm_bottom_hull_left(hulls)

    return shape1.union(shape2)

def palm_wall_brace_left_to_default(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_left(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_left(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_left(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_left(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_left(dx2, dy2))))
    shape2 = pbh.palm_bottom_hull_left_to_default(hulls)

    return shape1.union(shape2)

def palm_wall_brace_position(transform1, dx1, dy1, post1, transform2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: palm_position(shape, transform1)),
        dx1,
        dy1,
        post1,
        (lambda shape: palm_position(shape, transform2)),
        dx2,
        dy2,
        post2,
    )

def palm_wall_brace_left_position(transform1, dx1, dy1, post1, transform2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return palm_wall_brace_left(
        (lambda shape: palm_position(shape, transform1)),
        dx1,
        dy1,
        post1,
        (lambda shape: palm_position(shape, transform2)),
        dx2,
        dy2,
        post2,
    )

def palm_wall_brace_left_position_to_default(transform1, dx1, dy1, post1, transform2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return palm_wall_brace_left_to_default(
        (lambda shape: palm_position(shape, transform1)),
        dx1,
        dy1,
        post1,
        (lambda shape: palm_position(shape, transform2)),
        dx2,
        dy2,
        post2,
    )