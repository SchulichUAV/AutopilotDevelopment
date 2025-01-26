import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.initialize as initialize
import General.Operations.mode as mode
import General.Operations.speed as speed

vehicle_connection, valid_connection = initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

mode.set_mode(vehicle_connection, 15)
speed.set_guided_airspeed(vehicle_connection, 90)
