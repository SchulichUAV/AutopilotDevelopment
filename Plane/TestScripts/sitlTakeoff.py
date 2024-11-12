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

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

takeoff_configuration.set_takeoff_altitude(vehicle_connection, 100)
takeoff_configuration.set_takeoff_angle(vehicle_connection, 20)
time.sleep(1)
arm.arm(vehicle_connection)
time.sleep(1)
mode.set_mode(vehicle_connection, 13)

def set_altitude(altitude, frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT):

    vehicle_connection.wait_heartbeat()

    target_system = vehicle_connection.target_system
    target_component = vehicle_connection.target_component

    vehicle_connection.mav.set_position_target_global_int_send(
        0, # time since booting
        target_system,
        target_component,
        frame, 
        0b0000111111000111, # set altitude mask
        0,
        0,
        altitude,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    )

    print(f"Altitude now set to: {altitude} meters.")

def get_altitude():
    vehicle_connection.wait_heartbeat()

    vehicle_connection.mav.request_data_stream_send(

        vehicle_connection.target_system,
        vehicle_connection.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        1,
        1
    )

    msg = vehicle_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    altitude_meters = msg.alt 

    print(f"Current altitude: {altitude_meters}") 



set_altitude(100)

time.sleep(30) # just for testing if the altitude changes

get_altitude()
