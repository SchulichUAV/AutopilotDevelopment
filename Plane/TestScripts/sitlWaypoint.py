from pymavlink import mavutil
import time
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.arm as arm
import General.Operations.initialize as initialize
import General.Operations.mode as mode

import Plane.Operations.takeoffConfiguration as takeoff_configuration
import Plane.Operations.waypoint as waypoint

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')


ground_speed = 30 # [m/s]
loiter_radius = 20 # [m]
loiter_direction = 0 # 0: CW, 1: CCW
latitude: 0
longitude: 0
altitude: 100

takeoff_configuration.set_takeoff_altitude(vehicle_connection, 10)
takeoff_configuration.set_takeoff_angle(vehicle_connection, 20)
time.sleep(1)
arm.arm(vehicle_connection)
time.sleep(1)
mode.set_mode(vehicle_connection, 13)
time.sleep(5)
waypoint.reposition(vehicle_connection, ground_speed, loiter_radius, loiter_direction, latitude, longitude, altitude)



