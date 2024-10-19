from pymavlink import mavutil

import Operations.arm as arm
import Operations.initialize as initialize
import Operations.mode as mode
import Operations.takeoff as takeoff
import Operations.waypoint as waypoint

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:localhost:14550')

arm.arm(vehicle_connection)
mode.set_mode(vehicle_connection, 0)
takeoff.takeoff(vehicle_connection, 20)