import numpy as np
from numpy import pi, math
import corebasehelpers as cbh

# ######################
# ## Shape parameters ##
# ######################
counter = 0
show_caps = False

nrows = 5  # key rows
ncols = 4  # key columns

alpha = pi / 6.0  # curvature of the columns
beta = pi / 24.0  # curvature of the rows
centerrow = nrows - 3.5 # controls front_back tilt
centercol = 1.5  # controls left_right tilt / tenting (higher number is more tenting)
tenting_angle = 43.5  # or, change this for more precise tenting control

if nrows > 5:
    column_style = "orthographic"
else:
    column_style = "standard"  # options include :standard, :orthographic, and :fixed


keyboard_offset = [0, 0 ,37]  # controls overall height# original=9 with centercol=3# use 16 for centercol=2

extra_width = 3.5  # extra space between the base of keys# original= 2
extra_height = -0.5  # original= 0.5

#extra_width = 2.5  # extra space between the base of keys# original= 2
#extra_height = 1.0  # original= 0.5

## Settings for column_style == :fixed
## The defaults roughly match Maltron settings
##   http://patentimages.storage.googleapis.com/EP0219944A2/imgf0002.png
## fixed_z overrides the z portion of the column ofsets above.
## NOTE: THIS DOESN'T WORK QUITE LIKE I'D HOPED.
fixed_angles = [cbh.deg2rad(10), cbh.deg2rad(10), 0, 0, 0, cbh.deg2rad(-15), cbh.deg2rad(-15)]
fixed_x = [-41.5, -22.5, 0, 20.3, 41.4, 65.5, 89.6]  # relative to the middle finger
fixed_z = [12.1, 8.3, 0, 5, 10.7, 14.5, 17.5]
fixed_tenting = cbh.deg2rad(0)

#######################
## General variables ##
#######################

lastrow = nrows - 1
cornerrow = lastrow - 1
lastcol = ncols - 1

###################
## Key variables ##
###################

column_zero_offset = [-4.0, 3.0, -1]
column_one_offset = [0.0, 3.6, -3.15]
column_two_offset = [1.2, 0.0, -1.7]
column_three_offset = [-1.07, 5.3, 16.25]
column_default_offset = [0, 0, 0]

#####################
## Thumb variables ##
#####################

thumb_offsets = [6, -3, 7]

########################
## Joystick variables ##
########################

joystick_width = 32.0
joystick_length = 36.0
joystick_height = 21.5

#joystick_rotation = [6,-59,209.1]
#joystick_offset = [-45.7,-29.75,17.7]

####new
#joystick_rotation = [6,-59,209.1]
#joystick_offset = [-48.2,-30,17.7]

joystick_rotation = [6,-45,210.1]
joystick_offset = [-54.7,-30.15,22.5]

########################
## Display variables ##
########################

display_width = 88
display_length = 39
display_height = 9

display_rotation = [43,0,-23]
display_offset = [-95,17,56]

#################
## Switch Hole ##
#################

keyswitch_height = 14.197  ## Was 14.1, then 14.25
keyswitch_width = 14.197

#keyswitch_height = 14.3  ## Was 14.1, then 14.25
#keyswitch_width = 14.3

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

##########################
## SA Keycap Parameters ##
##########################

sa_length = 18.25
sa_double_length = 37.5

##########################
## Placement Parameters ##
##########################

cap_top_height = plate_thickness + sa_profile_key_height
row_radius = ((mount_height + extra_height) / 2) / (np.sin(alpha / 2)) + cap_top_height
column_radius = (((mount_width + extra_width) / 2) / (np.sin(beta / 2))) + cap_top_height
column_x_delta = -1 - column_radius * np.sin(beta)
column_base_angle = beta * (centercol - 2)

###############################
## Web Connector Parameters ##
###############################

web_thickness = 4.0
post_size = 0.1

###############################
## Web Post Parameters ##
###############################

post_adj = 0

###############################
## Joystick Post Parameters ##
###############################

joy_adj = -0.3

###############################
## Display Post Parameters ##
###############################

display_horizontal_adj = 0.7
display_vertical_adj = -1.4

#####################
## Case Parameters ##
#####################

wall_z_offset = -15  # length of the first downward_sloping part of the wall (negative)
wall_xy_offset = 5  # offset in the x and/or y direction for the first downward_sloping part of the wall (negative)
wall_thickness = 2  # wall thickness parameter# originally 5

left_wall_x_offset = 12.5
left_wall_z_offset = 3
