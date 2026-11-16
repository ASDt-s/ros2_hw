import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3Stamped
import numpy as np
from filterpy.kalman import KalmanFilter

class StateEstimator(Node):
    def __init__(self):
        super().__init__('state_estimator')
        self.sub = self.create_subscription(Vector3Stamped, '/vision/target_raw', self.vision_cb, 10)
        self.pub = self.create_publisher(Vector3Stamped, '/tracker/target_predicted', 10)
        
        
        self.kf = KalmanFilter(dim_x=6, dim_z=3)
        dt = 0.033
        self.kf.F = np.array([[1,0,0, dt,0,0], [0,1,0, 0,dt,0], [0,0,1, 0,0,dt],
                              [0,0,0, 1,0,0],  [0,0,0, 0,1,0],  [0,0,0, 0,0,1]])
        self.kf.H = np.array([[1,0,0, 0,0,0], [0,1,0, 0,0,0], [0,0,1, 0,0,0]])
        self.kf.R *= 0.1
        self.kf.Q *= 0.01
        self.kf.x = np.array([0,0,1.5, 0,0,0])

    def vision_cb(self, msg):
        z = np.array([msg.vector.x, msg.vector.y, msg.vector.z])
        self.kf.predict()
        self.kf.update(z)
        
        out = Vector3Stamped()
        out.vector.x = self.kf.x[0] 
        out.vector.y = self.kf.x[1] 
        out.vector.z = self.kf.x[2] 
        self.pub.publish(out)
