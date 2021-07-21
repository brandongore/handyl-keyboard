from cadquery import Wire, Edge
from cadquery import selectors
from cadquery import Shape
from cadquery import occ_impl
from cadquery import Workplane
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from jupyter_cadquery import set_sidecar, set_defaults, reset_defaults
from cqkit import *

import corebase as cb
import corebasehelpers as cbh
import coreparameters as cp
import thumbbase as tb
import thumbbasehelpers as tbh

def joystick_right():
    shape = cq.Workplane('XY').union(joystick_hole())

    print('end of joystick right')
    return shape

def joystick_hole():
    boxwidth = cp.joystick_width
    boxlength = cp.joystick_length
    boxheight = cp.joystick_height
    
    holewidth = 19.97
    holeheight = 26.46
    joystickholesize = 21.4
    
    leftjoystickoffset = 0.9
    rightjoystickoffset = 0.8
    topjoystickoffset = 14.30
    bottomjoystickoffset = 12.69
    
    centerheight = topjoystickoffset - holeheight/2  
    
    print(centerheight)
    offsetorigin = (0, rightjoystickoffset, centerheight)
    
    vcount = cbh.vertCounter()
    
    shape = cq.Workplane("YZ").box(boxwidth, boxlength, 21.5).faces(">X").circle(13.4).workplane(offset=0.4).circle(13.2).workplane(offset=0.3).circle(12.9).loft(combine=True)
    shape = shape.faces(">X").fillet(0.3)

    shape = shape.shell(1)

    shape = shape.faces(">X").hole(joystickholesize)

    shape = shape.faces("<X").workplane().rect(34, 38).cutBlind(-2)

    shape = shape.faces("<X[-2]").workplane(offset=-0.4).rect(19.0,24, forConstruction=True).vertices().triangle(12.3, 7, vcount).extrude(16.4)#.circle(3.25).extrude(15.9)
    shape = shape.faces("<X[-3]").workplane(offset=-0.4).rect(28.2,24.5, forConstruction=True).vertices().rect(4.4,11.8).extrude(16.4)
    shape = shape.faces("<X[-3]").workplane(offset=-0.4).rect(12.12,30.6, forConstruction=True).vertices().rect(12.11,5.69).extrude(16.4)
    shape = shape.faces("<X[-3]").workplane(offset=-0.4).circle(13.4).cutBlind(16, False)

    rs = RadiusSelector(joystickholesize/2)
    shape= shape.edges(rs).chamfer(0.4)
   
    shape = shape.faces(">X[-2]").workplane(origin=offsetorigin).rect(holewidth,holeheight, forConstruction=True).vertices().cboreHole(4.08, 4.08, 2.0, depth=25)
    boltentry = cq.Workplane("YZ").workplane(offset=11.5, origin=offsetorigin).rect(holewidth,holeheight, forConstruction=True).vertices().cone(3.72,4.0,2.0)#.cutBlind(2.0, True)
    shape = shape.cut(boltentry)
    cone = shape.faces(">X[-2]").workplane(offset=-2.72).rect(holewidth,holeheight, forConstruction=True).vertices().cone(2.025,3.71,2.75)
    shape = (shape).cut(cone)
    shape = shape.faces("<Z").workplane().center(-18.0,0).rect(12.5,13.9).cutBlind(-12.5, False)

    joyball = cq.Workplane("YZ").workplane(offset=2.55).sphere(14.14)
    joyball = joyball.workplane(offset=-15).circle(15.0).cutBlind(12, False)
    joyball = joyball.workplane(offset=-0.5).circle(15.0).cutBlind(13, False)
    centerball = cq.Workplane("YZ").workplane(offset=3.85).sphere(14.30)
    centerball = centerball.workplane(offset=-15).circle(15.0).cutBlind(12, False)
    centerball = centerball.workplane(offset=-0.5).circle(15.0).cutBlind(13, False)
    extraball = cq.Workplane("YZ").workplane(offset=5.0).sphere(14.33)
    extraball = extraball.workplane(offset=-15).circle(15.0).cutBlind(12, False)
    extraball = extraball.workplane(offset=1).circle(15.0).cutBlind(13, False)
    bottomentry = cq.Workplane("YZ").workplane(offset=-6.0).circle(13.75).extrude(7)
    joyball = joyball.union(extraball)
    joyball = joyball.union(centerball)
    joyball = joyball.union(bottomentry)
    shape = (shape).cut(joyball)
    shape = shape.faces("<X").workplane().center(0,19).rect(38, 38).cutBlind(-4.4, False)

    xrad = cbh.deg2rad(cp.joystick_rotation[0])  
    yrad = cbh.deg2rad(cp.joystick_rotation[1]) 
    zrad = cbh.deg2rad(cp.joystick_rotation[2]) 
    
    shape = cbh.y_rot(shape, yrad)
    shape = cbh.z_rot(shape, zrad)
    shape = cbh.x_rot(shape, xrad)
    
    #shape = shape.translate((40, 11, 0))
    #shape = rotate(shape, (0, 0, -24))
    #shape = shape.translate((-70.2,-54.8,19.0))
    shape = shape.translate((cp.joystick_offset[0],cp.joystick_offset[1],cp.joystick_offset[2]))
    
    # +4.6 -0.2 -5.5
    
    #shape = shape.translate((-79.8,-57.6,24.5))

    return shape
