import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    config = os.path.join(get_package_share_directory('param_cpp_pkg'), 'config', 'params.yaml')
    return LaunchDescription([
        Node(
            package='param_cpp_pkg',
            executable='param_node',
            name='cpp_param_node',  # 必须和 YAML 第一行对应
            parameters=[config],
            output='screen'
        )
    ])
