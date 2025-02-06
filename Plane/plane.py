from pymavlink import mavutil
import sys
import os

script_dir = os.path.abspath('./..')
sys.path.append(script_dir)

import General.Operations.arm as plane_arm
import General.Operations.initialize as plane_initialize
import General.Operations.mode as plane_mode
import General.Operations.speed as plane_speed
import General.Operations.monitor_waypoint as plane_monitor_waypoint

import Plane.Operations.system_state as plane_system_state
import Plane.Operations.takeoff as plane_takeoff_config
import Plane.Operations.waypoint as plane_waypoint

class Plane:
    def __init__(self, vehicle_connection='udpin:127.0.0.1:14550'):
        self.vehicle_connection, self.valid_connection = plane_initialize.connect_to_vehicle(vehicle_connection)
        print(f"Connnected to vehicle at {vehicle_connection}")

    def arm_vehicle(self):
        plane_arm.arm(self.vehicle_connection)

    def set_flight_mode(self, mode_id):
        plane_mode.set_mode(self.vehicle_connection, mode_id)

    def set_speed(self, speed_input):
        plane_speed.set_cruise_speed(self.vehicle_connection, speed_input)

    def get_waypoint_data(self):
        plane_monitor_waypoint.receive_wp(self.vehicle_connection)

    def get_speed_data(self):
        return plane_monitor_waypoint.receive_speeds(self.vehicle_connection)
    
    def calculate_waypoint_eta(self):
        return plane_monitor_waypoint.waypoint_eta(self.vehicle_connection)

    ## system state configurations
    def get_system_status(self):
        return plane_system_state.receive_system_status(self.vehicle_connection)
    
    def get_param_value(self, param_id):
        return plane_system_state.receive_param_request_read(self.vehicle_connection, param_id)
    
    def get_gps_raw(self):
        return plane_system_state.receive_gps_raw(self.vehicle_connection)
    
    def get_lat_long(self):
        lat_long_data = plane_system_state.receive_lat_long(self.vehicle_connection)
        if lat_long_data:
            print(f"Latitude: {lat_long_data['latitude']}, Longitude: {lat_long_data['longitude']}")
        return lat_long_data
    ## from system state, we still need gps status, scaled imu, utm_global_position and wind_cov

    ## takeoff configurations
    def set_takeoff_altitude(self, height):
        plane_takeoff_config.set_takeoff_altitude(self.vehicle_connection, height)

    def set_takeoff_angle(self, pitch):
        plane_takeoff_config.set_takeoff_angle(self.vehicle_connection, pitch)

    ## waypoint configurations
    def add_waypoint(self, latitude, longitude, altitude):
        plane_waypoint.set_waypoint(self.vehicle_connection, latitude, longitude, altitude)

    def set_waypoint_radius(self, radius):
        plane_waypoint.set_waypoint_radius(self.vehicle_connection, radius)

    def set_loiter_radius(self, loiter_radius):
        plane_waypoint.set_waypoint_loiter_radius(self.vehicle_connection, loiter_radius)

    def set_rtl_radius(self, rtl_loiter_radius):
        plane_waypoint.set_waypoint_rtl_loiter_radius(self.vehicle_connection, rtl_loiter_radius)
