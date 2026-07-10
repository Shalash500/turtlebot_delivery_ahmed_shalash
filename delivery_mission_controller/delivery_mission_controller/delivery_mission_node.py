import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from geometry_msgs.msg import Twist
from delivery_mission_interfaces.action import DeliveryMission # Import the delivery mission interface


class DeliveryMissionNode(Node):

    def __init__(self):
        super().__init__("delivery_mission_node")

        # Publisher used to control TurtleBot3 movement
        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)

        # Create the Action Server
        self.action_server = ActionServer(self, DeliveryMission, "delivery_mission", self.execute_callback)

        self.get_logger().info("Delivery Mission Action Server Started")

    # Publish a forward velocity command
    def move_forward(self, speed):
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = 0.0
        self.cmd_pub.publish(msg)

    # Stop the robot by publishing a zero Twist message
    def stop_robot(self):
        msg = Twist()
        self.cmd_pub.publish(msg)

    # Called automatically whenever a client sends a new goal
    def execute_callback(self, goal_handle):

        goal = goal_handle.request

        result = DeliveryMission.Result()
        feedback = DeliveryMission.Feedback()

        # Record mission start time for timeout calculations
        mission_start = time.time()

        self.get_logger().info("========== Mission Started ==========")


        # Phase 1 : Drive to Pickup Location
        self.get_logger().info("Driving to pickup location...")

        start = time.time()

        while time.time() - start < goal.pickup_duration:

            # Check whether the client requested cancellation
            if goal_handle.is_cancel_requested:
                self.stop_robot()
                goal_handle.canceled()

                result.success = False
                result.message = "Mission Cancelled"

                self.get_logger().info("Mission Cancelled")
                return result

            # Abort if mission execution exceeds timeout
            elapsed = time.time() - mission_start

            if elapsed >= goal.timeout:
                self.stop_robot()
                goal_handle.abort()

                result.success = False
                result.message = "Mission Timeout"

                self.get_logger().info("Mission Timeout")
                return result

            # Keep moving forward
            self.move_forward(goal.speed)
            time.sleep(0.1)

        # Stop before beginning the pickup process
        self.stop_robot()


        # Phase 2 : Simulate Package Pickup
        self.get_logger().info("Picking up package...")

        for i in range(11):

            # Handle goal cancellation
            if goal_handle.is_cancel_requested:
                self.stop_robot()
                goal_handle.canceled()

                result.success = False
                result.message = "Mission Cancelled"

                self.get_logger().info("Mission Cancelled")
                return result

            # Handle mission timeout
            elapsed = time.time() - mission_start

            if elapsed >= goal.timeout:
                self.stop_robot()
                goal_handle.abort()

                result.success = False
                result.message = "Mission Timeout"

                self.get_logger().info("Mission Timeout")
                return result

            # Update feedback values
            feedback.pickup_progress = float(i * 10)

            total_time = goal.pickup_duration + goal.delivery_duration

            remaining = max(
                0.0,
                total_time - elapsed
            )

            feedback.remaining_time = remaining

            # Send feedback to the Action Client
            goal_handle.publish_feedback(feedback)

            self.get_logger().info(
                f"Pickup Progress: {feedback.pickup_progress:.0f}%"
            )

            time.sleep(0.5)


        # Phase 3 : Drive to Delivery Location
        self.get_logger().info("Driving to delivery location...")

        start = time.time()

        while time.time() - start < goal.delivery_duration:

            # Check for cancellation
            if goal_handle.is_cancel_requested:
                self.stop_robot()
                goal_handle.canceled()

                result.success = False
                result.message = "Mission Cancelled"

                self.get_logger().info("Mission Cancelled")
                return result

            # Check for timeout
            elapsed = time.time() - mission_start

            if elapsed >= goal.timeout:
                self.stop_robot()
                goal_handle.abort()

                result.success = False
                result.message = "Mission Timeout"

                self.get_logger().info("Mission Timeout")
                return result

            # Continue driving
            self.move_forward(goal.speed)
            time.sleep(0.1)

        # Stop the robot after reaching the destination
        self.stop_robot()


        # Mission Completed Successfully
        goal_handle.succeed()

        result.success = True
        result.message = "Mission Completed Successfully"

        self.get_logger().info("========== Mission Completed ==========")

        return result


def main(args=None):
    rclpy.init(args=args)
    node = DeliveryMissionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()