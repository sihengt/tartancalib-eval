import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


def rosbag_to_jpg(bag_file, output_dir, image_topic):
    status = False # To track status of conversion.
    print(
        "[rosbag_to_jpg] Extracting images from {} on topic {} into {}".format(
            bag_file,
            image_topic,
            output_dir
        )
    )

    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    assert (os.path.isdir(output_dir))

    bag = rosbag.Bag(bag_file, "r")
    bridge = CvBridge()
    count = 0
    for _topic, msg, _ts in bag.read_messages(topics=[image_topic]):
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="mono8")

        cv2.imwrite(os.path.join(output_dir,
                    "frame%06i.jpg" % count), cv_img)
        print("Wrote image %i" % count)
        count += 1

    bag.close()

    if (count > 0):
        status = True
    return status