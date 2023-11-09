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
            frame_id, corner_id, isOrdered, x, y = line.split(",")[coord_index:]
            frame_id, corner_id, x, y = int(frame_id), int(corner_id), float(x), float(y)
            corner_id = int(corner_id)
            row_top = corner_id // 12
            col_left = corner_id % 12
            tag_row = row_top // 2
            tag_col = col_left // 2
            tag_id = (5 - tag_row) * 6 + tag_col

            if (row_top % 2 == 0) and (col_left % 2 == 0):
                unified_id = tag_id * 4 + 3
            elif (row_top % 2 == 0) and (col_left % 2 == 1):
                unified_id = tag_id * 4 + 2
            elif (row_top % 2 == 1) and (col_left % 2 == 1):
                unified_id = tag_id * 4 + 1
            elif (row_top % 2 == 1) and (col_left % 2 == 0):
                unified_id = tag_id * 4 + 0

            orpc_corners.append([frame_id, unified_id, x, y])
            n_corners +=1
            
        # orpc_corners = np.array(orpc_corners)
        sorted_orpc_corners = sorted(orpc_corners, key=lambda x: x[1])
        all_corners.append(sorted_orpc_corners)

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
        frame_n, corner_id, x, y = line.split(",")[coord_index:]
        n_corners += 1
        if frame_iterator == int(frame_n):
            frame_n, corner_id, x, y = int(frame_n), int(corner_id), float(x), float(y)
            frame_corners.append([frame_n, corner_id, x, y]) # current frame corners, while iterator matches frame #
        else:
            sorted_corners = sorted(frame_corners, key=lambda x: x[1])
            all_corners.append(sorted_corners)
            frame_iterator += 1
            frame_n, corner_id, x, y = int(frame_n), int(corner_id), float(x), float(y)
            frame_corners = [[frame_n, corner_id, x, y],] # "Re-initialization condition"

    # To save this corner.
    # np_corners = np.array(all_corners)
    return n_corners, all_corners
