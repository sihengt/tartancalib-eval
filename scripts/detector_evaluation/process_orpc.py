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
    n_corners = 0
    for orpc_file in l_orpc_file:
        orpc_corners = []
        orpc_fn = os.path.join(filepath, orpc_file)
        with open(orpc_fn) as f:
            lines = f.readlines()

        for line in lines[data_index:]:
            x,y = line.split(",")[coord_index:]
            x,y = float(x), float(y)
            orpc_corners.append([x,y])
            n_corners +=1
            
        # orpc_corners = np.array(orpc_corners)
        
        all_corners.append(orpc_corners)

    # To save this corner.
    # np_corners = np.array(all_corners)

    return all_corners, n_corners

def numpify_corners(filepath, data_index, coord_index):
    all_corners = []
    frame_corners = []
    n_corners = 0

    with open(filepath) as f:
        lines = f.readlines()

    frame_iterator = 0
    for line in lines[data_index:]:
        frame_n,x,y = line.split(",")[coord_index:]
        n_corners += 1
        if frame_iterator == int(frame_n):
            x,y = float(x), float(y)
            frame_corners.append([x,y]) # current frame corners, while iterator matches frame #
        else:
            all_corners.append(frame_corners)
            frame_iterator += 1
            x,y = float(x), float(y)
            frame_corners = [[x,y],] # "Re-initialization condition"
    all_corners.append([frame_corners])

    # To save this corner.
    # np_corners = np.array(all_corners)
    return n_corners, all_corners
