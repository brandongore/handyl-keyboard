###### import cadquery as cq
from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from cqkit import *
import numpy as np

import keybasehelpers as kbh
import coreparameters as cp
import corebasehelpers as cbh
import corebase as cb

def key_place(shape, column, row):
    #print('key_place() col: ' + str(column) + 'row: ' + str(row))
    return kbh.apply_key_geometry(shape, cbh.translate, cbh.x_rot, cbh.y_rot, cbh.z_rot, column, row)

def key_position(position, column, row):
    #print('key_position()')
    return kbh.apply_key_geometry(position, cbh.post_translate, cbh.rotate_around_x, cbh.rotate_around_y, cbh.rotate_around_z, column, row)

def key_position_single(position, column, row):
    #print('key_position()')
    return kbh.apply_key_geometry(position, cbh.add_translate, cbh.rotate_around_x_single, cbh.rotate_around_y_single, cbh.rotate_around_z_single, column, row)
              
def left_key_position(row, direction):
    pos = np.array(
        key_position_single([-cp.mount_width * 0.5, direction * cp.mount_height * 0.5, 0], 0, row)
    )
    return list(pos - np.array([cp.left_wall_x_offset, 0, cp.left_wall_z_offset]))

def right_key_position(column, row, direction):
    #print("left_key_position()")
    pos = np.array(
        key_position_single([cp.mount_width * 0.5, direction * cp.mount_height * 0.5, 0], column, row)
    )
    return list(pos + np.array([5, 0, -3]))

def left_key_place(shape, row, direction):
    #print("left_key_place()")
    pos = left_key_position(row, direction)
    return cbh.post_translate(shape, pos) 

def left_key_place_single(shape, row, direction):
    #print("left_key_place()")
    pos = left_key_position(row, direction)
    return cbh.add_translate(shape, pos)                       

def right_key_place(shape, column, row, direction):
    #print("left_key_place()")
    pos = right_key_position(column, row, direction)
    return cbh.post_translate(shape, pos)  

def right_key_place_single(shape, column, row, direction):
    #print("left_key_place()")
    pos = right_key_position(column, row, direction)
    return cbh.add_translate(shape, pos)  

def any_key_position(column, row, direction, offset):
    #print("left_key_position()")
    pos = np.array(
        key_position_single([cp.mount_width * 0.5, direction *cp.mount_height * 0.5, 0], column, row)
    )
    return list(pos + offset)

def any_key_position_left(column, row, direction, offset):
    #print("left_key_position()")
    pos = np.array(
        key_position_single([-cp.mount_width * 0.5, direction *cp.mount_height * 0.5, 0], column, row)
    )
    return list(pos - offset)

def any_key_place_left(shape, column, row, direction, offset):
    shape = key_position(shape, column, row)
    
    return cbh.post_translate(shape, offset)  

def any_key_place(shape, column, row, direction, offset):
    #print("left_key_place()")
    pos = any_key_position(column, row, direction, offset)
    return cbh.post_translate(shape, pos)                        


def wall_brace_thin(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_thin(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_thin_extended(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_thin_extended(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_extended(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_extended(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_extended(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_extended(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_extended(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_extended(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_thin_to_thin_extended(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_thin(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_extended(dx2, dy2))))
    
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_extended(dx2, dy2))))
    
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_thin_back(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin_back(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_back(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_back(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_back(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_back(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_thin_back_extended(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_thin_back_extended(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back_extended(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back_extended(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin_back_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_back_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_back_extended(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back_extended(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back_extended(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_back_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_back_extended(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_thin_back_to_thin_back_extended(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin_back_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_back_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_back_extended(dx2, dy2))))
    
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_back_extended(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_back_extended(dx2, dy2))))
    
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_short(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_short(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_short(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_short(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_short(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_short(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_short(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_short(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_short_to_default(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_short(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_short(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_thin_to_default_low(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_low(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_low(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_low(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin_low(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_low(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_low(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_low(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_low(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_low(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_low(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_short_to_thin(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_thin(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_short(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_short(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_short_to_thin_back(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_short(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_short(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_short(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)

def wall_brace_left_to_thin(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin(dx2, dy2))))
    shape2 = kbh.bottom_hull_left_to_thin(hulls)

    return shape1.union(shape2)

def wall_brace_left_to_thin_back(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_thin_back(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_back(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_back(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_thin_back(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_thin_back(dx2, dy2))))
    shape2 = kbh.bottom_hull_left_to_thin(hulls)

    return shape1.union(shape2)

def wall_brace_left_to_default(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
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
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_left(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_left(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2_left(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3_left(dx2, dy2))))
    shape2 = kbh.bottom_hull_left_flat(hulls)

    return shape1.union(shape2)

def wall_brace_left_flat(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
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
    shape2 = kbh.bottom_hull_left_flat(hulls)

    return shape1.union(shape2)

def wall_brace_left(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
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
    shape2 = kbh.bottom_hull_left(hulls)

    return shape1.union(shape2)

def key_wall_brace(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: key_place(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: key_place(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )

def key_wall_brace_position(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return cb.wall_brace(
        (lambda shape: key_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: key_position(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )

def key_wall_brace_position_thin(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return wall_brace_thin(
        (lambda shape: key_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: key_position(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )

def key_wall_brace_position_thin_extended(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return wall_brace_thin_extended(
        (lambda shape: key_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: key_position(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )

def key_wall_brace_position_thin_to_thin_extended(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return wall_brace_thin_to_thin_extended(
        (lambda shape: key_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: key_position(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )

def key_wall_brace_position_thin_back(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return wall_brace_thin_back(
        (lambda shape: key_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: key_position(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )

def key_wall_brace_position_thin_back_extended(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return wall_brace_thin_back_extended(
        (lambda shape: key_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: key_position(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )

def key_wall_brace_position_thin_back_to_thin_back_extended(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    #print("key_wall_brace()")
    return wall_brace_thin_back_to_thin_back_extended(
        (lambda shape: key_position(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: key_position(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )

    
