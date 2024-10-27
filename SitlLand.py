from pymavlink import mavutil
import time

import Operations.arm as arm
import Operations.initialize as initialize
import Operations.mode as mode
import Operations.takeoff as takeoff
import Operations.waypoint as waypoint

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

mode.set_mode(vehicle_connection, 9)
