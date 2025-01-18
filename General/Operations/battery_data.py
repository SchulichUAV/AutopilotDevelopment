from pymavlink import mavutil
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.initialize as initialize

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'MAV_BATTERY_FUNCTION',
        3, # 3 for Avionics battery, may need to be changed
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
)

def recieve_battery_data(vehicle_connection):
    print(vehicle_connection.recv_match(type='BATTERY_STATUS', blocking=True))