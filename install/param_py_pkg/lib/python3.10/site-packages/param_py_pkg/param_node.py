import rclpy
from rclpy.node import Node

class ParamNode(Node):
    def __init__(self):
        super().__init__('py_param_node')
        
        
        
        self.declare_parameter('frames.odom', 'default_odom')
        self.declare_parameter('frames.baselink', 'default_base_link')
        self.declare_parameter('frames.lidar', 'default_lidar')
        self.declare_parameter('frames.imu', 'default_imu')

        
        sim_time = self.get_parameter('use_sim_time').value
        odom = self.get_parameter('frames.odom').value
        baselink = self.get_parameter('frames.baselink').value
        lidar = self.get_parameter('frames.lidar').value
        imu = self.get_parameter('frames.imu').value

        
        self.get_logger().info('====== 成功读取 YAML 内容 ======')
        self.get_logger().info(f'use_sim_time: {sim_time}')
        self.get_logger().info(f'frames.odom: {odom}')
        self.get_logger().info(f'frames.baselink: {baselink}')
        self.get_logger().info(f'frames.lidar: {lidar}')
        self.get_logger().info(f'frames.imu: {imu}')
        self.get_logger().info('===============================')

def main(args=None):
    rclpy.init(args=args)
    node = ParamNode()
    rclpy.spin_once(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
