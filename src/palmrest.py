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
import clusterjoin as cj

def palm_right(final):
    shape = cq.Workplane('XY').union(palm_rest())
    s2 = cq.Workplane('XY').union(palm_walls())
    shape = shape.union(s2)
    
    block = cq.Workplane("XY").box(350, 350, 40)
    block = block.translate((0, 0, -20))
    shape = shape.cut(block)


    
    shape2 = final.translate((0.0, -0.5, -37.9))

    square = cq.Workplane('XY').rect(1000, 1000)
    for wire in square.wires().objects:
        plane = cq.Workplane('XY').add(cq.Face.makeFromWires(wire))
    shape2 = shape2.intersect(plane)
    
    for wire in shape2.wires().objects[1:2]:
        centerplate = (cq.Workplane("XY").add(cq.Face.makeFromWires(wire)).workplane())
        centerplate = centerplate.add(wire).toPending().extrude(100)

    outer = (cq.Workplane("XY").add(shape2.faces("<Z")).workplane())
    outer = outer.add(shape2.wires()).toPending().extrude(100)
    shape2 = outer.union(centerplate, tol=.01)

    shape = shape.cut(shape2)



    shape3 = final.translate((0.0, -0.5, -42.9))

    square = cq.Workplane('XY').rect(1000, 1000)
    for wire in square.wires().objects:
        plane = cq.Workplane('XY').add(cq.Face.makeFromWires(wire))
    shape3 = shape3.intersect(plane)
    
    for wire in shape3.wires().objects[1:2]:
        centerplate = (cq.Workplane("XY").add(cq.Face.makeFromWires(wire)).workplane())
        centerplate = centerplate.add(wire).toPending().extrude(100)

    outer = (cq.Workplane("XY").add(shape3.faces("<Z")).workplane())
    outer = outer.add(shape3.wires()).toPending().extrude(100)
    shape3 = outer.union(centerplate, tol=.01)

    shape = shape.cut(shape3)









    
    key = cq.Workplane("XY").box(30.5, 15, 90)
    key = cbh.rotate(key, [0, 0, 44.5])
    key = key.translate((20.82, -38.03, 20))
    shape = shape.cut(key)
    



    # key2 = cq.Workplane("XY").box(3, 5, 90)
    # key2 = cbh.rotate(key2, [0, 0, 36.5])
    # key2 = key2.translate((-5.7, -57.68, 20))
    # shape = shape.cut(key2)

    # key4 = cq.Workplane("XY").box(10, 5, 90)
    # key4 = cbh.rotate(key4, [0, 0, 52.5])
    # key4 = key4.translate((-1.89, -53.38, 20))
    # shape = shape.cut(key4)
    



    key3 = cq.Workplane("XY").box(7, 10, 90)
    key3 = cbh.rotate(key3, [0, 0, -4])
    key3 = key3.translate((13.8, -48.86, 20))
    #shape = shape.union(key3)

    key5 = cq.Workplane("XY").box(7, 14.5, 90)
    key5 = cbh.rotate(key5, [0, 0, 32])
    key5 = key5.translate((9.08, -45.6, 20))
    #shape = shape.union(key5)



    connector = cj.palm_rest_to_key_screwholes()
    shape = shape.cut(connector)
    
    print('end of palm right')
    return shape

lowest_palm_verts = []

def addPalmLocations(loc):
    lowest_palm_verts.append((loc.x, loc.y, loc.z))

def palm_rest():
    thickness = 8
    edge_points = cq.Workplane('XY').center(0,0).ellipse(25,40)
    #edge_points = cq.Workplane('XY').ellipseArc(25,40,180, 0).ellipseArc(25,20,0, 180).close()
    x_radius, y_radius = 25, 40
    angle1, angle2 = 0.0, 180.0
    
    #edge_points  = (Workplane("XY").ellipse(100,10).ellipse(50, 50))
    
    #edge_points = Edge.makeEllipse(x_radius=x_radius, y_radius=y_radius, pnt=(0, 0, 0), dir=(0, 0, 1), angle1=angle1, angle2=angle2)
    #edge_points = Wire.assembleEdges(edge_points.edges())
    #edge_points = cq.Workplane("XY").ellipsearc(25,40,180, 270).ellipsearc(25,40,270, 0)
            #.ellipsearc(25,20,0, 90)
            #.ellipsearc(25,20,90, 180)
    wp = cq.Workplane("XY")
    #edges = [(wp.ellipseArc(25,40,180, 270, 90)).val()]
    #edges.append((wp.ellipseArc(25,20,0, 90)).val())
    #edges.append((wp.ellipseArc(25,20,90, 180)).val())
    #edges.append((wp.ellipseArc(25,40,270, 0)).val())
    
    #edge_points = (cq.Workplane("XY").ellipseArc(25,40,180, 270).ellipseArc(25,40,270, 0).ellipseArc(25,20,0, 90).ellipseArc(25,20,90, 180).close()).extrude(1)
    #edges = Wire.assembleEdges(edge_points)
            
    #edge_points=Wire.assembleEdges(edges)
    #print(edge_points.edges(">Z").size())
    #print(edge_points.edges())
    #points = [edge_points]
    #w = cq.Workplane('XY').Wire.assembleEdges(edge_points)
    #edge_points = edge_points.combine(edge_points.edges())
    #print()
    #print(edge_points.wires().size())
    
    #dge_points = (
    #        cq.Workplane("XY")
    #        #.moveTo(10, 15)
    #        .ellipseArc(5, 4, -10, 190, sense=-1, startAtCurrent=False)
    #    )
    #edge_points = (
    #        edge_points.ellipseArc(5, 4, 180, 0, 0, sense=-1)
    #        .ellipseArc(5, 4, 0, 180, 0, sense=-1)
    #    )
    surface_points = [[8, 8, 8]]
    edge_points = edge_points.interpPlate(edge_points, surface_points, thickness,True, True, 3, 15, 2, False, 0.00001, 0.001, 0.01, 0.1, 8, 49).edges(">Z").fillet(6)
    
    
    excluded =(cq.Workplane('XY').center(28,0).ellipseArc(28,20,0, 180).lineTo(-56,60).lineTo(0,60).lineTo(0,0).close()).extrude(30).translate((0, 0, -15))
    #excluded = cq.Workplane("XY").box(50, 60, 40)
    #excluded = excluded.translate((30, 0, 0))
    edge_points= edge_points.cut(excluded).edges(">Z").fillet(7)
    
    hexcut = cq.Workplane('XY').pushPoints (pbh.getHexGrid() ).polygon(6, 6.0).extrude(20).translate((0, 0, -5))
    #edge_points = (edge_points.cut(hexcut)).edges("+Z").fillet(0.8).faces(">Z").fillet(0.5)
    
    edge_points = (edge_points.cut(hexcut))
    
    #edge_points.edges("<Z").vertices().eachpoint(addPalmLocations)
    
    #lowest_palm_verts = [addPalmLocations(v) for v in edge_points.edges("<Z").val().locations([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], frame="frenet")]
    #for v in edge_points.edges("<Z").val().locations([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], frame="frenet"):
    #    addPalmLocations(v) 
        

    
    #e = edge_points.edges("<Z").toPending().wire().val()
    #ga = e._geomAdaptor()
    
    #locs_corrected = e.locations(
    #    [ga.FirstParameter(), ga.LastParameter()],
    #    mode="parameter",
    #    frame="corrected",
    #)
    #print(str(locs_corrected))
    
    #w = e.wire().val()
    #p = e.positions([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])

    #print(str(p))
    
    
    #lowest_palm_verts = np.array((edge_points.edges("<Y").vertices())
    
    
    #restend = edge_points.wire().combine(edge_points.faces(">X").edges())
    #print(restend.edges().size())
    #backsurface_points = [[1.,1.,1.]]
    #rest= edge_points.interpPlate(restend, backsurface_points, thickness,True, True, 3, 25, 2, False, 0.00001, 0.0001, 0.01, 0.1, 8, 9)
    rest= edge_points
    
    bottompalmedge = rest.edges("<Z")
    
    resttrans = [24, -71, 35]
    restrotate = [-30, -4.5, 259]
    
    rest = cbh.rotate(rest, restrotate)
    rest = cbh.translate(rest, resttrans)
    
    bottompalmedge = cbh.rotate(bottompalmedge, restrotate)
    bottompalmedge = cbh.translate(bottompalmedge, resttrans)
    
    
    #for v in rest.edges("<Z").tag("bottompalmedge").toPending().wire().val().positions([0, 0.0769, 0.1538, 0.2307, 0.3076, 0.3845, 0.4614, 0.5383, 0.6152, 0.6921, 0.769, 0.8459, 0.9228 , 1]):
    #    addPalmLocations(v) 
        
    for v in bottompalmedge.toPending().wire().val().positions([0, 0.0769, 0.1538, 0.2307, 0.3076, 0.3845, 0.4614, 0.5383, 0.6152, 0.6921, 0.769, 0.8459, 0.9228 , 1]):
        addPalmLocations(v) 
    
    
    print(str(lowest_palm_verts))
    #rest = rotate(rest, [-44, -6, 244])
    #rest = translate(rest, [0, 0, 10])
    
    #rest = translate(rest, [30, -75, 0])
    return rest

def palm_walls():
    shape = cq.Workplane('XY')

    p1 = cbh.Transform((lowest_palm_verts[0][0]-0.6,lowest_palm_verts[0][1] +8,lowest_palm_verts[0][2]+3), (0,0,0))
    p2 = cbh.Transform((lowest_palm_verts[1][0],lowest_palm_verts[1][1] +2,lowest_palm_verts[1][2]+1), (0,0,0))
    p3 = cbh.Transform(lowest_palm_verts[2], (0,0,0))
    p4 = cbh.Transform(lowest_palm_verts[3], (0,0,0))
    p5 = cbh.Transform(lowest_palm_verts[4], (0,0,0))
    p6 = cbh.Transform((lowest_palm_verts[6][0]+2,lowest_palm_verts[6][1] +0,lowest_palm_verts[6][2]), (0,0,0))
    p7 = cbh.Transform((lowest_palm_verts[6][0]+3,lowest_palm_verts[6][1] +1.5,lowest_palm_verts[6][2]), (0,0,0))
    p8 = cbh.Transform((lowest_palm_verts[7][0]+5,lowest_palm_verts[7][1] +1.5,lowest_palm_verts[7][2]), (0,0,0))
    p9 = cbh.Transform((lowest_palm_verts[8][0]+6,lowest_palm_verts[8][1] -3,lowest_palm_verts[8][2]+4), (0,0,0))
    p10 = cbh.Transform((lowest_palm_verts[9][0]+3.5,lowest_palm_verts[9][1] -6,lowest_palm_verts[9][2]+3), (0,0,0))
    p11 = cbh.Transform((lowest_palm_verts[10][0]-1,lowest_palm_verts[10][1] -11,lowest_palm_verts[10][2]+9), (0,0,0))
    p12 = cbh.Transform((lowest_palm_verts[11][0],lowest_palm_verts[11][1] -14,lowest_palm_verts[11][2]+9.5), (0,0,0))
    p13 = cbh.Transform((lowest_palm_verts[12][0],lowest_palm_verts[12][1] -3,lowest_palm_verts[12][2]+9), (0,0,0))
    p14 = cbh.Transform((lowest_palm_verts[13][0],lowest_palm_verts[13][1] -3,lowest_palm_verts[13][2]+3), (0,0,0))

    shape = shape.union(pb.palm_wall_brace_left_position_to_default(p1, -0.1, -1.1, cb.wbpost, p2, 0, -0.5, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_left_position(p2, 0, -0.5, cb.wbpost, p3, -0.5, -0.6, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_left_position(p3, -0.5, -0.6, cb.wbpost, p4, -1.25, -0.6, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_left_position(p4, -1.25, -0.6, cb.wbpost, p5, -1.25, -0.4, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_left_position(p5, -1.25, -0.4, cb.wbpost, p6, -1.0, -0.27, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_left_position_to_default(p7, -1.2, 0.73, cb.wbpost, p6, -1.0, -0.27, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p7, -1.2, 0.73, cb.wbpost, p8, -0.5, 0.4, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p8, -0.5, 0.4, cb.wbpost, p9, -0.25, 0.7, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p9, -0.25, 0.7, cb.wbpost, p10, 0, 0.7, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p10, 0, 0.7, cb.wbpost, p11, 0, 0.7, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p11, 0, 0.7, cb.wbpost, p12, -0.25, 1.2, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p12, -0.25, 1.2, cb.wbpost, p13, -0.25, 1, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p13, -0.25, 1, cb.wbpost, p14, -0.25, 0.75, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p14, 1.3, -0.25, cb.wbpost, p1, 1.6, -0.5, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p14, 1.3, -0.25, cb.wbpost, p14, -0.25, 0.75, cb.wbpost))
    shape = shape.union(pb.palm_wall_brace_position(p1, -0.1, -1.1, cb.wbpost, p1, 1.6, -0.5 , cb.wbpost))

    return shape

