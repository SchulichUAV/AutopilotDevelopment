from pymavlink import mavutil
import sys
import os

script_dir = os.path.abspath('./..')
sys.path.append(script_dir)

import modules.AutopilotDevelopment.General.Operations.arm as copter_arm
import modules.AutopilotDevelopment.General.Operations.battery_data as copter_battery_data
import modules.AutopilotDevelopment.General.Operations.initialize as copter_initialize
import modules.AutopilotDevelopment.General.Operations.mode as copter_mode
import modules.AutopilotDevelopment.General.Operations.speed as copter_speed
import modules.AutopilotDevelopment.General.Operations.monitor_waypoint as copter_monitor_waypoint

import modules.AutopilotDevelopment.Copter.Operations.takeoff as copter_takeoff
import modules.AutopilotDevelopment.Copter.Operations.waypoint as copter_waypoint

class Copter:
    def __init__(self, vehicle_connection='udpin:127.0.0.1:14550'):
        self.vehicle_connection, self.valid_connection = copter_initialize.connect_to_vehicle(vehicle_connection)
        print(f"Connnected to vehicle at {vehicle_connection}")

    def arm_vehicle(self):
        copter_arm.arm(self.vehicle_connection)

    def set_flight_mode(self, mode_id):
        copter_mode.set_mode(self.vehicle_connection, mode_id)

    def set_speed(self, speed_input):
        copter_speed.set_cruise_speed(self.vehicle_connection, speed_input)

    def get_waypoint_data(self):
        copter_monitor_waypoint.receive_wp(self.vehicle_connection)

    def get_battery_data(self):
        return copter_battery_data.receive_battery_data(self.vehicle_connection)

    def get_speed_data(self):
        return copter_monitor_waypoint.receive_speeds(self.vehicle_connection)
    
    def calculate_waypoint_eta(self):
        return copter_monitor_waypoint.waypoint_eta(self.vehicle_connection)

    def set_takeoff(self, height): 
        ## may want to change how this works and store a takeoff value since copter_takeoff.takeoff() sets height then immediately takes off
        copter_takeoff.takeoff(self.vehicle_connection, height)

    def calculate_waypoint_progress(self):
        copter_waypoint.waypoint_progress(self.vehicle_connection)

    def waypoint_move_xyz(self, xdistance, ydistance, zdistance):
        copter_waypoint.relative_movement(self.vehicle_connection, xdistance, ydistance, zdistance)

    def absolute_movement(self, latitude, longitude, altitude):
        copter_waypoint.absolute_movement(self.vehicle_connection, latitude, longitude, altitude)