from pymavlink import mavutil
import time
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.arm as arm
import General.Operations.initialize as initialize
import General.Operations.mode as mode
import Plane.Operations.waypoint as waypoint

import Plane.Operations.takeoffConfiguration as takeoff_configuration

vehicle_connection, valid_connection = initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

takeoff_configuration.set_takeoff_altitude(vehicle_connection, 100)
takeoff_configuration.set_takeoff_angle(vehicle_connection, 20)
time.sleep(1)
arm.arm(vehicle_connection)
time.sleep(1)
mode.set_mode(vehicle_connection, 13)

time.sleep(15)

mode.set_mode(vehicle_connection, 15)
waypoint.set_waypont(vehicle_connection, 51.100000, 2.000000, 100)