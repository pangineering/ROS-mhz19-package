#!/usr/bin/env python
import rospy
from std_msgs.msg import String


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "CO2: ", data.data)


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("co2data", String, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
