#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64
import numpy as np
import control

mass_cart = 20.0
mass_pole = 2.0
length_pole = 0.5
g = 9.81

A = np.matrix([[0,1,0,0],
               [0, 0, mass_pole*g/mass_cart, 0],
               [0, 0, 0, 1],
               [0, 0, (1 + mass_pole/mass_cart)*g/length_pole, 0]
               ])
B = np.matrix([ [0],
                [1/mass_cart],
                [0],
                [1/mass_cart/length_pole]
                ])
C = np.matrix([[1,0,0,0], [0,0,1,0]])

Q = np.diag([1, 1, 1, 1])
R = np.diag([0.1])

K, S, E = control.lqr(A, B, Q, R)

class Cartpolesystem:
    def __init__(self):
        self.current_state = np.array([0.0, 0.0, 0.0, 0.0])
        self.desired_state = np.array([0., 0., 0., 0.])
        #self.desired_state = np.matrix([[0],[0],[0],[0]])
        self.cmd_msg = Float64()
        self.sub_state = rospy.Subscriber("/invpend/joint_states", JointState, self.pose_callback)
        self.pub_vel = rospy.Publisher("/invpend/joint1_velocity_controller/command", Float64, queue_size=10)
    
    def pose_callback(self, data):
        self.current_state[0] = data.position[1]
        self.current_state[1] = data.velocity[1]
        self.current_state[2] = data.position[0]
        self.current_state[3] = data.velocity[0]
    
    def control(self):
        rate = rospy.Rate(50)
        while not rospy.is_shutdown():
            self.cmd_msg.data = np.matmul(K, (self.desired_state-self.current_state))
            self.pub_vel.publish(self.cmd_msg)
            rate.sleep()
    

if __name__ == '__main__':
    rospy.init_node('CartpoleLQR', anonymous=True)
    lqr = Cartpolesystem()
    lqr.control()
    rospy.spin()