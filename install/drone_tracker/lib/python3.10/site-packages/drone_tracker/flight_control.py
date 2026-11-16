import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3Stamped, TwistStamped
from sensor_msgs.msg import Imu
import math

class FlightController(Node):
    def __init__(self):
        super().__init__('flight_controller')
        self.sub_target = self.create_subscription(Vector3Stamped, '/tracker/target_predicted', self.target_cb, 10)
        self.sub_imu = self.create_subscription(Imu, '/mavros/imu/data', self.imu_cb, 10)
        
       
        self.pub_cmd = self.create_publisher(TwistStamped, '/mavros/setpoint_velocity/cmd_vel', 10)
        
        self.current_roll = 0.0
        self.current_pitch = 0.0

    def imu_cb(self, msg):
  
        q = msg.orientation
        sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
        cosr_cosp = 1 - 2 * (q.x * q.x + q.y * q.y)
        self.current_roll = math.atan2(sinr_cosp, cosr_cosp) * 180 / math.pi
        
        sinp = 2 * (q.w * q.y - q.z * q.x)
        self.current_pitch = math.asin(max(-1, min(1, sinp))) * 180 / math.pi

    def target_cb(self, msg):
    
        cmd = TwistStamped()
        cmd.twist.linear.y = msg.vector.x * 0.5   # 横
        cmd.twist.linear.z = msg.vector.y * 0.5   # 垂
        cmd.twist.linear.x = (msg.vector.z - 1.5) * 0.5 
        
       
        cmd.twist.linear.y = max(-1.0, min(1.0, cmd.twist.linear.y))
        cmd.twist.linear.z = max(-1.0, min(1.0, cmd.twist.linear.z))
        self.pub_cmd.publish(cmd)
