import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PreyNode(Node):
    def __init__(self):
        super().__init__('prey_node')
        self.publisher_ = self.create_publisher(Pose, 'prey_location', 10)
        
        self.pose = Pose()
        self.pose.x = 10.0
        self.pose.y = 10.0
        
        self.timer = self.create_timer(0.1, self.publish_pose)
        self.get_logger().info("Prey Node started, publishing location...")

    def publish_pose(self):
        self.publisher_.publish(self.pose)

def main(args=None):
    rclpy.init(args=args)
    node = PreyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()
