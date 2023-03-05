import xml.etree.ElementTree as ET
import numpy as np
import cv2
import pickle
import os

"""
Takes SVG path and outputs coordinates.
Only equipped to read for M and C
"""

MOVE_TO = "M"
CURVE = "C"
DEBUG = False
DEBUG_IMG = False

"""
Feed this function coordinates, get list of coords.
"""
def get_coords_from_string(s):
    #121.00,59.12
    s_coord = s.split(',')
    if DEBUG:
        print(s)
        print(float(s_coord[0]), float(s_coord[1]))
    return [float(s_coord[0]), float(s_coord[1])]

def traverse_M(string):
    #M 121.00,59.12
    if DEBUG:
        print(string.split(' '))
    coord_string = string.split(' ')[1]
    coords = get_coords_from_string(coord_string)
    return coords

def traverse_C(string):
    string = " ".join(string.split())
    coords = string.split(" ")
    coords = coords[1:]
    assert (len(coords) % 3 == 0)
    coords = coords[2::3]
    l_coords = []
    for coord in coords:
        l_coords.append(get_coords_from_string(coord))
    return l_coords

# Find all the points with M or C. Returns list of these points
def get_breakpoints(string):
    counter = 0
    breakpoints = []
    for letter in string:
        if letter == MOVE_TO:
            breakpoints.append(counter)
        if letter == CURVE:
            breakpoints.append(counter)
        counter += 1
    return breakpoints

def parse_svg_path(path):
    bp = get_breakpoints(path)
    if DEBUG:
        print(bp)
    index_minus_one = len(bp) - 1
    
    l_coords = []
    for x in range(index_minus_one):
        current_path = path[bp[x]:bp[x+1]]
        if current_path[0] == "M":
            current_coords = traverse_M(current_path)
            l_coords.append(current_coords)
        else:
            l_current_coords = traverse_C(current_path)
            for i_coord in l_current_coords:
                l_coords.append(i_coord)

    # Last portion
    rest_of_path = path[bp[-1]:]
    # Remove unnecessary spaces
    if rest_of_path[0] == "M":
        current_coords = traverse_M(rest_of_path)
        l_coords.append(current_coords)
    elif rest_of_path[0] == "C":
        l_current_coords = traverse_C(rest_of_path)
        for i_coord in l_current_coords:
            l_coords.append(i_coord)
    return l_coords


# TODO: FS.
file = "/home/siheng/Documents/Calibration/ICRA2023/annotated/paths/gopro-6x6-1663019984.945267.path"
dbg_image = "/home/siheng/Documents/Calibration/ICRA2023/annotate/gopro-6x6/1663019984.945267.png"

ANNOTATED_FILEPATH = "/home/siheng/Documents/Calibration/ICRA2023/annotated/paths"
CORNER_FILEPATH = "/home/siheng/Documents/Calibration/ICRA2023/corner-accuracy"
DEBUG_IMAGE_FILEPATH = "/home/siheng/Documents/Calibration/ICRA2023/annotate/"

path_files = os.listdir(ANNOTATED_FILEPATH)
total_corners = 0
for path_fn in path_files:
    path_fp = os.path.join(ANNOTATED_FILEPATH, path_fn)
    path_name = path_fn[:-5]
    path_name += ".pkl"
    path_fp_out = os.path.join(CORNER_FILEPATH, path_name)
    tree = ET.parse(path_fp)
    root = tree.getroot()

    for child in root:
        corner_coords = parse_svg_path(child.attrib['d'])
        break
    
    print("Dumping to {}".format(path_fp_out))
    with open(path_fp_out, 'ab') as p_corner:
        pickle.dump(corner_coords, p_corner)

    if DEBUG_IMG:
        dbg_img_folder = path_name.split("_")[0]
        dbg_image = os.path.join(DEBUG_IMAGE_FILEPATH, dbg_img_folder)
        img_name = path_fn.split("_")[1:][0]
        dbg_image = os.path.join(dbg_image, img_name[:-5] + ".png")
        print(dbg_image)
        img = cv2.imread(dbg_image,cv2.IMREAD_COLOR)
        for coord in corner_coords:
            cv2.circle(img, (int(coord[0]), int(coord[1])), 5, (0,255,0), 2)
        cv2.imshow("hi", img)
        cv2.waitKey(0)

    print("Corners:{}".format(len(corner_coords)))
    assert(len(corner_coords) == 280 or len(corner_coords) == 144)
    total_corners += len(corner_coords)

print("TOTAL CORNERS ANNOTATED={}".format(total_corners))
