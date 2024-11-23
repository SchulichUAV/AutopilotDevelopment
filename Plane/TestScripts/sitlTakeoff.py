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

import Plane.Operations.takeoffConfiguration as takeoff_configuration

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

takeoff_configuration.set_takeoff_altitude(vehicle_connection, 100)
takeoff_configuration.set_takeoff_angle(vehicle_connection, 20)
time.sleep(1)
arm.arm(vehicle_connection)
time.sleep(1)
mode.set_mode(vehicle_connection, 13)

'''
     implementation here
     on my machine, calling this function returns:
     CONDITION_CHANGE_ALT: UNSUPPORTED
     pls take a look on your machines ? 
'''

altitude.set_current_altitude(vehicle_connection, 300)
