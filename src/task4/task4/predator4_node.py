import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
import math
import time

class Predator4Node(Node):
    def __init__(self):
        super().__init__('predator_node')
        self.pose = None 
        self.prey_pose = None
        self.last_prey_pose = None
        self.other_p1 = Pose()
        self.other_p2 = Pose()
        
        self.start_time = time.time()
        self.caught = False

        node_name = self.get_name()
        self.pub = self.create_publisher(Twist, f'/{node_name}/cmd_vel', 10)
        self.sub_self = self.create_subscription(Pose, f'/{node_name}/pose', self.self_cb, 10)
        self.sub_prey = self.create_subscription(Pose, '/prey/pose', self.prey_cb, 10)

        all_preds = ['predator1', 'predator2', 'predator3']
        others = [p for p in all_preds if p != node_name]
        self.create_subscription(Pose, f'/{others[0]}/pose', self.other1_cb, 10)
        self.create_subscription(Pose, f'/{others[1]}/pose', self.other2_cb, 10)

        self.pen_client = self.create_client(SetPen, f'/{node_name}/set_pen')
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.init_pen()

    def init_pen(self):
        if self.pen_client.wait_for_service(timeout_sec=1.0):
            self.pen_client.call_async(SetPen.Request(r=255, g=0, b=0, width=2, off=0))

    def prey_cb(self, msg):
        self.last_prey_pose = self.prey_pose
        self.prey_pose = msg

    def self_cb(self, msg): self.pose = msg
    def other1_cb(self, msg): self.other_p1 = msg
    def other2_cb(self, msg): self.other_p2 = msg

    def timer_callback(self):
        if self.pose is None or self.prey_pose is None:
            return

        if (time.time() - self.start_time) > 60.0 or self.caught:
            self.pub.publish(Twist())
            return

        lead_time = 0.4
        target_x = self.prey_pose.x + (
            self.prey_pose.linear_velocity * math.cos(self.prey_pose.theta) * lead_time
        )
        target_y = self.prey_pose.y + (
            self.prey_pose.linear_velocity * math.sin(self.prey_pose.theta) * lead_time
        )

        dx = target_x - self.pose.x
        dy = target_y - self.pose.y

        for other in [self.other_p1, self.other_p2]:
            dist_to_other = math.hypot(self.pose.x - other.x, self.pose.y - other.y)
            if 0 < dist_to_other < 1.0:
                dx -= (other.x - self.pose.x) * 0.5
                dy -= (other.y - self.pose.y) * 0.5

        dist_to_actual = math.hypot(
            self.prey_pose.x - self.pose.x,
            self.prey_pose.y - self.pose.y
        )

        move = Twist()
        if dist_to_actual < 0.5:
            self.caught = True
        else:
            target_angle = math.atan2(dy, dx)
            diff = target_angle - self.pose.theta
            while diff > math.pi:
                diff -= 2 * math.pi
            while diff < -math.pi:
                diff += 2 * math.pi
            
            move.linear.x = 1.5
            move.angular.z = 6.0 * diff
        
        self.pub.publish(move)

def main(args=None):
    rclpy.init(args=args)
    node = Predator4Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
