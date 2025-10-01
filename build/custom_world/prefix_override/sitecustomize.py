import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sanjay/ros2_workspaces/nav_turtlebot/install/custom_world'
