import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from geometry_msgs.msg import Twist
import math
import time

class Prey2Node(Node):
    def __init__(self):
        super().__init__('prey2')
        self.pose = Pose()
        self.predator_pose = Pose()
        self.start_time = time.time()
        self.captured = False

        self.pub = self.create_publisher(Twist, '/prey2/cmd_vel', 10)
        self.sub_predator = self.create_subscription(Pose, '/predator2/pose', self.predator_callback, 10)
        self.sub_self = self.create_subscription(Pose, '/prey2/pose', self.self_callback, 10)

        self.set_pen_color(0, 255, 0)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def set_pen_color(self, r, g, b):
        client = self.create_client(SetPen, '/prey2/set_pen')
        while not client.wait_for_service(timeout_sec=1.0):
            pass
        req = SetPen.Request()
        req.r, req.g, req.b = r, g, b
        req.width = 2
        client.call_async(req)

    def predator_callback(self, msg):
        self.predator_pose = msg

    def self_callback(self, msg):
        self.pose = msg

    def timer_callback(self):
        # Calculate distance to see if caught
        dist = math.hypot(self.pose.x - self.predator_pose.x, self.pose.y - self.predator_pose.y)
        
        if (time.time() - self.start_time) > 60.0 or dist < 0.5:
            self.pub.publish(Twist())
            return

        move = Twist()
        margin = 1.5
        
        if self.pose.x < margin or self.pose.x > (11.0 - margin) or \
           self.pose.y < margin or self.pose.y > (11.0 - margin):
            target_angle = math.atan2(5.5 - self.pose.y, 5.5 - self.pose.x)
        else:
            target_angle = math.atan2(self.pose.y - self.predator_pose.y, 
                                      self.pose.x - self.predator_pose.x)

        angle_diff = target_angle - self.pose.theta
        while angle_diff > math.pi: angle_diff -= 2 * math.pi
        while angle_diff < -math.pi: angle_diff += 2 * math.pi

        move.linear.x = 1.5
        move.angular.z = 5.0 * angle_diff
        self.pub.publish(move)

def main(args=None):
    rclpy.init(args=args)
    node = Prey2Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
