#! /usr/bin/env python

import rospy
from visualization_msgs.msg import Marker
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "CO2: ", data.data)
    print(data.data)


def listener():
    rospy.init_node("rviz_marker")

    rospy.Subscriber("co2data", String, callback)
    rospy.spin()

def concentration2color(data):
    print(data.data)


if __name__ == '__main__':
    listener()

