from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/kill', 'turtlesim/srv/Kill', '{name: "turtle1"}'],
            output='screen'
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='ros2'
        ),
        Node(
            package='task2',
            executable='predator2_node',
            name='predator2'
        ),
        Node(
            package='task2',
            executable='prey2_node',
            name='prey2'
        ),
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', '{x: 1.0, y: 1.0, theta: 0.0, name: "predator2"}'],
            output='screen'
        ),
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', '{x: 10.0, y: 10.0, theta: 0.0, name: "prey2"}'],
            output='screen'
        ),
    ])

