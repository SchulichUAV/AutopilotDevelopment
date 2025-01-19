from pymavlink import mavutil
import time
import os
import sys

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.arm as arm
import General.Operations.initialize as initialize
import General.Operations.mode as mode
import Copter.Operations.takeoff as takeoff
import Copter.Operations.waypoint as waypoint

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

mode.set_mode(vehicle_connection, 9)

