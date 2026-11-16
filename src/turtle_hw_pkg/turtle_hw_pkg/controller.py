import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from example_interfaces.srv import SetInt64

class TurtleController(Node):
    def __init__(self):
        super().__init__('my_controller')
        
        
        self.declare_parameter('linear_speed', 2.0)
        self.declare_parameter('angular_speed', 1.5)
        self.lin_speed = self.get_parameter('linear_speed').value
        self.ang_speed = self.get_parameter('angular_speed').value

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        
        self.srv = self.create_service(SetInt64, 'set_mode', self.set_mode_callback)

        self.current_pose = None
        self.mode = 0 
        self.get_logger().info('Controller started. Default mode: 0')

    def set_mode_callback(self, request, response):
        self.mode = request.data
        self.get_logger().info(f'Switched to mode: {self.mode}')
        return response

    def pose_callback(self, msg):
        self.current_pose = msg
        self.move_turtle()

    def move_turtle(self):
        if self.current_pose is None:
            return

        cmd = Twist()
        x = self.current_pose.x
        y = self.current_pose.y
        current_time = self.get_clock().now().nanoseconds / 1e9

        if self.mode == 0:
            
            if x > 10.0 or x < 1.0 or y > 10.0 or y < 1.0:
                cmd.linear.x = 0.0
                cmd.angular.z = self.ang_speed
            else:
                cmd.linear.x = self.lin_speed
                cmd.angular.z = 0.0
        elif self.mode == 1:
            
            cmd.linear.x = self.lin_speed
            cmd.angular.z = self.ang_speed * math.sin(current_time * 2.0)
        elif self.mode == 2:
           
            cmd.linear.x = self.lin_speed
            if int(current_time) % 2 == 0:
                cmd.angular.z = self.ang_speed
            else:
                cmd.angular.z = -self.ang_speed

        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
