import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node

def generate_launch_description():
    turtlebot3_world_launch = os.path.join(
        get_package_share_directory('turtlebot3_gazebo'),
        'launch',
        'turtlebot3_world.launch.py'
    )

    # Use localization_launch.py or navigation_launch.py — both exist
    nav2_localization_launch = os.path.join(
        get_package_share_directory('nav2_bringup'),
        'launch',
        'localization_launch.py'
    )

    map_file = '/home/sanjay/ros2_workspaces/nav_turtlebot/src/slam_pkg/maps/slam_map.yaml'

    return LaunchDescription([
        # Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(turtlebot3_world_launch)
        ),

        # Navigation2 Localization
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(nav2_localization_launch),
            launch_arguments={
                'map': map_file,
                'use_sim_time': 'true'
            }.items()
        ),

        # RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2_node',
            output='screen',
            parameters=[{'use_sim_time': True}]
        )
    ])
