#copied imports from other pieces of code 
import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Point, Twist

#used to clamp the both coordinates to the inclusive range -10 through 10 logic is from postion_checker
def clamp(value):
    return max(-10, min(value, 10))

#alot of the class intilazation is just copied from command_sim and position_checker
class PositionControllerPublisher(Node):
    def __init__(self):
        super().__init__("position_controller_publisher")
        #Start at position (0, 0)
        self.x=0
        self.y=0
        #need for logic of stoping with e-stop logic taken from checker
        self.emergency_stop_active = False
        #copied from checker
        self.create_subscription(Bool, "/emergency_stop", self.on_estop, 10)
        self.create_subscription(Twist, "/movement_command", self.on_loctation, 10)
        #make a publisher that publishs the point x and y its /position because thats the topic name provided by the question and also cause geometry_msgs/Point dont work
        # Arguments: (Message Type, Topic Name, Queue Size)
        self.publisher = self.create_publisher(Point,"/position",10)
        
        

#should be same logic as postion_checker since the main loaction logic that uses the estop on or off logic is in on_locatation
    def on_estop(self, message):
        self.emergency_stop_active = message.data

#For each movement command, add linear.x and linear.y to the current X/Y position.
#Clamp both coordinates to the inclusive range -10 through 10.
    def on_loctation(self, command):
            if not self.emergency_stop_active:
                self.x = clamp(self.x + command.linear.x)
                self.y = clamp(self.y + command.linear.y)
            self.publish_postion()
                

#publish the point / same logic or code present in emergency_stop_pub
    def publish_postion(self):
        message=Point()
        message.x = self.x
        message.y = self.y
        self.publisher.publish(message)
     
#main just copy and paste spin just means do over and over agian so run the node over and over agian? destroy does what the name says
def main(args=None):
    rclpy.init(args=args)
    node = PositionControllerPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
#idk works so dont touch
if __name__ == "__main__":
    main()