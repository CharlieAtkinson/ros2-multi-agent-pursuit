import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction
import random

def generate_launch_description():
    turtlesim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='sim'
    )

    kill_turtle1 = ExecuteProcess(
        cmd=['ros2', 'service', 'call', '/kill', 'turtlesim/srv/Kill', "{name: 'turtle1'}"],
        output='screen'
    )

    turtles = ['predator1', 'predator2', 'predator3', 'prey']
    spawn_commands = []
    
    # We add a tiny delay between each individual spawn to help turtlesim keep up
    for i, name in enumerate(turtles):
        x, y = random.uniform(1.5, 9.5), random.uniform(1.5, 9.5)
        theta = random.uniform(0.0, 6.28)
        spawn_commands.append(
            TimerAction(
                period=float(i) * 0.5, # Stagger spawns by 0.5s
                actions=[ExecuteProcess(
                    cmd=['ros2', 'service', 'call', '/spawn', 'turtlesim/srv/Spawn', 
                         f"{{x: {x}, y: {y}, theta: {theta}, name: '{name}'}}"],
                    output='screen'
                )]
            )
        )

    predator_nodes = [
        Node(package='task4', executable='predator4_node', name=f'predator{i}') 
        for i in range(1, 4)
    ]

    prey_node = Node(package='task4', executable='prey4_node', name='prey')

    return LaunchDescription([
        turtlesim_node,
        TimerAction(period=1.0, actions=[kill_turtle1]),
        TimerAction(period=2.0, actions=spawn_commands),
        # Increase this to 6.0s to ensure all spawns are 100% finished
        TimerAction(period=6.0, actions=predator_nodes + [prey_node]),
    ])
