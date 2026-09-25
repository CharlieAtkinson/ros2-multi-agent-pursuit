import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math

class PredatorNode(Node):
    def __init__(self):
        super().__init__('predator_node')
        self.prey_pose = None
        self.predator_pose = None
        self.create_subscription(Pose, 'prey_location', self.prey_callback, 10)
        self.create_subscription(Pose, '/predator/pose', self.predator_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/predator/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_toward_prey)
        self.get_logger().info("Predator Node started, searching for prey...")

    def prey_callback(self, msg):
        self.prey_pose = msg

    def predator_callback(self, msg):
        self.predator_pose = msg

    def move_toward_prey(self):
        if self.prey_pose is None or self.predator_pose is None:
            return

        dx = self.prey_pose.x - self.predator_pose.x
        dy = self.prey_pose.y - self.predator_pose.y
        distance = math.sqrt(dx**2 + dy**2)

        msg = Twist()

        if distance < 0.5:
            self.get_logger().info('Prey caught! Stopping.')
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_pub.publish(msg)
            return

        angle_to_prey = math.atan2(dy, dx)
        angle_error = angle_to_prey - self.predator_pose.theta

        if angle_error > math.pi:
            angle_error -= 2 * math.pi
        elif angle_error < -math.pi:
            angle_error += 2 * math.pi

        msg.linear.x = min(1.5 * distance, 2.0)
        msg.angular.z = 6.0 * angle_error

        self.cmd_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = PredatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

