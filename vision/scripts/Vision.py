#!/usr/bin/env python
from pathlib import Path
import sys
import os
import rospy as ros
import numpy as np
import cv2 as cv
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import sensor_msgs.point_cloud2 as point_cloud2
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Int32
from motion.msg import pos
from LegoDetect import LegoDetect

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
IMG = os.path.abspath(os.path.join(ROOT, "detect.png"))

w_R_c = np.matrix([[0, -0.499, 0.866], [-1, 0, 0], [0, -0.866, -0.499]])
x_c = np.array([-0.9, 0.24, -0.35])
base_offset = np.array([0.5, 0.35, 1.75])

# -----------------------------------------------------------------------------------------

class Vision:

    def __init__(self):

        ros.init_node('vision', anonymous=True)

        self.lego_list = []
        self.bridge = CvBridge()

        # Flags
        self.allow_receive_image = True
        self.allow_receive_pointcloud = False
        self.vision_ready = 0

        self.pos_pub = ros.Publisher("/vision/pos", pos, queue_size=1)
        self.ack_sub = ros.Subscriber('/vision/ack', Int32, self.ackCallbak)
        self.image_sub = ros.Subscriber("/ur5/zed_node/left_raw/image_raw_color", Image, self.receive_image)
        self.sub_pointcloud = ros.Subscriber("/ur5/zed_node/point_cloud/cloud_registered", PointCloud2, self.receive_pointcloud, queue_size=1)
        self.ack_pub = ros.Publisher('/taskManager/stop', Int32, queue_size=1)
        
    def receive_image(self, data):

        # Flag
        if not self.allow_receive_image:
            return
        self.allow_receive_image = False

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        cv.imwrite(IMG, cv_image)
        legoDetect = LegoDetect()
        legoDetect.detect(IMG)
        self.lego_list = legoDetect.lego_list

        self.allow_receive_pointcloud = True

    def receive_pointcloud(self, msg):

        # Flag
        if not self.allow_receive_pointcloud:
            return
        self.allow_receive_pointcloud = False
        
        self.pos_msg_list = []

        for lego in self.lego_list:

            # Get point cloud
            for data in point_cloud2.read_points(msg, field_names=['x','y','z'], skip_nans=True, uvs=[lego.center_point]):
                lego.point_cloud = (data[0], data[1], data[2])

            # Transform point cloud to world
            lego.point_world = w_R_c.dot(lego.point_cloud) + x_c + base_offset

            # Show details
            lego.show()

            # Create msg for pos_pub
            pos_msg = pos()
            pos_msg.class_id = 1
            pos_msg.x = lego.point_world[0, 0]
            pos_msg.y = lego.point_world[0, 1]
            pos_msg.z = lego.point_world[0, 2]
            pos_msg.pitch = 0
            pos_msg.roll = 0
            pos_msg.yaw = 0
            self.pos_msg_list.append(pos_msg)
            
        print('DONE DETECTING LEGO! VISION READY!')
        self.vision_ready = 1
        self.send_pos_msg()

    def ackCallbak(self, ack_ready):
        
        if self.vision_ready == 1 and ack_ready.data == 1:
            self.send_pos_msg()
            
    def send_pos_msg(self):
        try:
            pos_msg = self.pos_msg_list.pop()
            self.pos_pub.publish(pos_msg)
            print('Position published:\n', pos_msg)
        except IndexError:
            print('FINISH ALL LEGO')
            
            

# -----------------------------------------------------------------------------------------
        
if __name__ == '__main__':

    vision = Vision()

    try:
        ros.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        if os.path.exists(IMG):
            os.remove(IMG)
    