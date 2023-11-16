import os
import glob
from unittest import result
from scripts.detector_evaluation.process_orpc import numpify_corners, numpify_orpc_corners
from aruco import aruco
import numpy as np
import pandas as pd
import pickle
def glob_this(filepath):
    return glob.glob(os.path.join(filepath,"*"))

def run_experiments(image_folder, results_filepath, repo_folder):
    KAESS_AT_COMMAND =  os.path.join(repo_folder, "kaess-apriltags/bin/apriltags_demo")
    APRILTAG3_COMMAND = os.path.join(repo_folder, "apriltag/build/apriltag_demo")
    DELTILLE_COMMAND =  os.path.join(repo_folder, "deltille/build/apps/deltille_detector")
    # image_folder sample input: /home/siheng/Documents/TartanCalib/Datasets/022723_Boards/022723_aprilboard/jpeg/BF5M2223S129C
    # repo_folder sample input: /home/siheng/dha/tartancalib-evaluation
    corners_dict = {'deltille':0, 'at3':0, 'kaess-at3':0, 'aruco':0}  

    result_bag_name = image_folder.split('/')[-1]

    #############################
    # Experiment 1: Kaess's AT. #
    #############################
    # if RUN_EXPERIMENT_1:
        # DATA_INDEX / COORD_INDEX are constants for each experiment type.
        # Expresses in which index you may retrieve relevant information.
    KAESS_AT3_DATA_INDEX = 0
    KAESS_AT3_COORD_INDEX = 0


    result_folder = os.path.join(results_filepath, "kaess-at")
    if not os.path.isdir(result_folder):
        os.makedirs(result_folder)
    result_filename = os.path.join(result_folder, "KAESS-AT-" + result_bag_name + ".txt")

    exp_1_command = KAESS_AT_COMMAND + " " + image_folder + "/*.jpg" + " -o " + result_filename
    print("\nEXPERIMENT 1: {}".format(exp_1_command))
    os.system(exp_1_command)

    # Convert corners into numpy array + save into results.
    n_corners, np_corners = numpify_corners(result_filename, KAESS_AT3_DATA_INDEX, KAESS_AT3_COORD_INDEX)
    np_folder = os.path.join(results_filepath, "kaess-at")
    if not os.path.isdir(np_folder):
        os.makedirs(np_folder)
    kaess_np_fp = os.path.join(np_folder, "kaess_AT3-" + result_bag_name + ".npy")

    print("Writing {} corners to: {}".format(n_corners, kaess_np_fp))
    print(len(np_corners))
    with open(kaess_np_fp, 'wb') as f:
        pickle.dump(np_corners, f)
    corners_dict['kaess-at3'] = n_corners

    ###############################
    # Experiment 2: Apriltag3 AT. #
    ###############################
    AT3_DATA_INDEX = 0
    AT3_COORD_INDEX = 0

    result_folder = os.path.join(results_filepath, "AT3")
    if not os.path.isdir(result_folder):
        os.makedirs(result_folder)
    result_filename = os.path.join(result_folder, "AT3-" + result_bag_name + ".txt")
    exp_2_command = APRILTAG3_COMMAND + " -q " + image_folder + "/*.jpg" + " -o " + result_filename

    print("\nEXPERIMENT 2: {}".format(exp_2_command))
    os.system(exp_2_command)

    # Convert corners into numpy array + save into results.
    n_corners, np_corners = numpify_corners(result_filename, AT3_DATA_INDEX, AT3_COORD_INDEX) 
    np_folder = os.path.join(results_filepath, "AT3")
    if not os.path.isdir(np_folder):
        os.makedirs(np_folder)
    at3_np_fp = os.path.join(np_folder, "AT3-" + result_bag_name + ".npy")
    print("Writing {} corners to: {}".format(n_corners, at3_np_fp))
    with open(at3_np_fp, 'wb') as f:
        pickle.dump(np_corners, f)
    corners_dict['at3'] = n_corners

    ###########################
    # Experiment 3: Deltille. #
    ###########################
    # if RUN_EXPERIMENT_3:
    DELTILLE_DATA_INDEX = 5
    DELTILLE_COORD_INDEX = 0
    BOARD_FILEPATH = os.path.join(repo_folder, "boards", "april_6x6.dsc")

    result_folder = os.path.join(results_filepath, "deltille")
    if not os.path.isdir(result_folder):
        os.makedirs(result_folder)
    result_filename = os.path.join(result_folder, "deltille-" + result_bag_name)
    exp_3_command = DELTILLE_COMMAND + " -t " + BOARD_FILEPATH + " -f " + image_folder + "/*.jpg" + " -o " + result_filename
    print("\nEXPERIMENT 3: {}".format(exp_3_command))
    os.system(exp_3_command)
    
    # Convert corners into numpy array + save into results.
    np_corners, n_features = numpify_orpc_corners(result_filename, DELTILLE_DATA_INDEX, DELTILLE_COORD_INDEX) # Technically doesn't numpify.

    np_folder = os.path.join(results_filepath, "deltille")
    if not os.path.isdir(np_folder):
        os.makedirs(np_folder)
    deltille_np_fp = os.path.join(np_folder, "deltille-" + result_bag_name + ".npy")

    print("Written {} corners to: {}".format(n_features, deltille_np_fp))
    with open(deltille_np_fp, 'wb') as f:
        pickle.dump(np_corners, f)
    corners_dict['deltille'] = n_features

    #######################
    # Experiment 4: Aruco #
    #######################
    # if RUN_EXPERIMENT_4:
        # ARUCO_DATA_INDEX = None
        # ARUCO_COORD_INDEX = 3
    print("\nEXPERIMENT 4: {}".format("Running aruco"))
    result_folder = os.path.join(results_filepath, "aruco")
    corners_dict['aruco'] = aruco.aruco_experiment(image_folder, result_folder, result_bag_name)

    # 2: Kaess-AT, 3: AT, 4: deltille, 5:aruco
    def record_detection_to_table(np_corners, detect_array, detector_idx):
        for frames in np_corners:
            for corner_frame in frames:
                frame_id = corner_frame[0]
                corner_id = corner_frame[1]
                detect_array[frame_id, corner_id, detector_idx] = 1

    img_count = len(glob.glob1(image_folder, "*.jpg"))
    detection_list = []
    print("image number is", img_count)
    for frame_num in range(img_count):
        corners = []
        for corner_id in range(144):
            corners.append([frame_num, corner_id, 0, 0, 0, 0])
        detection_list.append(corners)

    detection_array = np.array(detection_list).astype(int)
    
    k_at3_path = os.path.join(results_filepath, "kaess-at", "kaess_AT3-" + result_bag_name + ".npy")
    np_corners = np.load(k_at3_path, allow_pickle = True)
    record_detection_to_table(np_corners, detection_array, 2)

    at3_path = os.path.join(results_filepath, "AT3", "AT3-" + result_bag_name + ".npy")
    np_corners = np.load(at3_path, allow_pickle = True)
    record_detection_to_table(np_corners, detection_array, 3)

    deltille_path = os.path.join(results_filepath, "deltille", "deltille-" + result_bag_name + ".npy")
    np_corners = np.load(deltille_path, allow_pickle = True)
    record_detection_to_table(np_corners, detection_array, 4)

    aruco_path = os.path.join(results_filepath, "aruco", "aruco-" + result_bag_name + ".npy")
    np_corners = np.load(aruco_path, allow_pickle = True)
    record_detection_to_table(np_corners, detection_array, 5)

    result_path = os.path.join(results_filepath, "detection_results-" + result_bag_name + ".npy")
    detection_array_2d = detection_array.reshape(-1, 6)
    np.save(result_path, detection_array_2d)
    # print(detection_array_2d)

    print("EXPERIMENTS COMPLETE: {}".format(result_bag_name))
    return corners_dict    
