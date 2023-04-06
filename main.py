import os
import argparse
import sys
import pandas as pd
import glob 
from scripts.preprocessing import rosbag_to_jpg as ros2jpg
from scripts.detector_evaluation.run_experiments import run_experiments

JPEG_FOLDER_PREFIX = "jpeg"
TARTANCALIB_EVAL_FOLDER = sys.path[0]

def get_bag_filenames(input_folder):
    """ Helper function to get all bagfiles """
    # bag_files = [f for f in os.listdir(input_folder) if f.endswith('.bag')]
    bag_files = glob.glob(os.path.join(input_folder,'**/*.bag'))
    print(bag_files)
    return bag_files

def main():
    """ Main entrypoint to generating tables """
    # Part 1: rosbag to jpg
    parser = argparse.ArgumentParser(description="Convert ROSbag into individual jpg images.")
    parser.add_argument(
        '-i',
        '--input_folder',
        required=True,
        help='Folder containing rosbags to process.')
    parser.add_argument(
        '-r',
        '--results_folder',
        required=True,
        help='Folder to store results in.'
    )
    parser.add_argument(
        '-t',
        '--topic',
        default = "/camera_0/image_raw"
    )
    args = parser.parse_args()
    assert os.path.isdir(args.input_folder), "Check input folder. You entered: {}".format(args.input_folder)
    assert os.path.isdir(args.results_folder), "Check results folder. You entered: {}".format(args.results_folder)

    bag_files = get_bag_filenames(args.input_folder)
    assert len(bag_files) > 0, "No .bag files within folder. Exiting."

    # Make a loop and do this:
    for f in bag_files:
        bag_name = f.split('.bag')[0]
        image_topic = args.topic # TODO: un-hardcode this.
        print(image_topic)
        # print("jpg_fn={}".format(os.path.join(args.input_folder, JPEG_FOLDER_PREFIX, jpg_fn)))
        jpg_path = os.path.join(args.input_folder, JPEG_FOLDER_PREFIX, bag_name)
        if not os.path.isdir(jpg_path):
            os.makedirs(jpg_path)
        ros2jpg.rosbag_to_jpg(os.path.join(args.input_folder, f), jpg_path, image_topic)

    # Part 2: run experiments
    
    table_data = {}
    for f in bag_files:
        bag_name = f.split('.bag')[0]
        jpg_path = os.path.join(args.input_folder, JPEG_FOLDER_PREFIX, bag_name)
        print(jpg_path)
        corners_dict = run_experiments(jpg_path, args.results_folder, TARTANCALIB_EVAL_FOLDER) 
        
        table_data[bag_name] = [
            corners_dict['deltille'],
            corners_dict['at3'],
            corners_dict['kaess-at3'], 
            corners_dict['aruco']
        ]
    print(table_data)        

    columns = ["Deltille", "AT3", "Kaess-AT3", "ArUco"]
    df = pd.DataFrame.from_dict(table_data, orient="index", columns=columns)
    
    print(df)
    df.to_csv(os.path.join(args.results_folder, "total_corners_detected.csv"))
        
        # Use bag name as data entry
        # Create table.



    
    pass

if __name__ == "__main__":
    main()