import subprocess
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os


def generate_launch_description():
    subprocess.run(["pkill", "-9", "gzserver"])
    subprocess.run(["pkill", "-9", "gzclient"])
    declared_arguments = []
    # ctrl_name = "vec_controller"
    # ctrl_name = "tau_controller"
    ctrl_name = "pos_controller"

    # General arguments
    ##########
    # gazebo #
    ##########
    xml = open('./src/gazebo_ros2_control_a_mini_demo/urdf/bot_test.urdf', 'r').read()


    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name='robot_state_publisher',
        output="both",
        parameters=[{
            "use_sim_time":True,
            "robot_description": xml,
            "publish_frequency": 50.0,
            "ignore_timestamp": False}],
    )
    # Launch arm controller
    start_arm_controller_cmd = Node(
      package="controller_manager",
      executable="spawner",
      arguments=[
        ctrl_name,
        "--controller-manager",
        "/controller_manager"
      ]
    )  

    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')
    # Start Gazebo server
    start_gazebo_server_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
      launch_arguments={'params_file': './src/gazebo_ros2_control_a_mini_demo/config/gazebo_param.yaml'}.items()
    )

  # Start Gazebo client    
    start_gazebo_client_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
      os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')),
    )

    # Launch joint state broadcaster
    start_joint_state_broadcaster_cmd = Node(
    package="controller_manager",
    executable="spawner",
    arguments=[
      "joint_state_broadcaster",
      "--controller-manager",
      "/controller_manager"
      ]
    )
    
    # Spawn the robot
    start_gazebo_ros_spawner_cmd = Node(
      package='gazebo_ros',
      executable='spawn_entity.py',
      arguments=[
      '-entity', 'bot_test',
      '-topic', "robot_description", 
      ],
      output='screen')  

    nodes_to_start = [
        start_arm_controller_cmd,
        start_gazebo_server_cmd,
        start_gazebo_client_cmd,
        start_joint_state_broadcaster_cmd,
        robot_state_publisher_node,
        start_gazebo_ros_spawner_cmd
    ]
    return LaunchDescription(nodes_to_start)

