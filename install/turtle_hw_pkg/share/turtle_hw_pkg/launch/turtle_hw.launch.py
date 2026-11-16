import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('turtle_hw_pkg'),
        'config',
        'turtle_params.yaml'
    )

    return LaunchDescription([
        
        Node(package='turtlesim', executable='turtlesim_node', name='turtlesim'),
        
        
        Node(
            package='turtle_hw_pkg',
            executable='controller',
            name='my_controller',
            parameters=[config]
        ),

        
        Node(
            package='turtle_hw_pkg',
            executable='teleop',
            name='my_teleop',
            prefix='xterm -e'
        )
    ])
