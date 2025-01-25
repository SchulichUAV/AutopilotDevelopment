from pymavlink import mavutil
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.initialize as initialize

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

vehicle_connection.mav.param_set_send(
        target_system = vehicle_connection.target_system,
        target_component = vehicle_connection.target_component,
        param_id = b'MAV_BATTERY_FUNCTION',
        param_value = 3, # 3 for Avionics battery, may need to be changed
        param_type = mavutil.mavlink.MAV_PARAM_TYPE_UINT32
)

def receive_battery_data(vehicle_connection):
    '''
    PROMISES: Receives information about the system's battery
    REQUIRES: Vehicle connection
    '''
    print(vehicle_connection.recv_match(type='BATTERY_STATUS', blocking=True))