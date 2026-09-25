import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from geometry_msgs.msg import Twist
import math
import time

class Predator2Node(Node):
    def __init__(self):
        super().__init__('predator2')
        self.pose = Pose()
        self.prey_pose = Pose()
        self.start_time = time.time()
        self.caught = False

        self.pub = self.create_publisher(Twist, '/predator2/cmd_vel', 10)
        self.sub_prey = self.create_subscription(Pose, '/prey2/pose', self.prey_callback, 10)
        self.sub_self = self.create_subscription(Pose, '/predator2/pose', self.self_callback, 10)

        # Call service to set pen colour to Red
        self.set_pen_color(255, 0, 0)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def set_pen_color(self, r, g, b):
        client = self.create_client(SetPen, '/predator2/set_pen')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for set_pen service...')
        req = SetPen.Request()
        req.r, req.g, req.b = r, g, b
        req.width = 3
        req.off = 0
        client.call_async(req)

    def prey_callback(self, msg):
        self.prey_pose = msg

    def self_callback(self, msg):
        self.pose = msg

    def timer_callback(self):
        if (time.time() - self.start_time) > 60.0 or self.caught:
            self.pub.publish(Twist())
            return

        dx = self.prey_pose.x - self.pose.x
        dy = self.prey_pose.y - self.pose.y
        distance = math.hypot(dx, dy)

        move = Twist()
        if distance < 0.5:
            self.get_logger().info('Prey caught!')
            self.caught = True
            move.linear.x = 0.0
            move.angular.z = 0.0
        else:
            target_angle = math.atan2(dy, dx)
            angle_diff = target_angle - self.pose.theta
            while angle_diff > math.pi: angle_diff -= 2 * math.pi
            while angle_diff < -math.pi: angle_diff += 2 * math.pi

            move.linear.x = 1.5
            move.angular.z = 6.0 * angle_diff

        self.pub.publish(move)

def main(args=None):
    rclpy.init(args=args)
    node = Predator2Node()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
