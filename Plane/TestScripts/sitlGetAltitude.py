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

mode.set_mode(vehicle_connection, 7)
altitude.set_current_altitude(vehicle_connection, 300)
altitude.get_current_altitude(vehicle_connection)
time.sleep(20)
altitude.get_current_altitude(vehicle_connection)
