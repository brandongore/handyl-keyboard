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
import thumbbasehelpers as tbh

def thumb_place(shape, column, row):
    #print('key_place()')
    return tbh.apply_thumb_geometry(shape, cbh.translate, cbh.x_rot, cbh.y_rot, cbh.z_rot, column, row)

def thumb_position(position, column, row):
    #print('key_position()')
    return tbh.apply_thumb_geometry(position, cbh.post_translate, cbh.rotate_around_x, cbh.rotate_around_y, cbh.rotate_around_z, column, row)

def thumb_position_single(position, column, row):
    #print('thumb_position_single()')
    print('thumb_position_single() before', str(position))
    pos =  tbh.apply_thumb_geometry(position, cbh.add_translate, cbh.rotate_around_x_single, cbh.rotate_around_y_single, cbh.rotate_around_z_single, column, row)
    print('thumb_position_single() after', str(pos))
    return pos

def thumb_1x_layout(shape, cap=False):
    #print('thumb_1x_layout()')
    if cap:
        shapes = tbh.thumb_mr_place(shape)
        shapes = shapes.add(tbh.thumb_ml_place(shape))
        shapes = shapes.add(tbh.thumb_br_place(shape))
        shapes = shapes.add(tbh.thumb_bl_place(shape))
    else:
        shapes = cbh.union(
            [
                tbh.thumb_mr_place(shape),
                tbh.thumb_ml_place(shape),
                tbh.thumb_br_place(shape),
                tbh.thumb_bl_place(shape),
            ]
        )
    return shapes

def thumb_15x_layout(shape, cap=False):
    print('thumb_15x_layout()')
    if cap:
        shape = cbh.rotate(shape, (0, 0, 90))
        return tbh.thumb_tr_place(shape).add(tbh.thumb_tl_place(shape).solids().objects[0])
    else:
        return tbh.thumb_tr_place(shape).union(tbh.thumb_tl_place(shape))

def thumb():
    #print('thumb()')
    shape = thumb_1x_layout(cb.single_plate())
    shape = shape.union(thumb_15x_layout(cb.single_plate()))
    shape = shape.union(thumb_15x_layout(cb.double_plate()))
    return shape

def thumb_wall_brace_position(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: thumb_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: thumb_position(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )

def thumb_wall_brace_position_to_cartesian(x1, y1, dx1, dy1, post1, xyz, xryrzr, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: thumb_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: cbh.web_post_position(shape, xyz, xryrzr)),
        dx2,
        dy2,
        post2,
    )

def thumb_wall_brace_position_to_post_position(x1, y1, dx1, dy1, post1, transform, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: thumb_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: cbh.web_post_position(shape, transform.translation, transform.rotation)),
        dx2,
        dy2,
        post2,
    )

def thumb_wall_brace_post_position_to_post_position(transform1, dx1, dy1, post1, transform2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: cbh.web_post_position(shape, transform1.translation, transform1.rotation)),
        dx1,
        dy1,
        post1,
        (lambda shape: cbh.web_post_position(shape, transform2.translation, transform2.rotation)),
        dx2,
        dy2,
        post2,
    )
