from pymavlink import mavutil
import time
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.arm as arm
import General.Operations.initialize as initialize
import General.Operations.mode as mode
import General.Operations.altitude as altitude
import General.Operations.speed as speed

import Plane.Operations.takeoff as takeoff_configuration

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

takeoff_configuration.set_takeoff_altitude(vehicle_connection, 100)
takeoff_configuration.set_takeoff_angle(vehicle_connection, 20)
time.sleep(1)
arm.arm(vehicle_connection)
time.sleep(1)
mode.set_mode(vehicle_connection, 13)

# example usage
#altitude.set_current_altitude(vehicle_connection, 300)
#altitude.get_current_altitude(vehicle_connection)

while(1):
    test_speed = float(input("Enter the speed (km/h): "))
    test_speed = test_speed / 3.6
    speed.set_cruise_speed(vehicle_connection, test_speed)


