import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Vector3Stamped
import cv2
import numpy as np

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.publisher_ = self.create_publisher(Vector3Stamped, '/vision/target_raw', 10)
        self.cap = cv2.VideoCapture(0)
        self.timer = self.create_timer(0.033, self.timer_callback) # 30fps
        
        # 内参
        self.FOCAL_LENGTH = 600 
        self.TARGET_REAL_WIDTH = 0.15 # 宽

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret: return
        
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255])) + \
               cv2.inRange(hsv, np.array([170, 120, 70]), np.array([180, 255, 255]))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        msg = Vector3Stamped()
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            if cv2.contourArea(c) > 500:
                M = cv2.moments(c)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    _, _, w, _ = cv2.boundingRect(c)
                    
                    
                    Z = (self.TARGET_REAL_WIDTH * self.FOCAL_LENGTH) / w
                   
                    X = ((cx - frame.shape[1]//2) / self.FOCAL_LENGTH) * Z
                    Y = ((cy - frame.shape[0]//2) / self.FOCAL_LENGTH) * Z
                    
                    msg.vector.x = float(X)
                    msg.vector.y = float(Y)
                    msg.vector.z = float(Z)
        
        self.publisher_.publish(msg)
        cv2.imshow("Vision", frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
