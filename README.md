# ROS 2 Delivery Mission Action Server

A ROS 2 Action-based delivery mission simulation developed as part of the **ETGAH ROS 2 Course**.

This project demonstrates how to create and use a custom ROS 2 Action interface to control a TurtleBot3 robot through a complete delivery mission. The robot receives a mission goal, drives to a pickup location, simulates package pickup while providing continuous feedback, then drives to the delivery location before reporting the mission result.

---

## Features

* Custom ROS 2 Action interface
* ROS 2 Action Server implementation
* TurtleBot3 movement using `/cmd_vel`
* Mission progress feedback
* Mission timeout handling
* Goal cancellation support
* Console logging for mission status

---

## Project Structure

```text
delivery_ws/
│
├── src/
│   ├── delivery_mission_controller/
│   │   ├── delivery_mission_controller/
│   │   │   ├── __init__.py
│   │   │   └── delivery_mission_node.py
│   │   ├── package.xml
│   │   ├── setup.py
│   │   └── setup.cfg
│   │
│   └── delivery_mission_interfaces/
│       ├── action/
│       │   └── DeliveryMission.action
│       ├── CMakeLists.txt
│       └── package.xml
│
├── Demo/
│   └── demo.webm
│
└── README.md
```

---

## Custom Action Definition

`DeliveryMission.action`

### Goal

```text
float32 speed
float32 pickup_duration
float32 delivery_duration
float32 timeout
```

### Result

```text
bool success
string message
```

### Feedback

```text
float32 remaining_time
float32 pickup_progress
```

---

## Mission Workflow

1. Receive a delivery mission goal.
2. Move toward the pickup location.
3. Stop the robot.
4. Simulate package pickup.
5. Publish pickup progress feedback.
6. Drive toward the delivery location.
7. Stop the robot.
8. Return the mission result.

---

## Build Instructions

Clone or copy the workspace and build it using:

```bash
cd ~/delivery_ws

colcon build

source install/setup.bash
```

---

## Running the Project

### Terminal 1

Run the Action Server:

```bash
source ~/delivery_ws/install/setup.bash

ros2 run delivery_mission_controller delivery_mission_node
```

---

### Terminal 2

Send a delivery mission goal:

```bash
source ~/delivery_ws/install/setup.bash

ros2 action send_goal /delivery_mission delivery_mission_interfaces/action/DeliveryMission "{speed: 0.2, pickup_duration: 4.0, delivery_duration: 5.0, timeout: 20.0}" --feedback
```

---

## Expected Output

The server prints messages similar to:

```text
Delivery Mission Action Server Started

========== Mission Started ==========

Driving to pickup location...

Picking up package...

Pickup Progress: 0%
Pickup Progress: 10%
Pickup Progress: 20%
...
Pickup Progress: 100%

Driving to delivery location...

========== Mission Completed ==========
```

The client receives continuous feedback:

```text
Feedback:
remaining_time: XX.X
pickup_progress: XX.X
```

Finally, the mission result is returned:

```text
Result:
success: True
message: Mission Completed Successfully
```

---

## Timeout Handling

If the mission execution time exceeds the specified timeout value:

* Robot stops immediately.
* Mission is aborted.
* Result returned:

```text
success: false
message: Mission Timeout
```

---

## Goal Cancellation

If the client cancels the goal while it is running:

* Robot stops immediately.
* Action is canceled.
* Result returned:

```text
success: false
message: Mission Cancelled
```

---

## Demo

A demonstration video is included in the repository:

```text
Demo/demo.webm
```

The video shows:

* Starting the Action Server
* Sending a delivery mission goal
* Robot movement
* Feedback updates
* Mission completion

---

## Concepts Demonstrated

* ROS 2 Actions
* Action Server
* Custom Action Interface
* Publishers
* geometry_msgs/Twist
* Robot motion control
* Feedback publishing
* Goal management
* Timeout handling
* Goal cancellation

---

## Author

**Ahmed Shalash**

