import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.arm as arm
import General.Operations.initialize as initialize
import General.Operations.mode as mode
import General.Operations.speed as speed
import General.Operations.monitor_waypoint as monitor_waypoint

import Plane.Operations.system_state as system_state ## not fully configured, needs to be checked with a gps
import Plane.Operations.takeoff as takeoff_config
import Plane.Operations.waypoint as waypoint

class Plane:
    def __init__(self, vehicle_connection='udpin:127.0.0.1:14550'):
        self.vehicle_connection = initialize.connect_to_vehicle(vehicle_connection)
        print(f"Connnected to vehicle at {vehicle_connection}")

    def arm_vehicle(self):
        arm.arm(self.vehicle_connection)

    def set_flight_mode(self, mode_id):
        mode.set_mode(self.vehicle_connection, mode_id)

    def set_speed(self, speed_input):
        speed.set_cruise_speed(self.vehicle_connection, speed_input)

    def add_waypoint(self, latitude, longitude, altitude):
        waypoint.set_waypoint(self.vehicle_connection, latitude, longitude, altitude)
    
