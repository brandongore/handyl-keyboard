import cadquery as cq
from jupyter_cadquery.cadquery import (PartGroup, Part, Edges, Faces, Vertices, show)
from jupyter_cadquery import set_sidecar, set_defaults, reset_defaults

import numpy as np
from numpy import pi
import os.path as path

from scipy.spatial import ConvexHull as sphull
#from pyhull.convex_hull import ConvexHull as sphull


def deg2rad(degrees: float) -> float:
    return degrees * pi / 180


def rad2deg(rad: float) -> float:
    return rad * 180 / pi

# ######################
# ## Shape parameters ##
# ######################

show_caps = True

nrows = 5  # key rows
ncols = 4  # key columns

alpha = pi / 6.0  # curvature of the columns
beta = pi / 24.0  # curvature of the rows
centerrow = nrows - 3  # controls front_back tilt
centercol = 3  # controls left_right tilt / tenting (higher number is more tenting)
tenting_angle = 45.2  # or, change this for more precise tenting control

if nrows > 5:
    column_style = "orthographic"
else:
    column_style = "standard"  # options include :standard, :orthographic, and :fixed


# column_style='fixed'

def rotate(shape, angle):
    # print('rotate()')
    origin = (0, 0, 0)
    shape = shape.rotate(axisStartPoint=origin, axisEndPoint=(1, 0, 0), angleDegrees=angle[0])
    shape = shape.rotate(axisStartPoint=origin, axisEndPoint=(0, 1, 0), angleDegrees=angle[1])
    shape = shape.rotate(axisStartPoint=origin, axisEndPoint=(0, 0, 1), angleDegrees=angle[2])
    return shape


def translate(shape, vector):
    # print('translate()')
    return shape.translate(tuple(vector))

def mirror(shape, plane=None):
    print('mirror()')
    return shape.mirror(mirrorPlane=plane)

def union(shapes):
    print('union()')
    shape = None
    for item in shapes:
        if shape is None:
            shape = item
        else:
            shape = shape.union(item)
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
    print('hull_from_points()')
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
    print('hull_from_shapes()')
    vertices = []
    for shape in shapes:
        verts = shape.vertices()
        for vert in verts.objects:
            vertices.append(np.array(vert.toTuple()))
    if points is not None:
        for point in points:
            vertices.append(np.array(point))

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


def column_offset(column: int) -> list:
    # print('column_offset()')
    if column == 0:
        return [-0.3, 2.9, -2]
    elif column == 1:
        return [-0.5, 2.9, -4]
    elif column == 2:
        return [0.5, -1, 0]
    elif column == 3:
        return [1.2, -4.7, 3]  # original [0 -5.8 5.64]
    else:
        return [0, 0, 0]


thumb_offsets = [6, -3, 7]
keyboard_z_offset = (
    27  # controls overall height# original=9 with centercol=3# use 16 for centercol=2
)

extra_width = 3.5  # extra space between the base of keys# original= 2
extra_height = -0.5  # original= 0.5

wall_z_offset = -15  # length of the first downward_sloping part of the wall (negative)
wall_xy_offset = 5  # offset in the x and/or y direction for the first downward_sloping part of the wall (negative)
wall_thickness = 2  # wall thickness parameter# originally 5

## Settings for column_style == :fixed
## The defaults roughly match Maltron settings
##   http://patentimages.storage.googleapis.com/EP0219944A2/imgf0002.png
## fixed_z overrides the z portion of the column ofsets above.
## NOTE: THIS DOESN'T WORK QUITE LIKE I'D HOPED.
fixed_angles = [deg2rad(10), deg2rad(10), 0, 0, 0, deg2rad(-15), deg2rad(-15)]
fixed_x = [-41.5, -22.5, 0, 20.3, 41.4, 65.5, 89.6]  # relative to the middle finger
fixed_z = [12.1, 8.3, 0, 5, 10.7, 14.5, 17.5]
fixed_tenting = deg2rad(0)

#######################
## General variables ##
#######################

lastrow = nrows - 1
cornerrow = lastrow - 1
lastcol = ncols - 1

#################
## Switch Hole ##
#################

keyswitch_height = 14.195  ## Was 14.1, then 14.25
keyswitch_width = 14.195

sa_profile_key_height = 12.7

plate_thickness = 4
mount_width = keyswitch_width + 3
mount_height = keyswitch_height + 3
mount_thickness = plate_thickness

SWITCH_WIDTH = 14
SWITCH_HEIGHT = 14
CLIP_THICKNESS = 1.4
CLIP_UNDERCUT = 1.0
UNDERCUT_TRANSITION = .2


def single_plate(cylinder_segments=100):
    top_wall = cq.Workplane("XY").box(keyswitch_width + 3, 1.5, plate_thickness)
    top_wall = top_wall.translate((0, (1.5 / 2) + (keyswitch_height / 2), plate_thickness / 2))

    left_wall = cq.Workplane("XY").box(1.5, keyswitch_height + 3, plate_thickness)
    left_wall = left_wall.translate(((1.5 / 2) + (keyswitch_width / 2), 0, plate_thickness / 2))

    side_nub = cq.Workplane("XY").union(cq.Solid.makeCylinder(radius=0.4, height=4.5))
    side_nub = side_nub.translate((0, 0, -4.5 / 2.0))
    side_nub = rotate(side_nub, (90, 0, 0))
    side_nub = side_nub.translate((keyswitch_width / 2, 0, 3))
    nub_cube = cq.Workplane("XY").box(0.1, 12, plate_thickness)
    nub_cube = nub_cube.translate(((2.5 / 2) + (keyswitch_width / 2), 0, plate_thickness / 2))

    side_nub2 = tess_hull(shapes=(side_nub, nub_cube))
    side_nub2 = side_nub2.union(side_nub).union(nub_cube)
    #side_nub2 = rotate(side_nub2, (180, 0, 0))

    plate_half1 = top_wall.union(left_wall).union(side_nub2)
    plate_half2 = plate_half1
    plate_half2 = mirror(plate_half2, 'XZ')
    plate_half2 = mirror(plate_half2, 'YZ')

    plate = plate_half1.union(plate_half2)

    return plate


################
## SA Keycaps ##
################

sa_length = 18.25
sa_double_length = 37.5


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
        key_cap = hull_from_shapes((k1, k2, m1))
    else:
        key_cap = hull_from_shapes((k1, k2))

    key_cap = key_cap.translate((0, 0, 5 + plate_thickness))
    # key_cap = key_cap.color((220 / 255, 163 / 255, 163 / 255, 1))

    return key_cap


#########################
## Placement Functions ##
#########################


def rotate_around_x(position, angle):
    # print('rotate_around_x()')
    t_matrix = np.array(
        [
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)],
        ]
    )
    return np.matmul(t_matrix, position)


def rotate_around_y(position, angle):
    # print('rotate_around_y()')
    t_matrix = np.array(
        [
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)],
        ]
    )
    return np.matmul(t_matrix, position)

def rotate_around_z(position, angle):
    # print('rotate_around_z()')
    t_matrix = np.array(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )
    return np.matmul(t_matrix, position)


cap_top_height = plate_thickness + sa_profile_key_height
row_radius = ((mount_height + extra_height) / 2) / (np.sin(alpha / 2)) + cap_top_height
column_radius = (
                        ((mount_width + extra_width) / 2) / (np.sin(beta / 2))
                ) + cap_top_height
column_x_delta = -1 - column_radius * np.sin(beta)
column_base_angle = beta * (centercol - 2)


def apply_key_geometry(
        shape,
        translate_fn,
        rotate_x_fn,
        rotate_y_fn,
        rotate_z_fn,
        column,
        row,
        column_style=column_style,
):
    print('apply_key_geometry()')

    column_angle = beta * (centercol - column)

    if column_style == "orthographic":
        column_z_delta = column_radius * (1 - np.cos(column_angle))
        shape = translate_fn(shape, [0, 0, -row_radius])
        shape = rotate_x_fn(shape, alpha * (centerrow - row))
        shape = translate_fn(shape, [0, 0, row_radius])
        shape = rotate_y_fn(shape, column_angle)
        shape = translate_fn(
            shape, [-(column - centercol) * column_x_delta, 0, column_z_delta]
        )
        shape = translate_fn(shape, column_offset(column))

    elif column_style == "fixed":
        shape = rotate_y_fn(shape, fixed_angles[column])
        shape = translate_fn(shape, [fixed_x[column], 0, fixed_z[column]])
        shape = translate_fn(shape, [0, 0, -(row_radius + fixed_z[column])])
        shape = rotate_x_fn(shape, alpha * (centerrow - row))
        shape = translate_fn(shape, [0, 0, row_radius + fixed_z[column]])
        shape = rotate_y_fn(shape, fixed_tenting)
        shape = translate_fn(shape, [0, column_offset(column)[1], 0])

    else:
        shape = translate_fn(shape, [0, 0, -row_radius])
        shape = rotate_x_fn(shape, alpha * (centerrow - row))
        shape = translate_fn(shape, [0, 0, row_radius])
        shape = translate_fn(shape, [0, 0, -column_radius])
        shape = rotate_y_fn(shape, column_angle)
        shape = translate_fn(shape, [0, 0, column_radius])
        shape = translate_fn(shape, column_offset(column))
        
        if column == 0:
        # if row == 0:
        #     shape = translate_fn(shape, [0.5, 0, 0])
        # shape = translate_fn(shape, [0, 0, 1.7* (nrows-row-2)])
        # shape = translate_fn(shape, [1.2* (nrows-row-1), 0, 0])
            shape = rotate_x_fn(shape, 0.01* (nrows-row-1))
        # shape = rotate_y_fn(shape, -0.05* (nrows-row-1))
            shape = rotate_z_fn(shape, 0.01)
        if column == 1:
        # if row == 0:
        #     shape = translate_fn(shape, [0.5, 0, 0])
        # shape = translate_fn(shape, [0, 0, 1.7* (nrows-row-2)])
        # shape = translate_fn(shape, [1.2* (nrows-row-1), 0, 0])
            shape = rotate_x_fn(shape, 0.01* (nrows-row-1))
        # shape = rotate_y_fn(shape, -0.05* (nrows-row-1))
            shape = rotate_z_fn(shape, -0.05)
        if column == 2:
        #if row == 0:
            #shape = translate_fn(shape, [0.5, 0, 0])
        # shape = translate_fn(shape, [0, 0, 1.7* (nrows-row-2)])
        # shape = translate_fn(shape, [1.2* (nrows-row-1), 0, 0])
            shape = rotate_x_fn(shape, -0.01* (nrows-row-1))
        # shape = rotate_y_fn(shape, -0.05* (nrows-row-1))
            shape = rotate_z_fn(shape, -0.12)
        if column == 3:
        # shape = translate_fn(shape, [0, 0, 1.7* (nrows-row-2)])
        # shape = translate_fn(shape, [1.5* (nrows-row-2), 0, 0])
        #shape = rotate_x_fn(shape, 0.01* (nrows-row-1))
            shape = rotate_y_fn(shape, -0.1)
            shape = rotate_z_fn(shape, -0.2)

    shape = rotate_y_fn(shape, tenting_angle)
    shape = translate_fn(shape, [0, 0, keyboard_z_offset])

    return shape


def x_rot(shape, angle):
    # print('x_rot()')
    return rotate(shape, [rad2deg(angle), 0, 0])


def y_rot(shape, angle):
    # print('y_rot()')
    return rotate(shape, [0, rad2deg(angle), 0])

def z_rot(shape, angle):
     # print('z_rot()')
    return rotate(shape, [0, 0, rad2deg(angle)])


def key_place(shape, column, row):
    print('key_place()')
    return apply_key_geometry(shape, translate, x_rot, y_rot, z_rot, column, row)


def add_translate(shape, xyz):
    print('add_translate()')
    vals = []
    for i in range(len(shape)):
        vals.append(shape[i] + xyz[i])
    return vals


def key_position(position, column, row):
    print('key_position()')
    return apply_key_geometry(
        position, add_translate, rotate_around_x, rotate_around_y, rotate_around_z, column, row
    )


def key_holes():
    print('key_holes()')
    hole = single_plate()
    holes = []
    for column in range(ncols):
        for row in range(nrows):
            # if (not row == lastrow):
            #     if(not row == 2 or not column == lastcol):
            if (not row == lastrow):
                if not((column == 3 and row == 0) or (column == 3 and row == 3)):
                    holes.append(key_place(hole, column, row))
    
    
    
    
    # hole = single_plate()
    #holes = []
    #for column in range(ncols):
        #for row in range(nrows):
            #if (column in [2, 3]) or (not row == lastrow):
                #holes.append(key_place(single_plate(), column, row))

    shape = union(holes)

    return shape


def caps():
    cap = sa_cap()
    caps = None
    for column in range(ncols):
        for row in range(nrows):
            if (not column == lastcol and not row == lastrow):
                if caps is None:
                    caps = key_place(cap, column, row)
                else:
                    caps = caps.add(key_place(cap, column, row))
                    
    caps.append(key_place(cap, 3, 1))
    caps.append(key_place(cap, 3, 2))

    return caps


####################
## Web Connectors ##
####################

web_thickness = 3.5 + .5
post_size = 0.1


def web_post():
    print('web_post()')
    post = cq.Workplane("XY").box(post_size, post_size, web_thickness)
    post = post.translate((0, 0, plate_thickness - (web_thickness / 2)))
    return post


post_adj = post_size / 2


def web_post_tr():
    # print('web_post_tr()')
    return web_post().translate(((mount_width / 2) - post_adj, (mount_height / 2) - post_adj, 0))


def web_post_tl():
    # print('web_post_tl()')
    return web_post().translate((-(mount_width / 2) + post_adj, (mount_height / 2) - post_adj, 0))


def web_post_bl():
    # print('web_post_bl()')
    return web_post().translate((-(mount_width / 2) + post_adj, -(mount_height / 2) + post_adj, 0))


def web_post_br():
    # print('web_post_br()')
    return web_post().translate(((mount_width / 2) - post_adj, -(mount_height / 2) + post_adj, 0))


def triangle_hulls(shapes):
    print('triangle_hulls()')
    hulls = [cq.Workplane('XY')]
    for i in range(len(shapes) - 2):
        hulls.append(hull_from_shapes(shapes[i: (i + 3)]))

    return union(hulls)

webpostbr = web_post_br()
webposttr = web_post_tr()
webpostbl = web_post_bl()
webposttl = web_post_tl()

def connectors():
    print('connectors()')
    hulls = []
    for column in range(ncols - 1):
        for row in range(lastrow):  # need to consider last_row?
            # for row in range(nrows):  # need to consider last_row?
            places = []
            places.append(key_place(webposttl, column + 1, row))
            places.append(key_place(webposttr, column, row))
            places.append(key_place(webpostbl, column + 1, row))
            places.append(key_place(webpostbr, column, row))
            hulls.append(triangle_hulls(places))

    for column in range(ncols):
        # for row in range(nrows-1):
        for row in range(cornerrow):
            places = []
            places.append(key_place(webpostbl, column, row))
            places.append(key_place(webpostbr, column, row))
            places.append(key_place(webposttl, column, row + 1))
            places.append(key_place(webposttr, column, row + 1))
            hulls.append(triangle_hulls(places))

    for column in range(ncols - 1):
        # for row in range(nrows-1):  # need to consider last_row?
        for row in range(cornerrow):  # need to consider last_row?
            places = []
            places.append(key_place(webpostbr, column, row))
            places.append(key_place(webposttr, column, row + 1))
            places.append(key_place(webpostbl, column + 1, row))
            places.append(key_place(webposttl, column + 1, row + 1))
            hulls.append(triangle_hulls(places))
            
    for column in range(ncols):
        # fill pinky column
        for row in range(nrows-1):
            if (column == 3 and row == 3) or (column == 3 and row == 0):
                places = []
                places.append(key_place(webpostbl, column, row))
                places.append(key_place(webpostbr, column, row))
                places.append(key_place(webposttl, column, row ))
                places.append(key_place(webposttr, column, row))
                hulls.append(triangle_hulls(places))

    return union(hulls)


############
## Thumbs ##
############


def thumborigin():
    # print('thumborigin()')
    origin = key_position([mount_width / 2, -(mount_height / 2), 0], 1, cornerrow)
    for i in range(len(origin)):
        origin[i] = origin[i] + thumb_offsets[i]
    return origin


def thumb_tr_place(shape):
    print('thumb_tr_place()')
    shape = rotate(shape, [10, -23, 10])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-12, -16, 3])
    return shape


def thumb_tl_place(shape):
    print('thumb_tl_place()')
    shape = rotate(shape, [10, -23, 10])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-32, -15, -2])
    return shape


def thumb_mr_place(shape):
    print('thumb_mr_place()')
    shape = rotate(shape, [-6, -34, 48])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-29, -40, -13])
    return shape


def thumb_ml_place(shape):
    print('thumb_ml_place()')
    shape = rotate(shape, [6, -34, 40])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-51, -25, -12])
    return shape


def thumb_br_place(shape):
    print('thumb_br_place()')
    shape = rotate(shape, [-16, -33, 54])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-37.8, -55.3, -25.3])
    return shape


def thumb_bl_place(shape):
    print('thumb_bl_place()')
    shape = rotate(shape, [-4, -35, 52])
    shape = shape.translate(thumborigin())
    shape = shape.translate([-56.3, -43.3, -23.5])
    return shape


def thumb_1x_layout(shape, cap=False):
    print('thumb_1x_layout()')
    if cap:
        shapes = thumb_mr_place(shape)
        shapes = shapes.add(thumb_ml_place(shape))
        shapes = shapes.add(thumb_br_place(shape))
        shapes = shapes.add(thumb_bl_place(shape))
    else:
        shapes = union(
            [
                thumb_mr_place(shape),
                thumb_ml_place(shape),
                thumb_br_place(shape),
                thumb_bl_place(shape),
            ]
        )
    return shapes


def thumb_15x_layout(shape, cap=False):
    print('thumb_15x_layout()')
    if cap:
        shape = rotate(shape, (0, 0, 90))
        return thumb_tr_place(shape).add(thumb_tl_place(shape).solids().objects[0])
    else:
        return thumb_tr_place(shape).union(thumb_tl_place(shape))


def double_plate():
    print('double_plate()')
    plate_height = (sa_double_length - mount_height) / 3
    # plate_height = (2*sa_length-mount_height) / 3
    top_plate = cq.Workplane("XY").box(mount_width, plate_height, web_thickness)
    top_plate = translate(top_plate,
                          [0, (plate_height + mount_height) / 2, plate_thickness - (web_thickness / 2)]
                          )
    return union((top_plate, mirror(top_plate, 'XZ')))


def thumbcaps():
    t1 = thumb_1x_layout(sa_cap(1), cap=True)
    # t15 = thumb_15x_layout(rotate(sa_cap(1.5), [0, 0, pi / 2]), cap=True)
    t15 = thumb_15x_layout(sa_cap(1.5), cap=True)
    return t1.add(t15)


def thumb():
    print('thumb()')
    shape = thumb_1x_layout(single_plate())
    shape = shape.union(thumb_15x_layout(single_plate()))
    shape = shape.union(thumb_15x_layout(double_plate()))
    return shape


def thumb_post_tr():
    print('thumb_post_tr()')
    return translate(web_post(),
                     [(mount_width / 2) - post_adj, (mount_height / 1.15) - post_adj, 0]
                     )


def thumb_post_tl():
    print('thumb_post_tl()')
    return translate(web_post(),
                     [-(mount_width / 2) + post_adj, (mount_height / 1.15) - post_adj, 0]
                     )


def thumb_post_bl():
    print('thumb_post_bl()')
    return translate(web_post(),
                     [-(mount_width / 2) + post_adj, -(mount_height / 1.15) + post_adj, 0]
                     )


def thumb_post_br():
    print('thumb_post_br()')
    return translate(web_post(),
                     [(mount_width / 2) - post_adj, -(mount_height / 1.15) + post_adj, 0]
                     )


def thumb_connectors():
    print('thumb_connectors()')
    hulls = []

    # Top two
    hulls.append(
        triangle_hulls(
            [
                thumb_tl_place(thumb_post_tr()),
                thumb_tl_place(thumb_post_br()),
                thumb_tr_place(thumb_post_tl()),
                thumb_tr_place(thumb_post_bl()),
            ]
        )
    )

    # bottom two on the right
    hulls.append(
        triangle_hulls(
            [
                thumb_br_place(webposttr),
                thumb_br_place(webpostbr),
                thumb_mr_place(webposttl),
                thumb_mr_place(webpostbl),
            ]
        )
    )

    # bottom two on the left
    hulls.append(
        triangle_hulls(
            [
                thumb_br_place(webposttr),
                thumb_br_place(webpostbr),
                thumb_mr_place(webposttl),
                thumb_mr_place(webpostbl),
            ]
        )
    )
    # centers of the bottom four
    hulls.append(
        triangle_hulls(
            [
                thumb_bl_place(webposttr),
                thumb_bl_place(webpostbr),
                thumb_ml_place(webposttl),
                thumb_ml_place(webpostbl),
            ]
        )
    )

    # top two to the middle two, starting on the left
    hulls.append(
        triangle_hulls(
            [
                thumb_br_place(webposttl),
                thumb_bl_place(webpostbl),
                thumb_br_place(webposttr),
                thumb_bl_place(webpostbr),
                thumb_mr_place(webposttl),
                thumb_ml_place(webpostbl),
                thumb_mr_place(webposttr),
                thumb_ml_place(webpostbr),
            ]
        )
    )

    # top two to the main keyboard, starting on the left
    hulls.append(
        triangle_hulls(
            [
                thumb_tl_place(thumb_post_tl()),
                thumb_ml_place(webposttr),
                thumb_tl_place(thumb_post_bl()),
                thumb_ml_place(webpostbr),
                thumb_tl_place(thumb_post_br()),
                thumb_mr_place(webposttr),
                thumb_tr_place(thumb_post_bl()),
                thumb_mr_place(webpostbr),
                thumb_tr_place(thumb_post_br()),
            ]
        )
    )

    hulls.append(
        triangle_hulls(
            [
                thumb_tl_place(thumb_post_tl()),
                key_place(webpostbl, 0, cornerrow),
                thumb_tl_place(thumb_post_tr()),
                key_place(webpostbr, 0, cornerrow),
                thumb_tr_place(thumb_post_tl()),
                key_place(webpostbl, 1, cornerrow),
                thumb_tr_place(thumb_post_tr()),
                key_place(webpostbr, 1, cornerrow),
                key_place(webposttl, 2, lastrow),
                key_place(webpostbl, 2, lastrow),
                thumb_tr_place(thumb_post_tr()),
                key_place(webpostbl, 2, lastrow),
                thumb_tr_place(thumb_post_br()),
                key_place(webpostbr, 2, lastrow),
                key_place(webpostbl, 3, lastrow),
                key_place(webposttr, 2, lastrow),
                key_place(webposttl, 3, lastrow),
                key_place(webpostbl, 3, cornerrow),
                key_place(webposttr, 3, lastrow),
                key_place(webpostbr, 3, cornerrow),
                key_place(webpostbl, 4, cornerrow),
            ]
        )
    )

    hulls.append(
        triangle_hulls(
            [
                key_place(webpostbr, 1, cornerrow),
                key_place(webposttl, 2, lastrow),
                key_place(webpostbl, 2, cornerrow),
                key_place(webposttr, 2, lastrow),
                key_place(webpostbr, 2, cornerrow),
                key_place(webpostbl, 3, cornerrow),
            ]
        )
    )

    hulls.append(
        triangle_hulls(
            [
                key_place(webposttr, 3, lastrow),
                key_place(webpostbr, 3, lastrow),
                key_place(webposttr, 3, lastrow),
                key_place(webpostbl, 4, cornerrow),
            ]
        )
    )

    return union(hulls)


##########
## Case ##
##########


def bottom_hull(p, height=0.001):
    print("bottom_hull()")
    shape = None
    for item in p:
        # proj = sl.projection()(p)
        # t_shape = sl.linear_extrude(height=height, twist=0, convexity=0, center=True)(
        #      proj
        # )
        vertices = []
        verts = item.faces('<Z').vertices()
        for vert in verts.objects:
            v0 = vert.toTuple()
            v1 = [v0[0], v0[1], -10]
            vertices.append(np.array(v0))
            vertices.append(np.array(v1))

        t_shape = hull_from_points(vertices)

        # t_shape = translate(t_shape, [0, 0, height / 2 - 10])

        if shape is None:
            shape = t_shape

        for shp in (*p, shape, t_shape):
            try:
                shp.vertices()
            except:
                0
        # shape = shape.union(hull_from_shapes((item, shape, t_shape)))
        shape = shape.union(hull_from_shapes((shape, t_shape)))
        # shape = shape.union(t_shape)

    return shape


left_wall_x_offset = 10
left_wall_z_offset = 3


def left_key_position(row, direction):
    print("left_key_position()")
    pos = np.array(
        key_position([-mount_width * 0.5, direction * mount_height * 0.5, 0], 0, row)
    )
    return list(pos - np.array([left_wall_x_offset, 0, left_wall_z_offset]))


def left_key_place(shape, row, direction):
    print("left_key_place()")
    pos = left_key_position(row, direction)
    return shape.translate(pos)


def wall_locate1(dx, dy):
    print("wall_locate1()")
    return [dx * wall_thickness, dy * wall_thickness, -1]


def wall_locate2(dx, dy):
    print("wall_locate2()")
    return [dx * wall_xy_offset, dy * wall_xy_offset, wall_z_offset]


def wall_locate3(dx, dy):
    print("wall_locate3()")
    return [
        dx * (wall_xy_offset + wall_thickness),
        dy * (wall_xy_offset + wall_thickness),
        wall_z_offset,
    ]


def wall_brace(place1, dx1, dy1, post1, place2, dx2, dy2, post2):
    print("wall_brace()")
    hulls = []

    hulls.append(place1(post1))
    hulls.append(place1(translate(post1, wall_locate1(dx1, dy1))))
    hulls.append(place1(translate(post1, wall_locate2(dx1, dy1))))
    hulls.append(place1(translate(post1, wall_locate3(dx1, dy1))))

    hulls.append(place2(post2))
    hulls.append(place2(translate(post2, wall_locate1(dx2, dy2))))
    hulls.append(place2(translate(post2, wall_locate2(dx2, dy2))))
    hulls.append(place2(translate(post2, wall_locate3(dx2, dy2))))
    shape1 = hull_from_shapes(hulls)

    hulls = []
    hulls.append(place1(translate(post1, wall_locate2(dx1, dy1))))
    hulls.append(place1(translate(post1, wall_locate3(dx1, dy1))))
    hulls.append(place2(translate(post2, wall_locate2(dx2, dy2))))
    hulls.append(place2(translate(post2, wall_locate3(dx2, dy2))))
    shape2 = bottom_hull(hulls)

    return shape1.union(shape2)
    # return shape1


def key_wall_brace(x1, y1, dx1, dy1, post1, x2, y2, dx2, dy2, post2):
    print("key_wall_brace()")
    return wall_brace(
        (lambda shape: key_place(shape, x1, y1)),
        dx1,
        dy1,
        post1,
        (lambda shape: key_place(shape, x2, y2)),
        dx2,
        dy2,
        post2,
    )


def back_wall():
    print("back_wall()")
    x = 0
    shape = cq.Workplane('XY')
    shape = shape.union(key_wall_brace(x, 0, 0, 1, web_post_tl(), x, 0, 0, 1, web_post_tr()))
    for i in range(ncols - 1):
        x = i + 1
        shape = shape.union(key_wall_brace(x, 0, 0, 1, web_post_tl(), x, 0, 0, 1, web_post_tr()))
        shape = shape.union(key_wall_brace(
            x, 0, 0, 1, web_post_tl(), x - 1, 0, 0, 1, web_post_tr()
        ))
    shape = shape.union(key_wall_brace(
        lastcol, 0, 0, 1, web_post_tr(), lastcol, 0, 1, 0, web_post_tr()
    ))
    return shape


def right_wall():
    print("right_wall()")
    y = 0
    shape = cq.Workplane('XY')
    shape = shape.union(
        key_wall_brace(
            lastcol, y, 1, 0, web_post_tr(), lastcol, y, 1, 0, webpostbr
        )
    )
    for i in range(lastrow - 1):
        y = i + 1
        shape = shape.union(key_wall_brace(
            lastcol, y, 1, 0, web_post_tr(), lastcol, y, 1, 0, webpostbr
        ))
        shape = shape.union(key_wall_brace(
            lastcol, y, 1, 0, webpostbr, lastcol, y - 1, 1, 0, web_post_tr()
        ))
    shape = shape.union(key_wall_brace(
        lastcol,
        cornerrow,
        0,
        -1,
        webpostbr,
        lastcol,
        cornerrow,
        1,
        0,
        webpostbr,
    ))
    return shape


def left_wall():
    print('left_wall()')
    shape = cq.Workplane('XY')
    shape = shape.union(wall_brace(
        (lambda sh: key_place(sh, 0, 0)),
        0,
        1,
        web_post_tl(),
        (lambda sh: left_key_place(sh, 0, 1)),
        0,
        1,
        web_post(),
    ))

    shape = shape.union(wall_brace(
        (lambda sh: left_key_place(sh, 0, 1)),
        0,
        1,
        web_post(),
        (lambda sh: left_key_place(sh, 0, 1)),
        -1,
        0,
        web_post(),
    ))

    for i in range(lastrow):
        y = i
        temp_shape1 = wall_brace(
            (lambda sh: left_key_place(sh, y, 1)),
            -1,
            0,
            web_post(),
            (lambda sh: left_key_place(sh, y, -1)),
            -1,
            0,
            web_post(),
        )
        temp_shape2 = hull_from_shapes((
            key_place(web_post_tl(), 0, y),
            key_place(web_post_bl(), 0, y),
            left_key_place(web_post(), y, 1),
            left_key_place(web_post(), y, -1),
        ))
        shape = shape.union(temp_shape1)
        shape = shape.union(temp_shape2)

    for i in range(lastrow - 1):
        y = i + 1
        temp_shape1 = wall_brace(
            (lambda sh: left_key_place(sh, y - 1, -1)),
            -1,
            0,
            web_post(),
            (lambda sh: left_key_place(sh, y, 1)),
            -1,
            0,
            web_post(),
        )
        temp_shape2 = hull_from_shapes((
            key_place(web_post_tl(), 0, y),
            key_place(web_post_bl(), 0, y - 1),
            left_key_place(web_post(), y, 1),
            left_key_place(web_post(), y - 1, -1),
        ))
        shape = shape.union(temp_shape1)
        shape = shape.union(temp_shape2)

    return shape


def front_wall():
    print('front_wall()')
    shape = cq.Workplane('XY')
    shape = shape.union(
        key_wall_brace(
            lastcol, 0, 0, 1, webposttr, lastcol, 0, 1, 0, webposttr
        )
    )
    shape = shape.union(key_wall_brace(
        3, lastrow, 0, -1, webpostbl, 3, lastrow, 0.5, -1, webpostbr
    ))
    shape = shape.union(key_wall_brace(
        3, lastrow, 0.5, -1, webpostbr, 4, cornerrow, 1, -1, webpostbl
    ))
    for i in range(ncols - 4):
        x = i + 4
        shape = shape.union(key_wall_brace(
            x, cornerrow, 0, -1, webpostbl, x, cornerrow, 0, -1,webpostbr
        ))
    for i in range(ncols - 5):
        x = i + 5
        shape = shape.union(key_wall_brace(
            x, cornerrow, 0, -1, webpostbl, x - 1, cornerrow, 0, -1, webpostbr
        ))

    return shape


def thumb_walls():
    print('thumb_walls()')
    # thumb, walls
    shape = cq.Workplane('XY')
    shape = shape.union(
        wall_brace(
            thumb_mr_place, 0, -1, webpostbr, thumb_tr_place, 0, -1, thumb_post_br()
        )
    )
    shape = shape.union(wall_brace(
        thumb_mr_place, 0, -1, webpostbr, thumb_mr_place, 0, -1, webpostbl
    ))
    shape = shape.union(wall_brace(
        thumb_br_place, 0, -1, webpostbr, thumb_br_place, 0, -1, webpostbl
    ))
    shape = shape.union(wall_brace(
        thumb_ml_place, -0.3, 1, webposttr, thumb_ml_place, 0, 1, webposttl
    ))
    shape = shape.union(wall_brace(
        thumb_bl_place, 0, 1, webposttr, thumb_bl_place, 0, 1, webposttl
    ))
    shape = shape.union(wall_brace(
        thumb_br_place, -1, 0, webposttl, thumb_br_place, -1, 0, webpostbl
    ))
    shape = shape.union(wall_brace(
        thumb_bl_place, -1, 0, webposttl, thumb_bl_place, -1, 0, webpostbl
    ))
    # thumb, corners
    shape = shape.union(wall_brace(
        thumb_br_place, -1, 0, webpostbl, thumb_br_place, 0, -1, webpostbl
    ))
    shape = shape.union(wall_brace(
        thumb_bl_place, -1, 0, webposttl, thumb_bl_place, 0, 1, webposttl
    ))
    # thumb, tweeners
    shape = shape.union(wall_brace(
        thumb_mr_place, 0, -1, webpostbl, thumb_br_place, 0, -1, webpostbr
    ))
    shape = shape.union(wall_brace(
        thumb_ml_place, 0, 1, webposttl, thumb_bl_place, 0, 1, webposttr
    ))
    shape = shape.union(wall_brace(
        thumb_bl_place, -1, 0, webpostbl, thumb_br_place, -1, 0, webposttl
    ))
    shape = shape.union(wall_brace(
        thumb_tr_place,
        0,
        -1,
        thumb_post_br(),
        (lambda sh: key_place(sh, 3, lastrow)),
        0,
        -1,
        web_post_bl(),
    ))

    return shape


def thumb_connection():
    print('thumb_connection()')
    shape = cq.Workplane('XY')
    # clunky bit on the top left thumb connection  (normal connectors don't work well)
    shape = shape.union(bottom_hull(
        [
            left_key_place(
                translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1
            ),
            left_key_place(
                translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1
            ),
            thumb_ml_place(translate(web_post_tr(), wall_locate2(-0.3, 1))),
            thumb_ml_place(translate(web_post_tr(), wall_locate3(-0.3, 1))),
        ]
    ))

    # shape = shape.union(hull_from_shapes(

    shape = shape.union(
        hull_from_shapes(
            [
                left_key_place(
                    translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1
                ),
                left_key_place(
                    translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1
                ),
                thumb_ml_place(translate(web_post_tr(), wall_locate2(-0.3, 1))),
                thumb_ml_place(translate(web_post_tr(), wall_locate3(-0.3, 1))),
                thumb_tl_place(thumb_post_tl()),
            ]
        )
    )  # )

    shape = shape.union(hull_from_shapes(
        [
            left_key_place(web_post(), cornerrow, -1),
            left_key_place(
                translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1
            ),
            left_key_place(
                translate(web_post(), wall_locate2(-1, 0)), cornerrow, -1
            ),
            left_key_place(
                translate(web_post(), wall_locate3(-1, 0)), cornerrow, -1
            ),
            thumb_tl_place(thumb_post_tl()),
        ]
    ))

    shape = shape.union(hull_from_shapes(
        [
            left_key_place(web_post(), cornerrow, -1),
            left_key_place(
                translate(web_post(), wall_locate1(-1, 0)), cornerrow, -1
            ),
            key_place(web_post_bl(), 0, cornerrow),
            key_place(translate(web_post_bl(), wall_locate1(-1, 0)), 0, cornerrow),
            thumb_tl_place(thumb_post_tl()),
        ]
    ))

    shape = shape.union(hull_from_shapes(
        [
            thumb_ml_place(web_post_tr()),
            thumb_ml_place(translate(web_post_tr(), wall_locate1(-0.3, 1))),
            thumb_ml_place(translate(web_post_tr(), wall_locate2(-0.3, 1))),
            thumb_ml_place(translate(web_post_tr(), wall_locate3(-0.3, 1))),
            thumb_tl_place(thumb_post_tl()),
        ]
    ))

    return shape


def case_walls():
    print('case_walls()')
    shape = cq.Workplane('XY')
    return (
        union([
            shape,
            back_wall(),
            left_wall(),
            right_wall(),
            front_wall(),
            thumb_walls(),
            thumb_connection(),
        ])
    )


# rj9_start = list(
#     np.array([0, -3, 0])
#     + np.array(
#         key_position(
#             list(np.array(wall_locate3(0, 1)) + np.array([0, (mount_height / 2), 0])),
#             0,
#             0,
#         )
#     )
# )

# rj9_position = (rj9_start[0], rj9_start[1], 11)


# def rj9_cube():
#     print('rj9_cube()')
#     shape = cq.Workplane("XY").box(14.78, 13, 22.38)

#     return shape


# def rj9_space():
#     print('rj9_space()')
#     return rj9_cube().translate(rj9_position)


# def rj9_holder():
#     print('rj9_holder()')
#     shape = cq.Workplane("XY").box(10.78, 9, 18.38).translate((0, 2, 0))
#     shape = shape.union(cq.Workplane("XY").box(10.78, 13, 5).translate((0, 0, 5)))
#     shape = rj9_cube().cut(shape)
#     shape = shape.translate(rj9_position)

#     return shape


# usb_holder_position = key_position(
#     list(np.array(wall_locate2(0, 1)) + np.array([0, (mount_height / 2), 0])), 1, 0
# )
# usb_holder_size = [6.5, 10.0, 13.6]
# usb_holder_thickness = 4


# def usb_holder():
#     print('usb_holder()')
#     shape = cq.Workplane("XY").box(
#         usb_holder_size[0] + usb_holder_thickness,
#         usb_holder_size[1],
#         usb_holder_size[2] + usb_holder_thickness,
#     )
#     shape = shape.translate(
#         (
#             usb_holder_position[0],
#             usb_holder_position[1],
#             (usb_holder_size[2] + usb_holder_thickness) / 2,
#         )
#     )
#     return shape


# def usb_holder_hole():
#     print('usb_holder_hole()')
#     shape = cq.Workplane("XY").box(*usb_holder_size)
#     shape = shape.translate(
#         (
#             usb_holder_position[0],
#             usb_holder_position[1],
#             (usb_holder_size[2] + usb_holder_thickness) / 2,
#         )
#     )
#     return shape


# teensy_width = 20
# teensy_height = 12
# teensy_length = 33
# teensy2_length = 53
# teensy_pcb_thickness = 2
# teensy_holder_width = 7 + teensy_pcb_thickness
# teensy_holder_height = 6 + teensy_width
# teensy_offset_height = 5
# teensy_holder_top_length = 18
# teensy_top_xy = key_position(wall_locate3(-1, 0), 0, centerrow - 1)
# teensy_bot_xy = key_position(wall_locate3(-1, 0), 0, centerrow + 1)
# teensy_holder_length = teensy_top_xy[1] - teensy_bot_xy[1]
# teensy_holder_offset = -teensy_holder_length / 2
# teensy_holder_top_offset = (teensy_holder_top_length / 2) - teensy_holder_length


# def teensy_holder():
#     print('teensy_holder()')
#     s1 = cq.Workplane("XY").box(3, teensy_holder_length, 6 + teensy_width)
#     s1 = translate(s1, [1.5, teensy_holder_offset, 0])

#     s2 = cq.Workplane("XY").box(teensy_pcb_thickness, teensy_holder_length, 3)
#     s2 = translate(s2,
#                    (
#                        (teensy_pcb_thickness / 2) + 3,
#                        teensy_holder_offset,
#                        -1.5 - (teensy_width / 2),
#                    )
#                    )

#     s3 = cq.Workplane("XY").box(teensy_pcb_thickness, teensy_holder_top_length, 3)
#     s3 = translate(s3,
#                    [
#                        (teensy_pcb_thickness / 2) + 3,
#                        teensy_holder_top_offset,
#                        1.5 + (teensy_width / 2),
#                    ]
#                    )

#     s4 = cq.Workplane("XY").box(4, teensy_holder_top_length, 4)
#     s4 = translate(s4,
#                    [teensy_pcb_thickness + 5, teensy_holder_top_offset, 1 + (teensy_width / 2)]
#                    )

#     shape = union((s1, s2, s3, s4))

#     shape = shape.translate([-teensy_holder_width, 0, 0])
#     shape = shape.translate([-1.4, 0, 0])
#     shape = translate(shape,
#                       [teensy_top_xy[0], teensy_top_xy[1] - 1, (6 + teensy_width) / 2]
#                       )

#     return shape


# def screw_insert_shape(bottom_radius, top_radius, height):
#     print('screw_insert_shape()')
#     if bottom_radius == top_radius:
#         base = cq.Workplane('XY').union(cq.Solid.makeCylinder(radius=bottom_radius, height=height)).translate(
#             (0, 0, -height / 2)
#         )
#     else:
#         base = cq.Workplane('XY').union(
#             cq.Solid.makeCone(radius1=bottom_radius, radius2=top_radius, height=height)).translate((0, 0, -height / 2))

#     shape = union((
#         base,
#         cq.Workplane('XY').union(cq.Solid.makeSphere(top_radius)).translate((0, 0, (height / 2))),
#     ))
#     return shape


# def screw_insert(column, row, bottom_radius, top_radius, height):
#     print('screw_insert()')
#     shift_right = column == lastcol
#     shift_left = column == 0
#     shift_up = (not (shift_right or shift_left)) and (row == 0)
#     shift_down = (not (shift_right or shift_left)) and (row >= lastrow)

#     if shift_up:
#         position = key_position(
#             list(np.array(wall_locate2(0, 1)) + np.array([0, (mount_height / 2), 0])),
#             column,
#             row,
#         )
#     elif shift_down:
#         position = key_position(
#             list(np.array(wall_locate2(0, -1)) - np.array([0, (mount_height / 2), 0])),
#             column,
#             row,
#         )
#     elif shift_left:
#         position = list(
#             np.array(left_key_position(row, 0)) + np.array(wall_locate3(-1, 0))
#         )
#     else:
#         position = key_position(
#             list(np.array(wall_locate2(1, 0)) + np.array([(mount_height / 2), 0, 0])),
#             column,
#             row,
#         )

#     shape = screw_insert_shape(bottom_radius, top_radius, height)
#     shape = shape.translate((position[0], position[1], height / 2))

#     return shape


# def screw_insert_all_shapes(bottom_radius, top_radius, height):
#     print('screw_insert_all_shapes()')
#     shape = (
#         screw_insert(0, 0, bottom_radius, top_radius, height),
#         screw_insert(0, lastrow, bottom_radius, top_radius, height),
#         screw_insert(2, lastrow + 0.3, bottom_radius, top_radius, height),
#         screw_insert(3, 0, bottom_radius, top_radius, height),
#         screw_insert(lastcol, 1, bottom_radius, top_radius, height),
#     )

#     return shape


# screw_insert_height = 3.8
# screw_insert_bottom_radius = 5.31 / 2
# screw_insert_top_radius = 5.1 / 2
# screw_insert_holes = screw_insert_all_shapes(
#     screw_insert_bottom_radius, screw_insert_top_radius, screw_insert_height
# )
# screw_insert_outers = screw_insert_all_shapes(
#     screw_insert_bottom_radius + 1.6,
#     screw_insert_top_radius + 1.6,
#     screw_insert_height + 1.5,
# )
# screw_insert_screw_holes = screw_insert_all_shapes(1.7, 1.7, 350)

# wire_post_height = 7
# wire_post_overhang = 3.5
# wire_post_diameter = 2.6


# def wire_post(direction, offset):
#     print('wire_post()')
#     s1 = cq.Workplane("XY").box(
#         wire_post_diameter, wire_post_diameter, wire_post_height
#     )
#     s1 = translate(s1, [0, -wire_post_diameter * 0.5 * direction, 0])

#     s2 = cq.Workplane("XY").box(
#         wire_post_diameter, wire_post_overhang, wire_post_diameter
#     )
#     s2 = translate(s2,
#                    [0, -wire_post_overhang * 0.5 * direction, -wire_post_height / 2]
#                    )

#     shape = union((s1, s2))
#     shape = shape.translate([0, -offset, (-wire_post_height / 2) + 3])
#     shape = rotate(shape, [-alpha / 2, 0, 0])
#     shape = shape.translate((3, -mount_height / 2, 0))

#     return shape


# def wire_posts():
#     print('wire_posts()')
#     shape = thumb_ml_place(wire_post(1, 0).translate([-5, 0, -2]))
#     shape = shape.union(thumb_ml_place(wire_post(-1, 6).translate([0, 0, -2.5])))
#     shape = shape.union(thumb_ml_place(wire_post(1, 0).translate([5, 0, -2])))

#     for column in range(lastcol):
#         for row in range(lastrow - 1):
#             shape = union([
#                 shape,
#                 key_place(wire_post(1, 0).translate([-5, 0, 0]), column, row),
#                 key_place(wire_post(-1, 6).translate([0, 0, 0]), column, row),
#                 key_place(wire_post(1, 0).translate([5, 0, 0]), column, row),
#             ])
#     return shape

from random import random
def model_right():
    print('model_right()')
    #shape = single_plate()
    
    shape = cq.Workplane('XY').union(key_holes())
    shape = shape.union(connectors())
    # shape = shape.union(thumb())
    # shape = shape.union(thumb_connectors())
    # s2 = cq.Workplane('XY').union(case_walls())
    # s2 = union([s2, *screw_insert_outers])
    # # s2 = s2.union(teensy_holder())
    # s2 = s2.union(usb_holder())

    # s2 = s2.cut(rj9_space())
    # s2 = s2.cut(usb_holder_hole())
    # s2 = s2.cut(union(screw_insert_holes))

    # shape = shape.union(rj9_holder())
    # shape = shape.union(s2, tol=.01)
    # shape = shape.union(wire_posts())
    # block = cq.Workplane("XY").box(350, 350, 40)
    # block = block.translate((0, 0, -20))
    # shape = shape.cut(block)

    # if show_caps:
    #     shape = shape.add(thumbcaps())
    #     shape = shape.add(caps())

    print('end of model right')
    return shape


mod_r = model_right()

show(mod_r, grid=False)

#cq.exporters.export(w=mod_r, fname=path.join(r"..", "things", r"right_og_py.step"), exportType='STEP')

# cq.exporters.export(w=mod_r.mirror('YZ'), fname=path.join(r"..", "things", r"left_og_py.step"), exportType='STEP')


# def baseplate():
#     shape = mod_r

#     shape = shape.translate((0, 0, -0.1))

#     square = cq.Workplane('XY').rect(1000, 1000)
#     for wire in square.wires().objects:
#         plane = cq.Workplane('XY').add(cq.Face.makeFromWires(wire))

#     shape = shape.intersect(plane)

#     return shape


# base = baseplate()

# cq.exporters.export(w=base, fname=path.join(r"..", "things", r"plate_og_py.step"), exportType='STEP')
# cq.exporters.export(w=base, fname=path.join(r"..", "things", r"plate_og_py.dxf"), exportType='DXF')