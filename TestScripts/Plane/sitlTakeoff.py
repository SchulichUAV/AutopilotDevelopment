from pymavlink import mavutil
import time
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import Operations.General.arm as arm
import Operations.General.initialize as initialize
import Operations.General.mode as mode
import Operations.Copter.takeoff as takeoff
import Operations.General.waypoint as waypoint

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

arm.arm(vehicle_connection)
time.sleep(1)
mode.set_mode(vehicle_connection, 19)
time.sleep(1)

