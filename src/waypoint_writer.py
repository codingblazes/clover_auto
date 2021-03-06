#!/usr/bin/env python
import rospy
# import roslib; roslib.load_manifest('clover_auto')
import serial
from sensor_msgs.msg import NavSatFix
from std_srvs.srv import Trigger, TriggerResponse


class WaypointWriter():
    WAYPOINT_FILE = '/home/nvidia/waypoints.txt'
    PATH = '/dev/ttyUSB2'

    def __init__(self):
        self.sub = rospy.Subscriber('fix', NavSatFix, self.fix_callback)
        self.serv =  rospy.Service('record', Trigger, self.record_callback)
        self.ser = serial.Serial(self.PATH, 115200)

    def fix_callback(self, fix):
        self.fix = fix

    def record_callback(self, req):
        with open(self.WAYPOINT_FILE, 'a') as f:
            f.write(self.get_data_string())
        trigger = TriggerResponse()
        trigger.success = True
        return trigger

    def get_data_string(self):
        serial_line = self.ser.readline()
        theta = float(serial_line.split(':')[1])
        return '{},{},{}\n'.format(self.fix.latitude, 
                                   self.fix.longitude, theta)


def main():
    rospy.init_node('waypoint_writer', anonymous=False)
    ww = WaypointWriter()
    try:
        rospy.spin()
    except rospy.ROSInterruptException, KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

