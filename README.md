# gazebo_debug_demo
# USAGE
* ```mkdir -p test_ws/src```
* ```cd test_ws/src```
* ```git clone ```
* ```cd ..```
* ```colcon build --symlink-install```
* ```source install/setup.bash```
* ```ros2 launch gazebo_debug_demo run_gazebo.py```
* open a bash, and run: ```ros2 topic echo /joint_states```
* open another bash, and publish:
  
  ```ros2 topic pub /pos_controller/commands std_msgs/msg/Float64MultiArray "{data: [-1]}" --once"```
* change run_gazebo.py [ctrl_name] to vec_controller, restart and pub

  ```ros2 topic pub /vec_controller/commands std_msgs/msg/Float64MultiArray "{data: [-1]}" --once"```
* change run_gazebo.py [ctrl_name] to tau_controller, restart and pub

  ```ros2 topic pub /tau_controller/commands std_msgs/msg/Float64MultiArray "{data: [-1]}" --once"```
* if you want pid control, 
* change <command_interface name="position"> to <command_interface name="position_pid">
* or change <command_interface name="velocity"> to <command_interface name="position_pid">

* In position control mode, when your position input is a fixed value, the velocity will stabilize at a non-zero constant after the joint motion ends. This should be a bug.
