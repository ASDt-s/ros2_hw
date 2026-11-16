import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from example_interfaces.srv import SetInt64
import sys
import termios
import tty
import select

MSG = """
--- Custom Teleop ---
Control Movement:
   w
 a   s   d

Switch Modes:
 0 : Auto Avoid
 1 : Sine Wave
 2 : Square Wave

CTRL-C to quit
"""

class MyTeleop(Node):
    def __init__(self):
        super().__init__('my_teleop')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.client = self.create_client(SetInt64, 'set_mode')
        self.speed = 2.0
        self.turn = 2.0

    def send_velocity(self, lin, ang):
        msg = Twist()
        msg.linear.x = lin
        msg.angular.z = ang
        self.publisher_.publish(msg)

    def send_mode(self, mode_num):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /set_mode service...')
        req = SetInt64.Request()
        req.data = mode_num
        self.client.call_async(req)

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    node = MyTeleop()
    print(MSG)
    
    try:
        while rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0)
            key = get_key(settings)
            if key == 'w': node.send_velocity(node.speed, 0.0)
            elif key == 's': node.send_velocity(-node.speed, 0.0)
            elif key == 'a': node.send_velocity(0.0, node.turn)
            elif key == 'd': node.send_velocity(0.0, -node.turn)
            elif key == '0': node.send_mode(0)
            elif key == '1': node.send_mode(1)
            elif key == '2': node.send_mode(2)
            elif key == '\x03': break # CTRL-C
    except Exception as e:
        print(e)
    finally:
        node.send_velocity(0.0, 0.0)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
