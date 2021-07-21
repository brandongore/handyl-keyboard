from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from jupyter_cadquery import set_sidecar, set_defaults, reset_defaults
from cqkit import *
import numpy as np
from numpy import pi, math
import os.path as path
from scipy.spatial import ConvexHull as sphull

import coreparameters as cp
import corebasehelpers as cbh

def single_plate(cylinder_segments=100, padding=False, padding_amount= 0.0, rotateHole=False):
    width = cp.keyswitch_width
    height = cp.keyswitch_height
    if(padding == True):
        width = width + padding_amount
        height = height + padding_amount
    top_wall = cq.Workplane("XY").box(width + 3, 1.5, cp.plate_thickness)
    top_wall = top_wall.translate((0, (1.5 / 2) + (height / 2), cp.plate_thickness / 2))

    left_wall = cq.Workplane("XY").box(1.5, height + 3, cp.plate_thickness)
    left_wall = left_wall.translate(((1.5 / 2) + (width / 2), 0, cp.plate_thickness / 2))

    side_nub = cq.Workplane("XY").union(cq.Solid.makeCylinder(radius=0.4755, height=4.5))
    side_nub = side_nub.translate((-0.01, 0, -2.25))
    side_nub = cbh.rotate(side_nub, (90, 0, 0))
    side_nub = side_nub.translate((width / 2, 0, 3.05))
    nub_cube = cq.Workplane("XY").box(0.1, 12, cp.plate_thickness/2.6)
    nub_cube = nub_cube.translate(((0.25) + (width / 2), 0, (cp.plate_thickness / 2)+1.17))
    
    nub_cyl_cutout = cq.Workplane("XY").union(cq.Solid.makeCylinder(radius=0.5, height=(width / 2)-2.7))
    nub_cyl_cutout = nub_cyl_cutout.translate((0, 0, -2.2))
    nub_cyl_cutout = cbh.rotate(nub_cyl_cutout, (90, 0, 0))
    nub_cyl_cutout = nub_cyl_cutout.translate(((-0.07) + (width / 2), 0, (cp.plate_thickness / 2)+0.12))
    
    nub_cube_cutout = cq.Workplane("XY").box(0.1, 14, cp.plate_thickness/5)
    nub_cube_cutout = nub_cube_cutout.translate(((-0.38) + (width / 2), 0, (cp.plate_thickness / 2)+0.335))
    
    side_nub2_cutout = cbh.tess_hull(shapes=(nub_cyl_cutout, nub_cube_cutout))
    side_nub2_cutout = side_nub2_cutout.union(nub_cyl_cutout).union(nub_cube_cutout)

    side_nub2 = cbh.tess_hull(shapes=(side_nub, nub_cube))
    side_nub2 = side_nub2.union(side_nub).union(nub_cube)
    
    side_nub3 = cq.Workplane("XY").union(cq.Solid.makeCylinder(radius=1, height=2.3))
    side_nub3 = side_nub3.translate((-0.01, 0, -1.15))
    side_nub3 = cbh.rotate(side_nub3, (90, 0, 0))
    side_nub3 = side_nub3.translate((width / 2, 0, 1.8))
    nub_cube3 = cq.Workplane("XY").box(0.1, 3.2, cp.plate_thickness/1)
    nub_cube3 = nub_cube3.translate(((0.25) + (width / 2), 0, (cp.plate_thickness / 2)+0.0))
    
    
    side_nub4 = cbh.tess_hull(shapes=(side_nub3, nub_cube3))
    side_nub4 = side_nub4.union(side_nub3).union(nub_cube3)
    side_nub4 = cbh.rotate(side_nub4, (0, 0, 90))
    #side_nub2 = rotate(side_nub2, (180, 0, 0))

    plate_half1 = top_wall.union(left_wall).union(side_nub2).cut(side_nub2_cutout)#.union(side_nub4)
    plate_half2 = plate_half1
    plate_half2 = cbh.mirror(plate_half2, 'XZ')
    plate_half2 = cbh.mirror(plate_half2, 'YZ')

    plate = plate_half1.union(plate_half2)
    
    if rotateHole:
        plate = cbh.rotate(plate, (0, 0, 90))

    return plate

def double_plate():
    print('double_plate()')
    plate_height = (cp.sa_double_length - cp.mount_height) / 3
    top_plate = cq.Workplane("XY").box(cp.mount_width, plate_height, cp.web_thickness)
    top_plate = cbh.translate(top_plate,
                          [0, (plate_height + cp.mount_height) / 2, cp.plate_thickness - (cp.web_thickness / 2)]
                          )
    return cbh.union((top_plate, cbh.mirror(top_plate, 'XZ')))

def sa_cap(Usize=1):
    # MODIFIED TO NOT HAVE THE ROTATION.  NEEDS ROTATION DURING ASSEMBLY
    sa_length = 18.25

    bw2 = Usize * sa_length / 2
    bl2 = sa_length / 2
    m = 0
    pw2 = 6 * Usize + 1
    pl2 = 6

    if Usize == 1:
        m = 17 / 2

    k1 = cq.Workplane('XY').polyline([(bw2, bl2), (bw2, -bl2), (-bw2, -bl2), (-bw2, bl2), (bw2, bl2)])
    k1 = cq.Wire.assembleEdges(k1.edges().objects)
    k1 = cq.Workplane('XY').add(cq.Solid.extrudeLinear(outerWire=k1, innerWires=[], vecNormal=cq.Vector(0, 0, 0.1)))
    k1 = k1.translate((0, 0, 0.05))
    k2 = cq.Workplane('XY').polyline([(pw2, pl2), (pw2, -pl2), (-pw2, -pl2), (-pw2, pl2), (pw2, pl2)])
    k2 = cq.Wire.assembleEdges(k2.edges().objects)
    k2 = cq.Workplane('XY').add(cq.Solid.extrudeLinear(outerWire=k2, innerWires=[], vecNormal=cq.Vector(0, 0, 0.1)))
    k2 = k2.translate((0, 0, 12.0))
    if m > 0:
        m1 = cq.Workplane('XY').polyline([(m, m), (m, -m), (-m, -m), (-m, m), (m, m)])
        m1 = cq.Wire.assembleEdges(m1.edges().objects)
        m1 = cq.Workplane('XY').add(cq.Solid.extrudeLinear(outerWire=m1, innerWires=[], vecNormal=cq.Vector(0, 0, 0.1)))
        m1 = m1.translate((0, 0, 6.0))
        key_cap = cbh.hull_from_shapes((k1, k2, m1))
    else:
        key_cap = cbh.hull_from_shapes((k1, k2))

    key_cap = key_cap.translate((0, 0, 5 + cp.plate_thickness))

    return key_cap

####################
## Web Connectors ##
####################

def web_post():
    #print('web_post()')
    p1 = [0,0,cp.web_thickness/2]
    p2 = [0,0,-cp.web_thickness/2]
    
    toppoint = cbh.add_translate(p1, (0, 0, cp.plate_thickness - (cp.web_thickness / 2)))
    bottompoint = cbh.add_translate(p2, (0, 0, cp.plate_thickness - (cp.web_thickness / 2)))
    post = [toppoint,bottompoint]

    return post

def web_post_tr():
    post = wbpost
    return cbh.post_translate(post, ((cp.mount_width / 2) - cp.post_adj, (cp.mount_height / 2) - cp.post_adj, 0))

def web_post_tl():
    post = wbpost
    return cbh.post_translate(post, (-(cp.mount_width / 2) + cp.post_adj, (cp.mount_height / 2) - cp.post_adj, 0))
        
def web_post_bl():
    post = wbpost
    return cbh.post_translate(post, (-(cp.mount_width / 2) + cp.post_adj, -(cp.mount_height / 2) + cp.post_adj, 0))

def web_post_br():
    post = wbpost
    return cbh.post_translate(post, ((cp.mount_width / 2) - cp.post_adj, -(cp.mount_height / 2) + cp.post_adj, 0))

wbpost = web_post()

webpostbr = web_post_br()
webposttr = web_post_tr()
webpostbl = web_post_bl()
webposttl = web_post_tl()

##########
## Case ##
##########

def wall_locate1(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, dy * cp.wall_thickness, -1]

def wall_locate2(dx, dy):
    #print("wall_locate2()")
    return [dx * cp.wall_xy_offset, dy * cp.wall_xy_offset, -4]

def wall_locate3(dx, dy):
    #print("wall_locate3()")
    return [
        dx * (cp.wall_xy_offset + cp.wall_thickness),
        dy * (cp.wall_xy_offset + cp.wall_thickness),
        -8,
    ]

def wall_locate1_low(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, dy * cp.wall_thickness, -1]

def wall_locate2_low(dx, dy):
    #print("wall_locate2()")
    return [dx/1.4 * cp.wall_xy_offset, dy * cp.wall_xy_offset, -4]

def wall_locate3_low(dx, dy):
    #print("wall_locate3()")
    return [
        dx/1.4 * (cp.wall_xy_offset + cp.wall_thickness),
        dy * (cp.wall_xy_offset + cp.wall_thickness),
        -5,
    ]


def wall_locate1_thin(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, (dy)  * cp.wall_thickness -1, -6]

def wall_locate2_thin(dx, dy):
    #print("wall_locate2()")
    return [dx * cp.wall_xy_offset, (dy)  * cp.wall_xy_offset +2, -12]

def wall_locate3_thin(dx, dy):
    #print("wall_locate3()")
    return [
        dx * (cp.wall_xy_offset + cp.wall_thickness),
        dy  * (cp.wall_xy_offset + cp.wall_thickness) +2,
        -13,
    ]

def wall_locate1_thin_extended(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, (dy)  * cp.wall_thickness *1.1, -1]

def wall_locate2_thin_extended(dx, dy):
    #print("wall_locate2()")
    return [dx * cp.wall_xy_offset, (dy)  * cp.wall_xy_offset *1.4, -4]

def wall_locate3_thin_extended(dx, dy):
    #print("wall_locate3()")
    return [
        dx * (cp.wall_xy_offset + cp.wall_thickness),
        dy  * (cp.wall_xy_offset + cp.wall_thickness) *1.1,
        -8,
    ]

def wall_locate1_thin_low(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, (dy)  * cp.wall_thickness -1, -8]

def wall_locate2_thin_low(dx, dy):
    #print("wall_locate2()")
    return [dx * cp.wall_xy_offset, (dy)  * cp.wall_xy_offset +2, -16]

def wall_locate3_thin_low(dx, dy):
    #print("wall_locate3()")
    return [
        dx * (cp.wall_xy_offset + cp.wall_thickness),
        dy  * (cp.wall_xy_offset + cp.wall_thickness) +2,
        -17,
    ]

def wall_locate1_thin_back_display(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, (dy)  * cp.wall_thickness, -1]

def wall_locate2_thin_back_display(dx, dy):
    #print("wall_locate2()")
    return [dx * cp.wall_xy_offset, (dy)  * cp.wall_xy_offset, -9]

def wall_locate3_thin_back_display(dx, dy):
    #print("wall_locate3()")
    return [
        dx * (cp.wall_xy_offset + cp.wall_thickness),
        dy  * (cp.wall_xy_offset + cp.wall_thickness) ,
        -10,
    ]


def wall_locate1_thin_back(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, (dy)  * cp.wall_thickness, -1]

def wall_locate2_thin_back(dx, dy):
    #print("wall_locate2()")
    return [dx * cp.wall_xy_offset, (dy)  * cp.wall_xy_offset, -9]

def wall_locate3_thin_back(dx, dy):
    #print("wall_locate3()")
    return [
        dx * (cp.wall_xy_offset + cp.wall_thickness),
        dy  * (cp.wall_xy_offset + cp.wall_thickness) ,
        -10,
    ]

def wall_locate1_thin_back_extended(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, (dy)  * cp.wall_thickness*1.1, -1]

def wall_locate2_thin_back_extended(dx, dy):
    #print("wall_locate2()")
    return [dx  * cp.wall_xy_offset, (dy)  * cp.wall_xy_offset *1.4, -15]

def wall_locate3_thin_back_extended(dx, dy):
    #print("wall_locate3()")
    return [
        dx * (cp.wall_xy_offset + cp.wall_thickness),
        dy  * (cp.wall_xy_offset + cp.wall_thickness) *1.1,
        -12,
    ]


def wall_locate1_short(dx, dy):
    #print("wall_locate1()")
    return [dx/1.4 * cp.wall_thickness, dy/1.4 * cp.wall_thickness, -0.9]

def wall_locate2_short(dx, dy):
    #print("wall_locate2()")
    return [dx/2.4 * cp.wall_xy_offset, dy/2.2 * cp.wall_xy_offset, -1.1]

def wall_locate3_short(dx, dy):
    #print("wall_locate3()")
    return [
        (dx/2)  * (cp.wall_xy_offset + cp.wall_thickness),
        (dy/1.5)  * (cp.wall_xy_offset + cp.wall_thickness),
        -2.95,
    ]


def wall_locate1_left2(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, dy * cp.wall_thickness, -1]

def wall_locate2_left2(dx, dy):
    #print("wall_locate2()")
    return [dx * cp.wall_xy_offset, dy * cp.wall_xy_offset-1, -5]

def wall_locate3_left2(dx, dy):
    #print("wall_locate3()")
    return [
        dx * (cp.wall_xy_offset + cp.wall_thickness),
        dy * (cp.wall_xy_offset + cp.wall_thickness),
        -5,
    ]


def wall_locate1_left(dx, dy):
    #print("wall_locate1()")
    return [dx * cp.wall_thickness, dy * cp.wall_thickness, -1]

def wall_locate2_left(dx, dy):
    #print("wall_locate2()")
    return [dx * cp.wall_xy_offset, dy * cp.wall_xy_offset, -5]

def wall_locate3_left(dx, dy):
    #print("wall_locate3()")
    return [
        dx * (cp.wall_xy_offset + cp.wall_thickness),
        dy * (cp.wall_xy_offset + cp.wall_thickness),
        -5,
    ]

def wall_brace(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(cbh.post_translate(post1, wall_locate1(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, wall_locate3(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(cbh.post_translate(post2, wall_locate1(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, wall_locate2(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, wall_locate3(dx2, dy2))))
    shape1 = cbh.hull_from_shapes(hulls)
    
    hulls = []
    hulls.append(place1(cbh.post_translate(post1, wall_locate2(dx1, dy1))))
    hulls.append(place1(cbh.post_translate(post1, wall_locate3(dx1, dy1))))
    hulls.append(place2(cbh.post_translate(post2, wall_locate2(dx2, dy2))))
    hulls.append(place2(cbh.post_translate(post2, wall_locate3(dx2, dy2))))
    shape2 = cbh.bottom_hull(hulls)

    return shape1.union(shape2)