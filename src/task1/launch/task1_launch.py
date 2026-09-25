from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.actions import TimerAction

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim'
        ),

        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/kill', 'turtlesim/srv/Kill', '{name: "turtle1"}'],
            output='screen'
        ),

        TimerAction(
            period=1.0,
            actions=[
                ExecuteProcess(
                    cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', '{x: 10.0, y: 10.0, theta: 0.0, name: "prey"}'],
                    output='screen'
                ),
                ExecuteProcess(
                    cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', '{x: 1.0, y: 1.0, theta: 0.0, name: "predator"}'],
                    output='screen'
                ),
            ]
        ),

        TimerAction(
            period=2.0,
            actions=[
                Node(
                    package='task1',
                    executable='prey_node',
                    name='prey_node'
                ),
                Node(
                    package='task1',
                    executable='predator_node',
                    name='predator_node'
                ),
            ]
        ),
    ])

