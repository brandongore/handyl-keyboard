from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from jupyter_cadquery import set_sidecar, set_defaults, reset_defaults
from cqkit import *

import numpy as np
from numpy import pi
import thumbbase as tb
import keybase as kb
import corebase as cb
import corebasehelpers as cbh
import coreparameters as cp
import clusterjoinbase as cjb
import clusterjoinbasehelpers as cjbh
import joystickbase as jb
import joystickbasehelpers as jbh
import displaybase as db
import displaybasehelpers as dbh

# screw_insert_height = 3.8
# screw_insert_bottom_radius = 5.31 / 2
# screw_insert_top_radius = 5.1 / 2

screw_insert_height = 5.85 # +1.2
screw_insert_bottom_radius = 8.96 / 2 # +0.8
screw_insert_top_radius = 8.75 / 2 # +0.8

def final_assembly(mod_r, thumb_r, joystick_r, display_r):
    shape = cq.Workplane('XY')
    shape = shape.union(mod_r, tol=.01)
    shape = shape.union(thumb_r, tol=.01)
    shape = shape.union(joystick_r, tol=.01)
    shape = shape.union(display_r, tol=.01)
    s2 = cq.Workplane('XY').union(key_to_display_wall(), tol=.01)
    s2 = s2.union(key_to_thumb_wall(), tol=.01)
    s2 = s2.union(joystick_to_thumb_wall(), tol=.01)
    



    # # s3 = cq.Workplane('XY')
    # # screw_insert_outers = screw_insert_all_shapes(
    # # screw_insert_bottom_radius + 1.6,
    # # screw_insert_top_radius + 1.6,
    # # screw_insert_height + 1.5,
    # # True
    # # )




    s3 = cq.Workplane('XY')
    screw_insert_outers = screw_insert_all_shapes(
    screw_insert_bottom_radius + 1.8,
    screw_insert_top_radius + 1.8,
    screw_insert_height + 1.7,
    True
    )

    s3 = cbh.union([s3, *screw_insert_outers])
    shape = shape.union(s2, tol=.01)
    shape = shape.union(s3, tol=.01)
    block = cq.Workplane("XY").box(350, 350, 40)
    block = block.translate((0, 0, -20))
    shape = shape.cut(block)
    
    return shape

def final_assembly_processed(final):
    # screw_insert_hole_height = 5.7
    # screw_insert_hole_bottom_radius = 8.51 / 2
    # screw_insert_hole_top_radius = 8.3 / 2

    screw_insert_hole_height = 5.1 # +1.2
    screw_insert_hole_bottom_radius = 4.88 / 2 # +0.8
    screw_insert_hole_top_radius = 4.88 / 2# +0.8

    screw_insert_holes = screw_insert_all_shapes(
    screw_insert_hole_bottom_radius, screw_insert_hole_top_radius, screw_insert_hole_height
    )
    #screw_insert_nut_holes = screw_insert_all_nut_shapes(5)

    screw_insert_nut_holes = screw_insert_all_nut_shapes(4.7)


    finalprocessed = final.union(connector_cube())
    finalprocessed = finalprocessed.cut(cbh.union(screw_insert_holes))
    finalprocessed = finalprocessed.cut(cbh.union(screw_insert_nut_holes))
    finalprocessed = finalprocessed.cut(rj45_cutter())
    #finalprocessed = finalprocessed.cut(rj45_holder())
    finalprocessed = finalprocessed.cut(micro_controller_cutter())

    finalprocessed = finalprocessed.cut(palm_rest_to_key_screwholes())
    #finalprocessed = finalprocessed.cut(mc_hole())
    
    return finalprocessed
    #return rj45_cutter()
    #return final

    # s2 = s2.union(teensy_holder())
    # s2 = s2.union(usb_holder())

    # s2 = s2.cut(rj9_space())
    # s2 = s2.cut(usb_holder_hole())
    # s2 = s2.cut(union(screw_insert_holes))

    # shape = shape.union(rj9_holder())
    #s2 = union([s2, *screw_insert_outers])

def screw_test():
    screw_insert_height = 5.7 # +1.2
    screw_insert_bottom_radius = 8.51 / 2 # +0.8
    screw_insert_top_radius = 8.3 / 2 # +0.8

    screw_insert_hole_height = 5 # +1.2
    screw_insert_hole_bottom_radius = 4.88 / 2 # +0.8
    screw_insert_hole_top_radius = 4.88 / 2# +0.8
    screw_insert_holes = screw_insert_all_shapes(
    screw_insert_hole_bottom_radius, screw_insert_hole_top_radius, screw_insert_hole_height
    )
    screw_insert_nut_holes = screw_insert_all_nut_shapes(4.7) # -0.3

    shape =cq.Workplane('XY')

    s3 = cq.Workplane('XY')
    screw_insert_outers = screw_insert_all_shapes(
    screw_insert_bottom_radius + 1.8,
    screw_insert_top_radius + 1.8,
    screw_insert_height + 1.7,
    True
    )

    s3 = cbh.union([s3, *screw_insert_outers])
    shape = shape.union(s3, tol=.01)

    shape = shape.cut(cbh.union(screw_insert_holes))
    shape = shape.cut(cbh.union(screw_insert_nut_holes))
    return shape


def bottom_plate_processed(bottom_plate):
    screw_insert_bolt_height = 0
    screw_insert_bolt_bottom_radius = 4.08 / 2
    screw_insert_bolt_top_radius = 4.08 / 2

    screw_insert_bolt_holes = screw_insert_all_bolt_shapes(
    screw_insert_bolt_bottom_radius, screw_insert_bolt_top_radius, screw_insert_bolt_height
    )

    bottom_plate_processed = bottom_plate.cut(cbh.union(screw_insert_bolt_holes))

    # finalprocessed = finalprocessed.cut(rj45_cutter())
    # #finalprocessed = finalprocessed.cut(rj45_holder())
    # finalprocessed = finalprocessed.cut(micro_controller_cutter())
    # #finalprocessed = finalprocessed.cut(mc_hole())
    
    return bottom_plate_processed

def palm_rest_to_key_screwholes():
    shape = cq.Workplane("XZ").circle(2.04).extrude(28)
    shape = cbh.rotate(shape, (0,0,18))
    shape = shape.translate((-9.8, -44.5, 30))
    return shape

def connector_cube():
    shape = cq.Workplane("XY").box(90, 6, 30).edges("|Z ").fillet(2.5).faces(">Z").fillet(2.5)
    shape = shape.translate((-22, 0, -(45-30)/2))
    shape = shape.translate(connector_cube_position)
    return shape

connector_cube_start = list(
    np.array([0, 0, 0])
    + np.array(
        kb.left_key_place_single(
            list(np.array(cb.wall_locate2_thin_back(0, 2.4)) + np.array([0, 0, 0])),
            0,
            1,
        )
    )
)

connector_cube_position = (connector_cube_start[0], connector_cube_start[1], 22.5)

rj45_start = list(
    np.array([0, 0, 0])
    # + np.array(
    #     kb.left_key_place_single(
    #         list(np.array(cb.wall_locate2_thin_back(0, 1)) + np.array([0, 0, 0])),
    #         0,
    #         1,
    #     )
    # )
)

rj45_position = (rj45_start[0], rj45_start[1], 41/2)
 


rj45_cutter_start = list(
    np.array([0, 0, 0])
    + np.array(
        kb.left_key_place_single(
            list(np.array(cb.wall_locate2_thin_back(-8.6, -0.7)) + np.array([0, 0, 0])),
            0,
            1,
        )
    )
)

rj45_cutter_position = (rj45_cutter_start[0], rj45_cutter_start[1], 15)
rj45_cutter_rotation = (0, -90, 0)

def rj45_cube():
    print('rj45_cube()')
    #shape = cq.Workplane("XY").box(11.70, 21, 8.3)
    shape = cq.Workplane("XY").box(15.7, 28.07, 41)

    return shape


def rj45_space():
    print('rj45_space()')
    return rj45_cube().translate(rj45_position)

def rj45_hole():
    shape = cq.Workplane("XY").box(13.46, 30.24, 16.08).translate((1.14, (28.07-8.24)/2 + 3.6, 0))
    return shape

def rj45_connector_screws():
    shape = cq.Workplane("YZ").rect(14.85,21.41, forConstruction=True).vertices().circle(1.51).extrude(15.73)
    #8.28 + 0.2
    #5.37
    shape = shape.translate((-15.73/2, 1.71, 0))
    return shape

def rj45_connector_chip():
    shape = cq.Workplane("XY").box(1.8, 28.07, 33)
    #8.28 + 0.2
    #5.37
    shape = shape.translate((15.7/2 +1.8/2, 0, 0))
    return shape

def rj45_connector_tolerance():
    cube1 = cq.Workplane("XY").box(0.6, 28.07, 41)
    cube1 = cube1.translate((-15.7/2 -0.6/2, 0, 0))

    cube2 = cq.Workplane("XY").box(0.6, 28.07, 41)
    cube2 = cube2.translate((15.7/2 +0.6/2, 0, 0))

    cube3 = cq.Workplane("XY").box(15.7 + 1.2, 28.07, 0.45)
    cube3 = cube3.translate((0, 0, 41/2 + 0.45/2))

    cube4 = cq.Workplane("XY").box(15.7 + 1.2, 28.07, 0.45)
    cube4 = cube4.translate((0, 0, -41/2 - 0.45/2))

    shape = cq.Workplane("XY")
    shape = shape.union(cube1)
    shape = shape.union(cube2)
    shape = shape.union(cube3)
    shape = shape.union(cube4)
    
    return shape

def rj45_wall_screws():
    hole1 = cq.Workplane("XZ").circle(2.04).extrude(48.1)
    hole2 = cq.Workplane("XZ").circle(2.04).extrude(48.1)

    screw_recess1 = cq.Workplane("XZ").cone(3.71, 2.025,2.75)
    screw_recess2 = cq.Workplane("XZ").cone(3.71, 2.025,2.75)

    hole1 = hole1.translate((0, 60/2, 16.5))
    hole2 = hole2.translate((0, 60/2, -16.5))

    screw_recess1 = screw_recess1.translate((0, 45/2-3.95, 16.5))
    screw_recess2 = screw_recess2.translate((0, 45/2-3.95, -16.5))


    #8.28 + 0.2
    #5.37
    shape = cq.Workplane("XZ")
    shape = shape.union(hole1)
    shape = shape.union(hole2)
    shape = shape.union(screw_recess1)
    shape = shape.union(screw_recess2)

    shape = shape.translate((0, 0, 0))
    return shape

def rj45_wire_space():
    shape = cq.Workplane("XY").box(4, 9.1, 14.2).translate((5.9, -9.5, 0))
    return shape

def rj45_holder():
    print('rj45_holder()')
    shape = rj45_hole()
    #shape = shape.union(cq.Workplane("XY").box(10.78, 13, 5).translate((0, 0, 5)))
    shape = rj45_cube().cut(shape)
    shape = shape.cut(rj45_connector_screws())
    shape = shape.cut(rj45_wall_screws())
    shape = shape.cut(rj45_wire_space())
    shape = shape.translate(rj45_position)

    return shape

def rj45_cutter():
    shape = cq.Workplane("XY")
    shape = rj45_hole()
    #shape = shape.union(cq.Workplane("XY").box(10.78, 13, 5).translate((0, 0, 5)))
    shape = rj45_cube().cut(shape)
    shape = shape.union(rj45_connector_screws())
    shape = shape.union(rj45_wall_screws())
    shape = shape.union(rj45_wall_screws())
    shape = shape.union(rj45_hole())
    shape = shape.union(rj45_connector_chip())
    shape = shape.union(rj45_connector_tolerance())
    shape = cbh.rotate(shape, rj45_cutter_rotation)
    shape = shape.translate(rj45_cutter_position)
    
    return shape


usb_holder_position = kb.key_position_single(
    list(np.array(cb.wall_locate2(0, 1)) + np.array([0, (3.8 / 2), 0])), 1, 0
)
usb_holder_size = [6.5, 10.0, 13.6]
usb_holder_thickness = 4


def usb_holder():
    print('usb_holder()')
    shape = cq.Workplane("XY").box(
        usb_holder_size[0] + usb_holder_thickness,
        usb_holder_size[1],
        usb_holder_size[2] + usb_holder_thickness,
    )
    shape = shape.translate(
        (
            usb_holder_position[0],
            usb_holder_position[1],
            (usb_holder_size[2] + usb_holder_thickness) / 2,
        )
    )
    return shape


def usb_holder_hole():
    print('usb_holder_hole()')
    shape = cq.Workplane("XY").box(*usb_holder_size)
    shape = shape.translate(
        (
            usb_holder_position[0],
            usb_holder_position[1],
            (usb_holder_size[2] + usb_holder_thickness) / 2,
        )
    )
    return shape


teensy_width = 20
teensy_height = 12
teensy_length = 33
teensy2_length = 53
teensy_pcb_thickness = 2
teensy_holder_width = 7 + teensy_pcb_thickness
teensy_holder_height = 6 + teensy_width
teensy_offset_height = 5
teensy_holder_top_length = 18
teensy_top_xy = kb.key_position_single(cb.wall_locate3(-1, 0), 0, cp.centerrow - 1)
teensy_bot_xy = kb.key_position_single(cb.wall_locate3(-1, 0), 0, cp.centerrow + 1)
teensy_holder_length = teensy_top_xy[1] - teensy_bot_xy[1]
teensy_holder_offset = -teensy_holder_length / 2
teensy_holder_top_offset = (teensy_holder_top_length / 2) - teensy_holder_length

def micro_controller_cube():
    print('mc_cube()')
    #shape = cq.Workplane("XY").box(11.70, 21, 8.3)
    shape = cq.Workplane("XY").box(10, 39, 38)

    return shape

    #+ (3.03) + (5.8-3.03)/2 

    #

def micro_controller_hole(chip_clip=False, top_holder_tab=False):
    #3.73 bottom pin height to top of processor  3.9   -> 5.8   3.03
    shape = cq.Workplane("XY").box(5.8, 34.94, 20.91).translate((-(10-5.8)/2, (39-34.94)/2, 0))
    bottom_holder = cq.Workplane("XY").box((5.8-2.43), 1.88, 20.91).translate((-(((10-5.8))/2 -5.8/2 + (5.8-2.43)/2 + 2.43), (39-34.94)/2 - (34.94 - 1.88)/2, 0))
    if top_holder_tab == True:
        top_holder = cq.Workplane("XY").box((5.8-2.43), 1.3, 0.7).fillet(0.349).translate((-(((10-5.8))/2 -5.8/2 + (5.8-2.43)/2 + 2.43), (39-34.94)/2 + (34.94 - 1.3)/2, (-20.91 )/2))
        shape = shape.cut(top_holder)
    shape = shape.cut(bottom_holder)
    
    if chip_clip == True:
        chip_holder = cq.Workplane("XY").box((5.8-3.57), 15, 2.5).translate((-(((10-5.8))/2 -5.8/2 + (5.8-3.57)/2 + 3.57), (39-34.94)/2 - (34.94 - 15)/2, 0))
        shape = shape.cut(chip_holder)

    return shape



def micro_controller_holder():
    shape = cq.Workplane("XY")
    shape = micro_controller_cube()
    shape = shape.cut(micro_controller_hole(True, True))
    shape = shape.cut(micro_controller_wall_screws())
    shape = shape.translate(micro_controller_cutter_position)
    return shape

micro_controller_start = list(
    np.array([0, 0, 0])
    + np.array(
        kb.left_key_place_single(
            list(np.array(cb.wall_locate2_thin_back(-2.65, -4)) + np.array([0, 0, 0])),
            0,
            1,
        )
    )
)

micro_controller_position = (micro_controller_start[0], micro_controller_start[1], 38/2)

micro_controller_cutter_start = list(
    np.array([0, 0, 0])
    + np.array(
        kb.left_key_place_single(
            list(np.array(cb.wall_locate2_thin_back(0, -1.7)) + np.array([0, 0, 0])),
            0,
            1,
        )
    )
)

micro_controller_cutter_rotation = (0, 90, 0)

micro_controller_cutter_position = (micro_controller_cutter_start[0], micro_controller_cutter_start[1], 14.9)

def micro_controller_wall_screws():
    
    hole1 = cq.Workplane("XZ").circle(2.04).extrude(55)
    hole2 = cq.Workplane("XZ").circle(2.04).extrude(55)

    screw_recess1 = cq.Workplane("XZ").cone(3.71, 2.025,2.75)
    screw_recess2 = cq.Workplane("XZ").cone(3.71, 2.025,2.75)

    hole1 = hole1.translate((0, 60/2, 14.5))
    hole2 = hole2.translate((0, 60/2, -14.5))

    screw_recess1 = screw_recess1.translate((0, 45/2+1.1, 14.5))
    screw_recess2 = screw_recess2.translate((0, 45/2+1.1, -14.5))
    #8.28 + 0.2
    #5.37
    shape = cq.Workplane("XZ")
    
    shape = shape.union(hole1)
    shape = shape.union(hole2)
    shape = shape.union(screw_recess1)
    shape = shape.union(screw_recess2)
    shape = shape.translate((0, 0, 0))
    return shape

def micro_controller_connector_hole():
    center_cube = cq.Workplane("XZ").box(2.55, 7.51, 20).fillet(1).translate((-(((10-5.8))/2 -5.8/2 + 2.55/2 + 3.03), (39-34.94)/2 + (34.94)/2 + 2, 0))
    shape = cq.Workplane("XZ")
    shape = shape.union(center_cube)
    shape = shape.translate((0, 0, 0))
    return shape

def micro_controller_connector_cable_hole():
    center_cube = cq.Workplane("XZ").box(7.6, 10.95, 20).fillet(1).translate((-(((10-5.8))/2 -5.8/2 + 2.55/2 + 3.03), (39-34.94)/2 + (34.94)/2 + 10.8, 0))
    shape = cq.Workplane("XZ")
    shape = shape.union(center_cube)
    shape = shape.translate((0, 0, 0))
    return shape
    #7.15  10.8

def micro_controller_tolerance():
    cube1 = cq.Workplane("XY").box(0.5, 39, 38)
    cube1 = cube1.translate((-10/2 -0.5/2, 0, 0))

    cube2 = cq.Workplane("XY").box(0.5, 39, 38)
    cube2 = cube2.translate((10/2 +0.5/2, 0, 0))

    cube3 = cq.Workplane("XY").box(10 + 1, 39, 0.4)
    cube3 = cube3.translate((0, 0, 38/2 + 0.3/2))

    cube4 = cq.Workplane("XY").box(10 + 1, 39, 0.4)
    cube4 = cube4.translate((0, 0, -38/2 - 0.3/2))

    shape = cq.Workplane("XY")
    shape = shape.union(cube1)
    shape = shape.union(cube2)
    shape = shape.union(cube3)
    shape = shape.union(cube4)
    
    return shape

def micro_controller_reset_hole_cutter():
    hole = cq.Workplane("XZ").circle(1.75).extrude(55)
    hole = hole.translate((10/2 +7.2/2, 60/2, 0))

    recess = cq.Workplane("XZ").box(8.4,9.4,39)
    recess = recess.translate((10/2 +9.4/2, 0, 0))

    shape = cq.Workplane("XZ")
    shape = shape.union(hole)
    shape = shape.union(recess)
    shape = shape.translate((0, 0, 0))
    return shape

def micro_controller_reset_holder():
    holder = cq.Workplane("XZ").box(9.2,8.2,39)
    holder = holder.translate((10/2 +9.2/2, 0, 0))

    clip = cq.Workplane("XZ").box(6.2,6.2,3.9)
    clip = clip.translate((10/2 +(9.2)/2, (39-3.9)/2, (8.2-6.2)/2))

    top_pin_cut = cq.Workplane("XZ").box(9.2,1.5,3.9)
    top_pin_cut = top_pin_cut.translate((10/2 +9.2/2, (39-3.9)/2, (8.2-1.5)/2))

    bottom_pin_cut = cq.Workplane("XZ").box(9.2,1.65,3.9)
    bottom_pin_cut = bottom_pin_cut.translate((10/2 +9.2/2, (39-3.9)/2, (8.2-6.2)/2 - (6.2-1.65)/2))

    shape = cq.Workplane("XZ")
    shape = shape.union(holder)
    shape = shape.cut(clip)
    shape = shape.cut(top_pin_cut)
    shape = shape.cut(bottom_pin_cut)
    shape = shape.translate((0, 0, 0))
    return shape

def micro_controller_cutter():
    shape = cq.Workplane("XY")
    shape = micro_controller_cube()
    #shape = shape.union(cq.Workplane("XY").box(10.78, 13, 5).translate((0, 0, 5)))
    #shape = shape.cut(micro_controller_hole())
    # shape = shape.cut(rj45_connector_screws())
    shape = shape.union(micro_controller_connector_hole())
    shape = shape.union(micro_controller_connector_cable_hole())
    shape = shape.union(micro_controller_wall_screws())
    shape = shape.union(micro_controller_tolerance())
    shape = shape.union(micro_controller_reset_hole_cutter())
    # shape = shape.union(rj45_wall_screws())
    # shape = shape.union(rj45_hole())
    shape = cbh.rotate(shape, micro_controller_cutter_rotation)
    shape = shape.translate(micro_controller_cutter_position)
    
    return shape

def screw_insert_shape(bottom_radius, top_radius, height):
    #print('screw_insert_shape()')
    if bottom_radius == top_radius:
        base = cq.Workplane('XY').union(cq.Solid.makeCylinder(radius=bottom_radius, height=height)).translate(
            (0, 0, -height / 2)
        )
    else:
        base = cq.Workplane('XY').union(
            cq.Solid.makeCone(radius1=bottom_radius, radius2=top_radius, height=height)).translate((0, 0, -height / 2))

    shape = cbh.union((
        base,
        cq.Workplane('XY').union(cq.Solid.makeSphere(top_radius)).translate((0, 0, (height / 2))),
    ))
    return shape

def screw_insert_nut_shape(rotation_angle):
    #print('screw_insert_nut_shape()')

    nut_width = 8.706
    nut_height = 5.6
    opening_width = 8.706

    base = cq.Workplane('XY').polygon(6, nut_width).extrude(nut_height)
    base_extended = cq.Workplane('XY').polygon(6, nut_width).extrude(nut_height).translate((-1.18, 0, 0))
    opening = cq.Workplane('XY').box(opening_width, nut_width-1.106, nut_height).translate((opening_width/2, 0, nut_height/2))

    shape = cbh.union((
        base,
        base_extended,
        opening,
    ))
    shape = cbh.rotate(shape, (0,0,rotation_angle))

    return shape

def screw_insert_bolt_shape(bottom_radius, top_radius, height):
    shape = cq.Workplane("XY").cone(3.71, 2.025,2.75)#.cutBlind(2.0, True)
    return shape

def screw_insert_bolt(screw_position, wall_locate, dx, dy, bottom_radius, top_radius, height):
    #print('screw_insert()')

    p1 =  list(np.array(wall_locate(dx, dy)))
    print(str(p1))
    position = screw_position(p1)

    # cbh.add_translate(position, cb.wall_locate1_thin_back(0, 1))

    shape = screw_insert_bolt_shape(bottom_radius, top_radius, height)
    
    shape = shape.translate((position[0], position[1], height / 2))

    return shape

def screw_insert_nut(screw_position, wall_locate, dx, dy, height, rotation_angle):
    print('screw_insert_nut()')
    # shift_right = column == cp.lastcol
    # shift_left = column == 0
    # shift_up = (not (shift_right or shift_left)) and (row == 0)
    # shift_down = (not (shift_right or shift_left)) and (row >= cp.lastrow)

    # if shift_up:
    #     position = kb.key_position_single(
    #         list(np.array(cb.wall_locate2(0, 1)) + np.array([0, (cp.mount_height / 2), 0])),
    #         column,
    #         row,
    #     )
    # elif shift_down:
    #     position = kb.key_position_single(
    #         list(np.array(cb.wall_locate2(0, -1)) - np.array([0, (cp.mount_height / 2), 0])),
    #         column,
    #         row,
    #     )
    # elif shift_left:
    #     #position = list(
    #     #    np.array(left_key_position(row, 0)) + np.array(wall_locate3(-1, 0))
    #     #)
    #     position = kb.key_position_single(
    #         list(np.array(cb.wall_locate2(1, 0)) + np.array([(cp.mount_height / 2), 0, 0])),
    #         column,
    #         row,
    #     )
    # else:
    p1 =  list(np.array(wall_locate(dx, dy)))
    print(str(p1))
    position = screw_position(p1)

    # cbh.add_translate(position, cb.wall_locate1_thin_back(0, 1))

    shape = screw_insert_nut_shape(rotation_angle)
    
    shape = shape.translate((position[0], position[1], height / 2))

    return shape

def screw_insert(screw_position, wall_locate, dx, dy, bottom_radius, top_radius, height):
    #print('screw_insert()')

    p1 =  list(np.array(wall_locate(dx, dy)))
    print(str(p1))
    position = screw_position(p1)

    # cbh.add_translate(position, cb.wall_locate1_thin_back(0, 1))

    shape = screw_insert_shape(bottom_radius, top_radius, height)
    
    shape = shape.translate((position[0], position[1], height / 2))

    return shape


# def screw_insert_all_shapes(bottom_radius, top_radius, height, is_outer = False):
#     shape = (
#         screw_insert((lambda shape: kb.key_position_single(shape, 1, 3)), (lambda dx1, dy1:  cb.wall_locate2_thin(dx1, dy1)), 2.5, -1.25, bottom_radius, top_radius, height),
#         screw_insert((lambda shape: kb.right_key_place_single(shape, 3, 2, 1)), (lambda dx1, dy1:  cb.wall_locate2_short(dx1, dy1)), -0.5, 2.75, (bottom_radius + 1.1 if is_outer == True else bottom_radius), top_radius, height-0.4 if is_outer == True else height),
#         screw_insert((lambda shape: kb.key_position_single(shape, 2, 0)), (lambda dx1, dy1:  cb.wall_locate2_thin_back(dx1, dy1)), -0.5, 1.1, bottom_radius, top_radius, height),
#         screw_insert((lambda shape: kb.left_key_place_single(shape, 0, 1)), (lambda dx1, dy1:  cb.wall_locate2_thin_back(dx1, dy1)), -9, 0.5, bottom_radius, top_radius, height),
#         screw_insert((lambda shape: jb.joystick_position_single(shape)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), 5.35, -3.2, bottom_radius, top_radius, height),
#         screw_insert((lambda shape: tb.thumb_position_single(shape, 0, 1)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), 2, -4, bottom_radius, top_radius, height),
#         screw_insert((lambda shape: db.display_position_single(shape)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), -9, -5, bottom_radius, top_radius, height),
#     )

#     return shape

# def screw_insert_all_nut_shapes(height, is_outer = False):
#     shape = (
#         screw_insert_nut((lambda shape: kb.key_position_single(shape, 1, 3)), (lambda dx1, dy1:  cb.wall_locate2_thin(dx1, dy1)), 2.5, -1.25, height, 105),
#         screw_insert_nut((lambda shape: kb.right_key_place_single(shape, 3, 2, 1)), (lambda dx1, dy1:  cb.wall_locate2_short(dx1, dy1)), -0.5, 2.75, height-0.4 if is_outer == True else height, 180),
#         screw_insert_nut((lambda shape: kb.key_position_single(shape, 2, 0)), (lambda dx1, dy1:  cb.wall_locate2_thin_back(dx1, dy1)), -0.5, 1.1, height, -90),
#         screw_insert_nut((lambda shape: kb.left_key_place_single(shape, 0, 1)), (lambda dx1, dy1:  cb.wall_locate2_thin_back(dx1, dy1)), -9, 0.5, height, -90),
#         screw_insert_nut((lambda shape: jb.joystick_position_single(shape)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), 5.35, -3.2, height, 0),
#         screw_insert_nut((lambda shape: tb.thumb_position_single(shape, 0, 1)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), 2, -4, height, 105),
#         screw_insert_nut((lambda shape: db.display_position_single(shape)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), -9, -5, height, 0),
#     )

#     return shape

# def screw_insert_all_bolt_shapes(bottom_radius, top_radius, height, is_outer = False):
#     shape = (
#         screw_insert_bolt((lambda shape: kb.key_position_single(shape, 1, 3)), (lambda dx1, dy1:  cb.wall_locate2_thin(dx1, dy1)), 2.5, -1.25, bottom_radius, top_radius, height),
#         screw_insert_bolt((lambda shape: kb.right_key_place_single(shape, 3, 2, 1)), (lambda dx1, dy1:  cb.wall_locate2_short(dx1, dy1)), -0.5, 2.75, bottom_radius, top_radius, height-0.4 if is_outer == True else height),
#         screw_insert_bolt((lambda shape: kb.key_position_single(shape, 2, 0)), (lambda dx1, dy1:  cb.wall_locate2_thin_back(dx1, dy1)), -0.5, 1.1, bottom_radius, top_radius, height),
#         screw_insert_bolt((lambda shape: kb.left_key_place_single(shape, 0, 1)), (lambda dx1, dy1:  cb.wall_locate2_thin_back(dx1, dy1)), -9, 0.5, bottom_radius, top_radius, height),
#         screw_insert_bolt((lambda shape: jb.joystick_position_single(shape)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), 5.35, -3.2, bottom_radius, top_radius, height),
#         screw_insert_bolt((lambda shape: tb.thumb_position_single(shape, 0, 1)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), 2, -4, bottom_radius, top_radius, height),
#         screw_insert_bolt((lambda shape: db.display_position_single(shape)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), -9, -5, bottom_radius, top_radius, height),
#     )

#     return shape

sc1param = [(lambda shape: kb.key_position_single(shape, 1, 3)), (lambda dx1, dy1:  cb.wall_locate2_thin(dx1, dy1)), 0.02, -1.65, 105]
sc2param = [(lambda shape: kb.right_key_place_single(shape, 3, 2, 1)), (lambda dx1, dy1:  cb.wall_locate2_short(dx1, dy1)), -1.2, 3.8, 180]
sc3param = [(lambda shape: kb.key_position_single(shape, 2, 0)), (lambda dx1, dy1:  cb.wall_locate2_thin_back(dx1, dy1)), -2.0, 1.55, -90]
sc4param = [(lambda shape: kb.left_key_place_single(shape, 0, 1)), (lambda dx1, dy1:  cb.wall_locate2_thin_back(dx1, dy1)), -16, 1.25, -90]
sc5param = [(lambda shape: jb.joystick_position_single(shape)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), 4.75, -5.1, 0]
sc6param = [(lambda shape: tb.thumb_position_single(shape, 0, 1)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), 1.85, -3.4, 105]
sc7param = [(lambda shape: db.display_position_single(shape)), (lambda dx1, dy1:  cb.wall_locate2(dx1, dy1)), -8.6, -5.25, 0]

def screw_insert_all_shapes(bottom_radius, top_radius, height, is_outer = False):
    shape = (
        screw_insert(sc1param[0], sc1param[1],sc1param[2],sc1param[3],bottom_radius, top_radius, height),
        screw_insert(sc2param[0], sc2param[1],sc2param[2],sc2param[3],(bottom_radius + 1.1 if is_outer == True else bottom_radius), top_radius, height-0.4 if is_outer == True else height),
        screw_insert(sc3param[0], sc3param[1],sc3param[2],sc3param[3],bottom_radius, top_radius, height),
        screw_insert(sc4param[0], sc4param[1],sc4param[2],sc4param[3],bottom_radius, top_radius, height),
        screw_insert(sc5param[0], sc5param[1],sc5param[2],sc5param[3],bottom_radius, top_radius, height),
        screw_insert(sc6param[0], sc6param[1],sc6param[2],sc6param[3],bottom_radius, top_radius, height),
        screw_insert(sc7param[0], sc7param[1],sc7param[2],sc7param[3],bottom_radius, top_radius, height),
    )

    return shape

def screw_insert_all_nut_shapes(height, is_outer = False):
    shape = (
        screw_insert_nut(sc1param[0], sc1param[1],sc1param[2],sc1param[3],height, 105),
        screw_insert_nut(sc2param[0], sc2param[1],sc2param[2],sc2param[3],height-0.4 if is_outer == True else height, 180),
        screw_insert_nut(sc3param[0], sc3param[1],sc3param[2],sc3param[3],height, -90),
        screw_insert_nut(sc4param[0], sc4param[1],sc4param[2],sc4param[3],height, -90),
        screw_insert_nut(sc5param[0], sc5param[1],sc5param[2],sc5param[3],height, 30),
        screw_insert_nut(sc6param[0], sc6param[1],sc6param[2],sc6param[3],height, 105),
        screw_insert_nut(sc7param[0], sc7param[1],sc7param[2],sc7param[3],height, 0),
    )

    return shape

def screw_insert_all_bolt_shapes(bottom_radius, top_radius, height, is_outer = False):
    shape = (
        screw_insert_bolt(sc1param[0], sc1param[1],sc1param[2],sc1param[3],bottom_radius, top_radius, height),
        screw_insert_bolt(sc2param[0], sc2param[1],sc2param[2],sc2param[3],bottom_radius, top_radius, height-0.4 if is_outer == True else height),
        screw_insert_bolt(sc3param[0], sc3param[1],sc3param[2],sc3param[3],bottom_radius, top_radius, height),
        screw_insert_bolt(sc4param[0], sc4param[1],sc4param[2],sc4param[3],bottom_radius, top_radius, height),
        screw_insert_bolt(sc5param[0], sc5param[1],sc5param[2],sc5param[3],bottom_radius, top_radius, height),
        screw_insert_bolt(sc6param[0], sc6param[1],sc6param[2],sc6param[3],bottom_radius, top_radius, height),
        screw_insert_bolt(sc7param[0], sc7param[1],sc7param[2],sc7param[3],bottom_radius, top_radius, height),
    )

    return shape

def between_position(shape, func1, func2):
    p1 = np.array(func1(shape)) 
    print(str(p1))
    p2 = np.array(func2(shape))
    print(str(p2))
    r1 = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2]
    print(str(r1))
    return list(r1)



# screw_insert_holes = screw_insert_all_shapes(
#     screw_insert_bottom_radius, screw_insert_top_radius, screw_insert_height
# )
# screw_insert_outers = screw_insert_all_shapes(
#     screw_insert_bottom_radius + 1.6,
#     screw_insert_top_radius + 1.6,
#     screw_insert_height + 1.5,
#     True
# )
screw_insert_screw_holes = screw_insert_all_shapes(1.7, 1.7, 350)

def key_to_display_wall():
    shape = cq.Workplane('XY')

     

    shape = shape.union(wall_brace_thin_back_to_display(
        (lambda sh: kb.left_key_place(sh, 0, 1)),
        0,
        2,
        cb.wbpost,
        (lambda sh: db.display_position(sh)),
        0,
        1,
        dbh.displaywebposttl,
    ))

    temp_shape2 = cbh.hull_from_shapes((
        db.display_position(dbh.displaywebposttl),
        kb.left_key_place(cb.wbpost, 0, 1),
        kb.left_key_place(cb.wbpost, 0, -1),
    ))
    shape = shape.union(temp_shape2)

    temp_shape3 = cbh.hull_from_shapes((
        db.display_position(dbh.displaywebposttr),
        db.display_position(dbh.displaywebposttl),
        kb.left_key_place(cb.wbpost, 1, 1),
        kb.left_key_place(cb.wbpost, 0, -1),
    ))
    shape = shape.union(temp_shape3)

    temp_shape4 = cbh.hull_from_shapes((
        db.display_position(dbh.displaywebposttr),
        kb.left_key_place(cb.wbpost, 1, 1),
        kb.left_key_place(cb.wbpost, 1, -1),
    ))
    shape = shape.union(temp_shape4)

    temp_shape5 = cbh.hull_from_shapes((
        db.display_position(dbh.displaywebposttr),
        db.display_position(dbh.displaywebpostbr),
        kb.left_key_place(cb.wbpost, 2, 1),
        kb.left_key_place(cb.wbpost, 1, -1),
    ))
    shape = shape.union(temp_shape5)

    temp_shape6 = cbh.hull_from_shapes((
        db.display_position(dbh.displaywebpostbr),
        kb.left_key_place(cb.wbpost, 2, 1),
        jb.joystick_position(jbh.joystickwebpostbr),
    ))
    shape = shape.union(temp_shape6)

    temp_shape7 = cbh.hull_from_shapes((
        db.display_position(dbh.displaywebpostbr),
        jb.joystick_position(jbh.joystickwebpostbr),
        jb.joystick_position(jbh.joystickwebpostbl),
    ))
    shape = shape.union(temp_shape7)

    temp_shape8 = cbh.hull_from_shapes((
        db.display_position(dbh.displaywebpostbr),
        db.display_position(dbh.displaywebpostbl),
        jb.joystick_position(jbh.joystickwebpostbl),
    ))
    shape = shape.union(temp_shape8)
    
    shape = shape.union(cjb.wall_brace_display_position_to_joystick_position(-0.5, -2, dbh.displaywebpostbl, 0, -1.5, jbh.joystickwebpostbl))

    shape = shape.union(db.display_wall_brace_position(-1, -1, dbh.displaywebpostbl, -0.5, -2, dbh.displaywebpostbl))

    # shape = shape.union(kb.wall_brace_left(
    #     (lambda sh: kb.left_key_place(sh, 0, 1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    #     (lambda sh: kb.left_key_place(sh, 0, -1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    # ))

    return shape

def key_to_thumb_wall():
    shape = cq.Workplane('XY')

    shape = shape.union(cjb.wall_brace_thin_extended_to_default(
        (lambda sh: tb.thumb_position(sh, 0, 0)),
        1.25, 
        0.25,
        cb.webposttr,
        (lambda sh: kb.left_key_place(sh, cp.cornerrow, -1)),
        3,
        -1.9,
        cb.wbpost,
    ))
    
    temp_shape2 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webposttl, 0, 0),
        tb.thumb_position(cb.webposttr, 0, 0),
        kb.left_key_place(cb.wbpost, 3, -1),
    ))
    shape = shape.union(temp_shape2)
    
    temp_shape2 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webposttl, 0, 0),
        tb.thumb_position(cb.webposttr, 1, 0),
        kb.left_key_place(cb.wbpost, 3, 1),
        kb.left_key_place(cb.wbpost, 3, -1),
    ))
    shape = shape.union(temp_shape2)
    
    temp_shape2 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webposttl, 1, 0),
        tb.thumb_position(cb.webposttr, 1, 0),
        kb.left_key_place(cb.wbpost, 3, 1),
        kb.left_key_place(cb.wbpost, 2, -1),
    ))
    shape = shape.union(temp_shape2)
    
    temp_shape2 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webposttl, 1, 0),
        kb.left_key_place(cb.wbpost, 2, 1),
        kb.left_key_place(cb.wbpost, 2, -1),
    ))
    shape = shape.union(temp_shape2)
    
    temp_shape2 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webposttl, 1, 0),
        tb.thumb_position(cb.webpostbl, 1, 0),
        kb.left_key_place(cb.wbpost, 2, 1),
    ))
    shape = shape.union(temp_shape2)
    
    temp_shape2 = cbh.hull_from_shapes((
        jb.joystick_position(jbh.joystickwebpostbr),
        tb.thumb_position(cb.webpostbl, 1, 0),
        kb.left_key_place(cb.wbpost, 2, 1),
    ))
    shape = shape.union(temp_shape2)
    
    # y = cp.lastrow - 2
    # temp_shape1 = cjb.wall_brace_left_to_joystick(
    #     (lambda sh: kb.left_key_place(sh, y - 1, -1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    #     (lambda sh: jb.joystick_position(sh)),
    #     -1,
    #     0,
    #     jbh.joystickwebpostbr,
    #     (lambda sh: jb.joystick_position(sh)),
    #     -1,
    #     0,
    #     jbh.joystickwebpostbl
    # )
    # shape = shape.union(temp_shape1)
    
    # y = cp.lastrow - 2
    # temp_shape1 = cjb.wall_brace_left_bottom_to_wall_brace(
    #     (lambda sh: kb.left_key_place(sh, y - 1, -1)),
    #     -1,
    #     0,
    #     cb.wbpost,
    #     (lambda sh: jb.joystick_position(sh)),
    #     0, 
    #     -1.5,
    #     jbh.joystickwebpostbl
    # )
    # shape = shape.union(temp_shape1)

    return shape

def joystick_to_thumb_wall():
    shape = cq.Workplane('XY')
    
    temp_shape1 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webpostbl, 0, 0),
        tb.thumb_position(cb.webposttl, 0, 1),
        tb.thumb_position(cb.webpostbr, 1, 0),
        jb.joystick_position(jbh.joystickwebposttr),
    ))
    shape = shape.union(temp_shape1)
    
    temp_shape1 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webpostbl, 1, 0),
        tb.thumb_position(cb.webpostbr, 1, 0),
        jb.joystick_position(jbh.joystickwebposttr),
        jb.joystick_position(jbh.joystickwebpostbr),
    ))
    shape = shape.union(temp_shape1)

    temp_shape2 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webpostbl, 0, 1),
        tb.thumb_position(cb.webposttl, 0, 1),
        jb.joystick_position(jbh.joystickwebposttr),
        jb.joystick_position(jbh.joystickposttrtotl)
    ))
    shape = shape.union(temp_shape2)

    temp_shape3 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webpostbl, 0, 1),
        tb.thumb_position(cb.webposttl, 0, 2),
        jb.joystick_position(jbh.joystickposttrtotl),
        jb.joystick_position(jbh.joystickwebposttl)
    ))
    shape = shape.union(temp_shape3)
  
    temp_shape4 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webpostbl, 0, 2),
        tb.thumb_position(cb.webposttl, 0, 2),
        #jb.joystick_position(jbh.joystickposttrtotl),
        jb.joystick_position(jbh.joystickwebposttl)
    ))
    shape = shape.union(temp_shape4)

    temp_shape6 = cbh.hull_from_shapes((
        tb.thumb_position(cb.webpostbl, 0, 2),
        tb.thumb_position(cb.webpostbl, 0, 2),
        jb.joystick_position(jbh.joystickwebposttl),
        jb.joystick_position(jbh.joystickwebpostbl)
    ))
    shape = shape.union(temp_shape6)

    shape = shape.union(cjb.thumb_wall_brace_post_position_to_joystick_position(0, 2, 0, -1.5, cb.webpostbl, 0, -1.5, jbh.joystickwebpostbl))

    #for joystick walls when prototyping thumb
    # shape = shape.union(cjb.thumb_wall_brace_joystick_position_to_joystick_position(-4, -1.5, jbh.joystickwebpostbr,-2, -2, jbh.joystickwebpostbl))
    # shape = shape.union(cjb.thumb_wall_brace_joystick_position_to_joystick_position(-2, -2, jbh.joystickwebpostbl, 0, -1.5, jbh.joystickwebpostbl))

    return shape

def wall_brace_thin_back_to_display(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    #print("wall_brace()")
    hulls = []


        #     (lambda sh: kb.key_position(sh, 0, 0)),
        # 0,
        # 1,
        # cb.webposttl,

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_thin_back_display(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back_display(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back_display(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    #hulls.append(place1(cbh.post_translate(post1, cb.wall_locate1_left(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate2_thin_back(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, cb.wall_locate3_thin_back(dx1, dy1))))
    #hulls.append(place2(cbh.post_translate(post2, cb.wall_locate1_left(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate2(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, cb.wall_locate3(dx2, dy2))))
    shape2 = cjbh.bottom_hull_left_to_display(hulls)

    return shape1.union(shape2)