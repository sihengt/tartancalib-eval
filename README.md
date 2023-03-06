# TartanCalib Evaluation

This repository contains code for evaluating AprilTag detectors against the method proposed within TartanCalib.

## Usage instructions
1. Pull all submodules and build. You'll have to build (you may specify your numprocs behind -j):

```
git clone git@github.com:seeeheng/tartancalib-eval.git
git submodule init 
git submodule update
```

- kaess-apriltags
```
cd kaess-apriltags
mkdir build && cd build
cmake .. && make -j8
```
- apriltag
```
cd apriltag
mkdir build && cd build
cmake .. & make -j8
```
- deltille
```
cd deltille
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_APPS=ON && make -j8
```

2. Source ros
`source /opt/ros/noetic/setup.bash`

3. Run
``` python main.py -i /path/to/folder/with/rosbags -r /path/to/folder/to/save/results ```

| Flag                 | Explanation                                                                      |
|----------------------|----------------------------------------------------------------------------------|
| -i, --input_folder   | Folder containing input rosbags. Must be a folder with all .bag files to analyze |
| -r, --results_folder | Folder used to store results. Must exist before execution.                       |

Input folder must be a folder containing rosbags. E.g. 

```
/path/to/folder/with/rosbags
|__ cam1.bag
|__ cam2.bag
|__ cam3.bag
|__ cam4.bag
|__ cam5.bag
|__ itsokaytohaverandomfiles.txt
|__ willonlyprocessbags.txt
```

## Output

Output CSV will be found in results folder as `total_corners_detected.csv` in the following format:
```
	Deltille	AT3	    	Kaess-AT3	ArUco
cam1	7291	    	4908    	5896	    	2152
cam2    20055       	20      	592         	10191
cam3    830         	8202    	10          	8101
cam4	3001	    	2548		2996	    	2420
cam5    20          	50      	3033        	808
```

Output also includes `.pkl` files (pickled lists of lists) named in the following format `$detectiontype/$detectiontype-$bagname.npy`.
Each `.pkl` file contains a list of lists of shape (n_frames, n_corners_in_frame). For each frame, if no detections are detected, an empty list will be appended still.

Use the `.pkl` files in conjunction with your script if you'd like to generate corners vs. polar angle.
