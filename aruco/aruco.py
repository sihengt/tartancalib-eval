import cv2
import glob
import os
import numpy as np
import pickle

# Uses ArUco detector to count corners. Includes flag for visualization.

def count_corners(image, viz=False):
	# arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_APRILTAG_36h11)
	arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)

	arucoParams = cv2.aruco.DetectorParameters_create()
	arucoParams.markerBorderBits = 2
	# arucoParams.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
	# arucoParams.cornerRefinementWinSize = 2
	arucoParams.adaptiveThreshWinSizeStep = 1

	total_corners = 0
	all_corners = []
	(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
		parameters=arucoParams)
	if viz:
		# verify *at least* one ArUco marker was detected
		viz_corners = corners
		if len(viz_corners) > 0:
			# flatten the ArUco IDs list
			ids = ids.flatten()
			# loop over the detected ArUCo corners
			for (markerCorner, markerID) in zip(viz_corners, ids):
				# extract the marker corners (which are always returned in
				# top-left, top-right, bottom-right, and bottom-left order)
				viz_corners = markerCorner.reshape((4, 2))
				(topLeft, topRight, bottomRight, bottomLeft) = viz_corners
				# convert each of the (x, y)-coordinate pairs to integers
				topRight = (int(topRight[0]), int(topRight[1]))
				bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
				bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
				topLeft = (int(topLeft[0]), int(topLeft[1]))

				# draw the bounding box of the ArUCo detection
				cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
				cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
				cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
				cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
				# compute and draw the center (x, y)-coordinates of the ArUco
				# marker
				cX = int((topLeft[0] + bottomRight[0]) / 2.0)
				cY = int((topLeft[1] + bottomRight[1]) / 2.0)
				cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
				# draw the ArUco marker ID on the image
				cv2.putText(image, str(markerID),
					(topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
					0.5, (0, 255, 0), 2)
				print("[INFO] ArUco marker ID: {}".format(markerID))
				# show the output image
			
			for rejectCorner in rejected:
				reject_corners = rejectCorner.reshape((4, 2))
				(topLeft, topRight, bottomRight, bottomLeft) = reject_corners
				topRight = (int(topRight[0]), int(topRight[1]))
				bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
				bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
				topLeft = (int(topLeft[0]), int(topLeft[1]))

				# draw the bounding box of the ArUCo detection
				cv2.line(image, topLeft, topRight, (255, 0, 0), 2)
				cv2.line(image, topRight, bottomRight, (255, 0, 0), 2)
				cv2.line(image, bottomRight, bottomLeft, (255, 0, 0), 2)
				cv2.line(image, bottomLeft, topLeft, (255, 0, 0), 2)

			cv2.imshow("Image", image)
			cv2.waitKey(0)

	if len(corners) > 0:
		for (markerCorner, markerID) in zip(corners, ids):
			# extract the marker corners (which are always returned in
			# top-left, top-right, bottom-right, and bottom-left order)
			current_corners = markerCorner.reshape((4, 2))
			
			for c in current_corners:
				all_corners.append(c)
			total_corners += len(current_corners)

	return all_corners, total_corners

def aruco_experiment(image_folder, result_folder, result_bag_name):
	# Setting up ArUco detector
	all_image_fp = glob.glob(os.path.join(image_folder,"*.jpg"))
	# Sorting by image #
	all_image_fp.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

	l_image_corner = []
	all_corners = []
	frame_n = 0
	n_corners = 0
	for image_fp in all_image_fp:
		frame_corners = []
		image = cv2.imread(image_fp)
		if not image is None:
			corners, current_n_corners = count_corners(image, viz=False)
			for c in corners:
				frame_corners.append([frame_n, c[0], c[1]])
				n_corners += 1
			l_image_corner.append(current_n_corners)
			print("Image = {}\tCorners detected={}".format(image_fp, n_corners))
		else:
			print("{} is not an image.".format(image_fp))
		all_corners.append(frame_corners)
		frame_n += 1
	
	# Take the list of image corners and write it.
	if not os.path.isdir(result_folder):
		os.makedirs(result_folder)
	np_fp = os.path.join(result_folder, "aruco-" + result_bag_name + ".npy")
	txt_fp = os.path.join(result_folder, "aruco-" + result_bag_name + ".txt")
	with open(np_fp, 'wb') as f:
		pickle.dump(all_corners, f)

	f = open(txt_fp, "w")
	# print(l_image_corner)
	f.write("total:{}\n".format(sum(l_image_corner)))
	f.write("frame_n,corners\n")
	for i, frame_corners in enumerate(l_image_corner):
		f.write("{},{}".format(i,str(frame_corners)+"\n"))
	f.close()

	return n_corners