import os
FP = "/home/siheng/Documents/Calibration/ICRA2023/results/deltille/gopro-6x6-sep12-200f/camera_0"
import numpy as np
# File format
FILENAME = 0
WIDTH = 1
HEIGHT = 2
NUM_CORNERS = 3
ENCODING = 4
DATA = 5

def numpify_orpc_corners(filepath, data_index, coord_index):
    l_orpc_file = os.listdir(filepath)
    l_orpc_file.sort()

    all_corners = []
    for orpc_file in l_orpc_file:
        orpc_fn = os.path.join(filepath, orpc_file)
        with open(orpc_fn) as f:
            lines = f.readlines()

        for line in lines[data_index:]:
            x,y = line.split(",")[coord_index:]
            x,y = float(x), float(y)
            all_corners.append([x,y])

    # To save this corner.
    np_corners = np.array(all_corners)
    return np_corners

def numpify_corners(filepath, data_index, coord_index):
    all_corners = []
    with open(filepath) as f:
        lines = f.readlines()

    for line in lines[data_index:]:
        x,y = line.split(",")[coord_index:]
        x,y = float(x), float(y)
        all_corners.append([x,y])

    # To save this corner.
    np_corners = np.array(all_corners)
    return np_corners
