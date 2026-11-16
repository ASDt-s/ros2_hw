import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3Stamped
import serial
import math

class GimbalController(Node):
    def __init__(self):
        super().__init__('gimbal_controller')
       
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
        
        self.sub_imu = self.create_subscription(Imu, '/mavros/imu/data', self.imu_cb, 10)
        self.sub_target = self.create_subscription(Vector3Stamped, '/tracker/target_predicted', self.target_cb, 10)
        
        self.roll, self.pitch = 0.0, 0.0
        self.tx, self.ty = 0.0, 0.0

    def imu_cb(self, msg):
        q = msg.orientation
        sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
        cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
        self.roll = math.atan2(sinr_cosp, cosr_cosp) * 180 / math.pi
        
        sinp = 2 * (q.w * q.y - q.z * q.x)
        self.pitch = math.asin(max(-1, min(1, sinp))) * 180 / math.pi

    def target_cb(self, msg):
        self.tx, self.ty = msg.vector.x, msg.vector.y
        
       
        stabilize_pan = 90 - self.roll
        stabilize_tilt = 90 - self.pitch
        
     
        track_pan = self.tx * 20
        track_tilt = self.ty * 20
        
       
        final_pan = max(0, min(180, stabilize_pan + track_pan))
        final_tilt = max(0, min(180, stabilize_tilt + track_tilt))
        
      
        self.ser.write(f"{final_pan:.1f},{final_tilt:.1f}\n".encode())
