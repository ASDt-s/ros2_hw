import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(get_package_share_directory('param_py_pkg'), 'config', 'params.yaml')
    return LaunchDescription([
        Node(
            package='param_py_pkg',
            executable='param_node',
            name='py_param_node',
            parameters=[
                config,
                {'frames.lidar': 'Lidar_From_Launch'}  
            ],
            output='screen'
        )
    ])
