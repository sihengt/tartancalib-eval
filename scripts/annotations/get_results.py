from cgitb import small
import os
import pickle
import cv2
import pandas as pd

ANNOTATED_FILEPATH = "/home/siheng/Documents/Calibration/ICRA2023/annotated/paths"
GT_FILEPATH = "/home/siheng/Documents/Calibration/ICRA2023/corner-accuracy"
COORD_FILEPATH = "/home/siheng/Documents/Calibration/ICRA2023/annotate/"

def read_txt_into_list(txt):
    l_coords = []
    for line in txt:
        line = line.split(',')
        l_coords.append([float(line[0]), float(line[1])])
    return l_coords

def distance(coord_1, coord_2):
    x1, y1 = coord_1
    x2, y2 = coord_2
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def find_closest_coord(ref_coord, l_coords, image_fp):
    smallest_distance = 10000
    smallest_i = -1
    keep = True
    for i in range(len(l_coords)):
        if distance(ref_coord, l_coords[i]) < smallest_distance:
            smallest_i = i
            smallest_distance = distance(ref_coord, l_coords[i])

    if smallest_distance > 10:
        return -1, -1
    if smallest_distance > 4:
        img = cv2.imread(image_fp,cv2.IMREAD_COLOR)
        cv2.circle(img, (int(ref_coord[0]), int(ref_coord[1])), 5, (0,255,0), 2)
        cv2.circle(img, (int(l_coords[smallest_i][0]), int(l_coords[smallest_i][1])), 5, (255,0,0), 2)
        cv2.imshow("hi", img)
        cv2.waitKey(3000)

        print("Found ground truth point:{} closest to evaluation point:{}".format(l_coords[smallest_i], ref_coord))
        print("Smallest_dist = {} ".format(smallest_distance))
        print("Are you keeping this?")
        while True:
            input_key = input()
            if input_key != "y" and input_key != "n":
                print("Only y or n accepted")
            elif input_key == "y":
                keep = True
                break
            elif input_key =="n":
                keep = False
                break
        
        cv2.destroyAllWindows()
    if keep:
        return smallest_i, smallest_distance
    else:
        return -1, -1

# MAIN LOOP
gt_files = os.listdir(GT_FILEPATH)
for gt_fn in gt_files:
    if not gt_fn.endswith(".pkl"):
        continue
    gt_fp = os.path.join(GT_FILEPATH, gt_fn)

    # Get the ground truth
    with open(gt_fp, 'rb') as p_corner:
        gt_corner_coords = pickle.load(p_corner)
    
    print(gt_fn)
    camera_folder = gt_fn.split("_")[0]
    annotation_file = gt_fn.split("_")[1][:-4]
    # print(camera_folder)
    # print(annotation_file)

    camera_fp = os.path.join(COORD_FILEPATH, camera_folder)
    image_fp = os.path.join(camera_fp, [x for x in os.listdir(camera_fp) if x.startswith(annotation_file) and x.endswith(".png")][0])
    # Files with method coords.
    coord_files = [x for x in os.listdir(camera_fp) if x.startswith(annotation_file) and x.endswith(".txt")]
    coord_files.sort()

    current_data_dict = {}
    for file in coord_files:
        print("Currently reading {}".format(file))
        # THIS IS WHERE YOU COMPUTE THE DISTANCE AND POPULATE DATAFRAME
        method_name = file.split("_")[-1][:-4]
        if method_name not in current_data_dict:
            current_data_dict[method_name] = []
        
        with open(os.path.join(camera_fp, file)) as f:
            lines = f.readlines()
            eval_corner_coords = read_txt_into_list(lines)

        # # compare eval_corner_coords to gt_corner_coords and populate dictionary.
        dict_eval_corner_distance = {}
        for eval_coord in eval_corner_coords:
            gt_i, dist = find_closest_coord(eval_coord, gt_corner_coords, image_fp)
            if gt_i < 0:
                continue
            dict_eval_corner_distance[gt_i] = dist
        
        for i in range(len(gt_corner_coords)):
            if i not in dict_eval_corner_distance.keys():
                current_data_dict[method_name].append(None)
            else:
                current_data_dict[method_name].append(dict_eval_corner_distance[i])
    df = pd.DataFrame.from_dict(current_data_dict)
    csv_fn = os.path.join(os.path.join(GT_FILEPATH, "results"), gt_fn)[:-4] + ".csv"
    print(df)
    print(df.dropna())
    df.to_csv(csv_fn, index=False)


# Generate a bunch of tables like this 
# |
# |
# V

# GOPRO_6x6_bla
#           method_1     method_2 
#corner1     ???%         ???%
#corner2     ???%         ???%
#corner3     ???
#corner4     ???