from cadquery import Wire, Edge
from cadquery import selectors
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from jupyter_cadquery import set_sidecar, set_defaults, reset_defaults
from cqkit import *
import numpy as np
from numpy import pi, math
import os.path as path
from scipy.spatial import ConvexHull as sphull

def deg2rad(degrees: float) -> float:
    return degrees * pi / 180

def rad2deg(rad: float) -> float:
    return rad * 180 / pi

def rotate(shape, angle):
    # print('rotate()')
    origin = (0, 0, 0)
    #print("angle 0 : "+str(angle[0]))
    #print("angle 1 : "+str(angle[1]))
    #print("angle 2 : "+str(angle[2]))
    shape = shape.rotate(axisStartPoint=origin, axisEndPoint=cq.Vector(1, 0, 0), angleDegrees=angle[0])
    shape = shape.rotate(axisStartPoint=origin, axisEndPoint=cq.Vector(0, 1, 0), angleDegrees=angle[1])
    shape = shape.rotate(axisStartPoint=origin, axisEndPoint=cq.Vector(0, 0, 1), angleDegrees=angle[2])
    return shape

def translate(shape, vector):
    # print('translate()')
    return shape.translate(tuple(vector))

def mirror(shape, plane=None):
    #print('mirror()')
    return shape.mirror(mirrorPlane=plane)

def union(shapes):
    #print('union()')
    shape = None
    for item in shapes:
        if shape is None:
            shape = item
        else:
            shape = shape.union(item, tol=.01)
    return shape

def face_from_points(points):
    # print('face_from_points()')
    edges = []
    num_pnts = len(points)
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % num_pnts]
        edges.append(
            cq.Edge.makeLine(
                cq.Vector(p1[0], p1[1], p1[2]),
                cq.Vector(p2[0], p2[1], p2[2]),
            )
        )

    face = cq.Face.makeFromWires(cq.Wire.assembleEdges(edges))

    return face

def hull_from_points(points):
    #print('hull_from_points()')
    hull_calc = sphull(points)
    n_faces = len(hull_calc.simplices)

    faces = []
    for i in range(n_faces):
        face_items = hull_calc.simplices[i]
        fpnts = []
        for item in face_items:
            fpnts.append(points[item])
        faces.append(face_from_points(fpnts))

    shape = cq.Solid.makeSolid(cq.Shell.makeShell(faces))
    shape = cq.Workplane('XY').union(shape)
    return shape


def hull_from_shapes(shapes, points=None):
    #print('hull_from_shapes()')
    vertices = []
    for shape in shapes:
        #print('hullfromshapes: ' + str(shape)) 
        verts = shape 
        for vert in verts:
            #print('vertices: ' + str(vert.toTuple()))  
            vertices.append(np.array(vert))
    if points is not None:
        for point in points:
            vertices.append(np.array(point))
            
    #print('hull from shapes vertices: ' + str(len(vertices)) + ' - points: ' + str(points))        

    shape = hull_from_points(vertices)
    return shape


def tess_hull(shapes, sl_tol=.5, sl_angTol=1):
    # print('hull_from_shapes()')
    vertices = []
    solids = []
    for wp in shapes:
        for item in wp.solids().objects:
            solids.append(item)

    for shape in solids:
        verts = shape.tessellate(sl_tol)[0]
        for vert in verts:
            vertices.append(np.array(vert.toTuple()))

    shape = hull_from_points(vertices)
    return shape

def triangle_hulls(shapes):
    #print('triangle_hulls()')
    hulls = [cq.Workplane('XY')]
    for i in range(len(shapes) - 2):
        hulls.append(hull_from_shapes(shapes[i: (i + 3)]))

    return union(hulls)

#########################
## Placement Functions ##
#########################

def rotate_around_x_single(position, angle):
    # print('rotate_around_x()')
    t_matrix = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ]
    )
    return np.matmul(t_matrix, position)

def rotate_around_y_single(position, angle):
    # print('rotate_around_y()')
    t_matrix = np.array(
        [
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)],
        ]
    )
    return np.matmul(t_matrix, position)

def rotate_around_z_single(position, angle):
    # print('rotate_around_z()')
    t_matrix = np.array(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )
    return np.matmul(t_matrix, position)

def rotate_around_x(position, angle):
    # print('rotate_around_x()')
    t_matrix = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ]
    )
    
    newpost = []
    for i in range(len(position)):
        newposition = np.matmul(t_matrix, position[i])
        newpost.append(newposition) 
    return newpost

def rotate_around_y(position, angle):
    # print('rotate_around_y()')
    t_matrix = np.array(
        [
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)],
        ]
    )
    
    newpost = []
    for i in range(len(position)):
        newposition = np.matmul(t_matrix, position[i])
        newpost.append(newposition) 
    return newpost

def rotate_around_z(position, angle):
    # print('rotate_around_z()')
    t_matrix = np.array(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )
    
    newpost = []
    for i in range(len(position)):
        newposition = np.matmul(t_matrix, position[i])
        newpost.append(newposition) 
    return newpost

# def rotate_around_x_from_point(angle):
#     rotation_degrees = 90
#     rotation_radians = np.radians(rotation_degrees)
#     rotation_axis = np.array([1, 0, 0])

#     rotation_vector = rotation_radians * rotation_axis
#     rotation = R.from_rotvec(rotation_vector)
#     rotated_vec = rotation.apply(vec)
#     return rotated_vec

def x_rot(shape, angle):
    # print('x_rot()')
    rotshape = rotate(shape, [rad2deg(angle), 0, 0])
    return rotshape

def y_rot(shape, angle):
    # print('y_rot()')
    rotshape = rotate(shape, [0, rad2deg(angle), 0])
    return rotshape

def z_rot(shape, angle):
     # print('z_rot()')
    rotshape = rotate(shape, [0, 0, rad2deg(angle)])
    return rotshape

def add_translate(shape, xyz):
    #print('add_translate()')
    vals = []
    for i in range(len(shape)):
        vals.append(shape[i] + xyz[i])
    return vals

def post_translate(post, xyz):
    newpost = []
    for i in range(len(post)):
        newpost.append(add_translate(post[i], xyz)) 
    return newpost

def cone(self, radius1: float, radius2: float, height: object):
    def _singleCone(loc):

        return cq.Solid.makeCone(radius1, radius2, height).locate(loc)
    
    return self.eachpoint(_singleCone, True)

#link the plugin into CadQuery
    
cq.Workplane.cone = cone

def triangle(self, diameter: float, rotateAngle: float, counter: object):
    def _singleTriangle(loc):
        angle = 2.0 * math.pi / 3
        pnts = []
        triloc = loc.wrapped.Transformation().TranslationPart()
        totalX = 0
        totalY = 0

        iteration = counter.count()
        splitAngle = 30#(360 / 4)
        rang = rotateAngle
        if iteration == 1 or iteration == 3:
            rang = rang - 44#* iteration

        finalRotation = rang + (splitAngle * iteration)# + (((iteration-1)/iteration)*15)
        finalRotation = deg2rad(finalRotation)

        for i in range(4):
            ang = angle * i
            pt = [(diameter / 2.0 * math.cos(ang)),(diameter / 2.0 * math.sin(ang)),0]

            pt = rotate_around_z_single(pt,finalRotation)
            vec = cq.Vector(pt[0], pt[1], pt[2])
            pnts.append(vec)

        return cq.Wire.makePolygon(pnts, False).locate(loc)
    

    return self.eachpoint(_singleTriangle, True)

#link the plugin into CadQuery
    
cq.Workplane.triangle = triangle

class vertCounter():
    count_n = 0

    @staticmethod
    def count():
        vertCounter.count_n += 1
        return vertCounter.count_n

class Transform:
    def __init__(self, translation, rotation):
        self.translation = translation
        self.rotation = rotation
           
#########################
## Placement Functions ##
#########################

def web_post_position(position, xyz, xryrzr):
    xrad = deg2rad(xryrzr[0])  
    yrad = deg2rad(xryrzr[1]) 
    zrad = deg2rad(xryrzr[2]) 
    
    post = rotate_around_y(position, yrad)
    post = rotate_around_z(post, zrad)
    post = rotate_around_x(post, xrad)
    post = post_translate(post, xyz)

    return post

def web_post_position_transform(position, transform):
    xrad = deg2rad(transform.rotation[0])  
    yrad = deg2rad(transform.rotation[1]) 
    zrad = deg2rad(transform.rotation[2]) 
    
    post = rotate_around_y(position, yrad)
    post = rotate_around_z(post, zrad)
    post = rotate_around_x(post, xrad)
    post = post_translate(post, transform.translation)

    return post

def bottom_hull(p, height=0.001):
    shape = None
    vertices = []
    for item in p:
        v0 = item[0]
        v1 = item[1]
        v2 = [v0[0], v0[1], -10]
        vertices.append(np.array(v0))
        vertices.append(np.array(v1))
        vertices.append(np.array(v2))

    t_shape = hull_from_points(vertices)
    shape = t_shape 
    return shape
