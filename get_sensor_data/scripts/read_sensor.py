#!/usr/bin/env python
# Collect data from sensor and publish
import rospy
from std_msgs.msg import String
import mh_z19


def collectData():
    pub = rospy.Publisher('co2data', String, queue_size=10)
    rospy.init_node('collectData', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        data = str(mh_z19.read())
        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()


if __name__ == '__main__':
    try:
        collectData()
    except rospy.ROSInterruptException:
        pass
