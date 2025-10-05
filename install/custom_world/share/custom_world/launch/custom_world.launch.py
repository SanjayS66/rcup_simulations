from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    world_file = '/home/sanjay/Desktop/gazebo_custom_map/rcup_custom_arena_fixed_table.world'

    gzserver = ExecuteProcess(
        cmd=['gzserver', '--verbose', world_file, '-slibgazebo_ros_init.so', '-slibgazebo_ros_factory.so'],
        output='screen'
    )

    gzclient = ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )

    spawn_bot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'burger',
            '-file', '/opt/ros/humble/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf',
            '-x', '0', '-y', '0', '-z', '0.01'
        ],
        output='screen'
    )

    return LaunchDescription([gzserver, gzclient, spawn_bot])
