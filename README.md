# ROS2 SLAM and Autonomous Navigation Simulations

## 🔍 Overview

This workspace provides a complete solution for: 

1. **SLAM-based mapping** - Create maps of unknown environments using the TurtleBot3's LiDAR sensor
2. **Localization** - Use AMCL (Adaptive Monte Carlo Localization) to localize the robot on a known map
3. **Autonomous Navigation** - Navigate to goal poses using Nav2's global and local planning algorithms

The implementation supports: 
- **TurtleBot3 models**:  Burger, Waffle, Waffle Pi
- **Standard environments**: TurtleBot3 House World, TurtleBot3 World
- **Custom environments**: RoboCup@work arena simulation

---

## 📁 Repository Structure

```
rcup_simulations/
├── README.md
└── src/
    ├── slam_pkg/           # Main SLAM and Nav2 package
    │   ├── launch/         # Launch files for SLAM, localization, and navigation
    │   ├── config/         # Configuration files (YAML, RViz)
    │   ├── maps/           # Saved maps
    │   ├── src/            # Source files (C++)
    │   ├── CMakeLists.txt
    │   └── package.xml
    └── custom_world/       # Custom Gazebo world package
        ├── launch/         # Launch files for custom world
        ├── config/         # Configuration files for custom world
        ├── maps/           # Maps for custom world
        ├── setup.py
        └── package.xml
```
## 📦 Packages

### 1.slam_pkg

The primary package containing all necessary launch files for SLAM and autonomous navigation in the standard TurtleBot3 environments.

**Features:**
- SLAM mapping using `slam_toolbox`
- AMCL-based localization
- Nav2 autonomous navigation
- Pre-configured RViz configurations

**Launch Files:**
- `slam.launch. py` - Start SLAM mapping
- `localisation_amcl.launch.py` - Start localization with saved map
- `nav2.launch.py` - Full autonomous navigation stack

### 2.custom_world

A specialized package for running SLAM and Nav2 in a custom Gazebo world resembling the RoboCup@work arena. 

**Features:**
- Custom world loader
- Adapted SLAM parameters
- Custom map support

**Launch Files:**
- `slam. launch.py` - SLAM in custom world
- `nav2.launch.py` - Navigation in custom world
- `turtlebot3_customworld.launch.py` - Load custom Gazebo world


---
## 📚 Key Concepts

### SLAM Toolbox
- **Asynchronous SLAM**: Processes scans in a separate thread for better performance
- **Loop Closure**: Detects when the robot revisits known areas to correct drift
- **Pose Graph Optimization**: Uses graph-based optimization (Ceres solver) for map consistency

### AMCL (Adaptive Monte Carlo Localization)
- **Particle Filter**: Represents robot pose uncertainty with particles
- **Sensor Model**: Compares expected laser scans with actual scans
- **Motion Model**:  Predicts particle movement based on odometry

### Nav2 Stack
- **Global Planner**: Computes optimal path from start to goal
- **Local Planner**: Generates velocity commands to follow the path
- **Recovery Behaviors**: Handles stuck situations (rotate, back up, clear costmap)
- **Behavior Trees**: Coordinates navigation tasks and recovery

---

## 🏗️ Architecture

### SLAM Pipeline

```
┌─────────────┐      ┌──────────────┐      ┌────────────┐
│   Gazebo    │─────▶│ TurtleBot3   │─────▶│ LiDAR Scan │
│   World     │      │ /scan topic  │      │  /scan     │
└─────────────┘      └──────────────┘      └─────┬──────┘
                                                  │
                                                  ▼
                     ┌──────────────────────────────────┐
                     │   slam_toolbox                   │
                     │   (async_slam_toolbox_node)      │
                     │   - Scan matching                │
                     │   - Loop closure                 │
                     │   - Map building                 │
                     └─────────────┬────────────────────┘
                                   │
                                   ▼
                          ┌────────────────┐
                          │  /map topic    │
                          │  Occupancy Grid│
                          └────────────────┘
```

### Navigation Pipeline

```
┌──────────────┐      ┌─────────────┐      ┌──────────────┐
│  Map Server  │─────▶│    AMCL     │─────▶│  Localized   │
│ (saved map)  │      │ (particles) │      │  Robot Pose  │
└──────────────┘      └─────────────┘      └──────┬───────┘
                                                   │
                                                   ▼
┌──────────────┐                          ┌────────────────┐
│  Goal Pose   │────────────────────────▶ │  Nav2 Stack    │
│ (from RViz)  │                          │  - Planner     │
└──────────────┘                          │  - Controller  │
                                          │  - Recovery    │
                                          └────────┬───────┘
                                                   │
                                                   ▼
                                          ┌────────────────┐
                                          │  cmd_vel       │
                                          │  (velocity     │
                                          │   commands)    │
                                          └────────────────┘
```

---



## 🔧 Prerequisites

### System Requirements
- **OS**: Ubuntu 22.04 (Jammy)
- **ROS2 Distribution**: Humble Hawksbill (recommended)

### Required Packages

```bash
# ROS2 Humble
sudo apt update
sudo apt install ros-humble-desktop

# TurtleBot3 packages
sudo apt install ros-humble-turtlebot3*
sudo apt install ros-humble-turtlebot3-gazebo

# SLAM Toolbox
sudo apt install ros-humble-slam-toolbox

# Nav2 Stack
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup

# Additional dependencies
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-rviz2
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/SanjayS66/rcup_simulations.git
```

### 2. Set TurtleBot3 Model

Add to your `~/.bashrc`:

```bash
export TURTLEBOT3_MODEL=burger  # or 'waffle', 'waffle_pi'
```

Then source:

```bash
source ~/.bashrc
```

### 3. Build the Workspace

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

---

## 🎮 Usage

### SLAM (Mapping)

#### Standard World (TurtleBot3 House)

```bash
# Terminal 1: Launch SLAM
ros2 launch slam_pkg slam.launch.py
```

This will:
- Start Gazebo with TurtleBot3 House world
- Launch `async_slam_toolbox_node` for mapping
- Open RViz2 with SLAM visualization

**Control the robot** using keyboard teleop: 

```bash
# Terminal 2: Teleoperation
ros2 run turtlebot3_teleop teleop_keyboard
```

**Save the map**:

```bash
# Terminal 3: Save map
ros2 run nav2_map_server map_saver_cli -f ~/maps/my_map
```

#### Custom World (RoboCup Arena)

```bash
ros2 launch custom_world slam.launch.py
```

### Localization

Launch localization with a previously saved map:

```bash
ros2 launch slam_pkg localisation_amcl.launch.py
```

**Set initial pose** in RViz: 
1. Click "2D Pose Estimate" in RViz toolbar
2. Click and drag on the map to set robot's initial position and orientation

### Autonomous Navigation

#### Standard World

```bash
ros2 launch slam_pkg nav2.launch.py
```

#### Custom World

```bash
ros2 launch custom_world nav2.launch.py
```

**Send navigation goals**: 
1. Set the Initial Pose
2. In RViz, click "Nav2 Goal" or "2D Goal Pose"
3. Click on the map where you want the robot to navigate
4. The robot will plan and execute a path to the goal

---
