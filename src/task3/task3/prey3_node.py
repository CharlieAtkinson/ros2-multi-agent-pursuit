import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
import math
import time

class Prey4Node(Node):
    def __init__(self):
        super().__init__('prey')
        self.pose = None
        self.p1, self.p2, self.p3 = Pose(), Pose(), Pose()
        self.start_time = time.time()

        self.create_subscription(Pose, '/predator1/pose', self.p1_cb, 10)
        self.create_subscription(Pose, '/predator2/pose', self.p2_cb, 10)
        self.create_subscription(Pose, '/predator3/pose', self.p3_cb, 10)
        self.create_subscription(Pose, '/prey/pose', self.self_cb, 10)
        
        self.pub = self.create_publisher(Twist, '/prey/cmd_vel', 10)
        self.pen_client = self.create_client(SetPen, '/prey/set_pen')
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.init_pen()

    def init_pen(self):
        if self.pen_client.wait_for_service(timeout_sec=1.0):
            self.pen_client.call_async(SetPen.Request(r=0, g=255, b=0, width=2, off=0))

    def p1_cb(self, msg): self.p1 = msg
    def p2_cb(self, msg): self.p2 = msg
    def p3_cb(self, msg): self.p3 = msg
    def self_cb(self, msg): self.pose = msg

    def timer_callback(self):
        if self.pose is None:
            return
        if (time.time() - self.start_time) > 60.0:
            self.pub.publish(Twist())
            return

        dists = [math.hypot(self.pose.x - p.x, self.pose.y - p.y) for p in [self.p1, self.p2, self.p3]]
        min_dist = min(dists)
        
        if min_dist < 0.5:
            self.pub.publish(Twist())
            return

        threat = [self.p1, self.p2, self.p3][dists.index(min_dist)]

        look_ahead_dist = 2.0
        future_x = self.pose.x + look_ahead_dist * math.cos(self.pose.theta)
        future_y = self.pose.y + look_ahead_dist * math.sin(self.pose.theta)

        margin = 1.0
        hitting_wall = (
            future_x < margin or future_x > 11.0 - margin or
            future_y < margin or future_y > 11.0 - margin
        )

        if hitting_wall:
            target_angle = math.atan2(5.5 - self.pose.y, 5.5 - self.pose.x)
        else:
            target_angle = math.atan2(self.pose.y - threat.y, self.pose.x - threat.x)

        diff = target_angle - self.pose.theta
        while diff > math.pi:
            diff -= 2 * math.pi
        while diff < -math.pi:
            diff += 2 * math.pi

        move = Twist()
        move.linear.x = 2.0
        move.angular.z = 6.0 * diff
        self.pub.publish(move)

def main(args=None):
    rclpy.init(args=args)
    node = Prey4Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

