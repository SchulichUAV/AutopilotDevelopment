from pymavlink import mavutil
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import modules.AutopilotDevelopment.General.Operations.initialize as initialize

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

def confirm_param():
    try:
        message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
        print('Set parameter %s to value: %d\n' %
            (message['param_id'], message['param_value']))
    except Exception as e:
        print(f"Error in function: confirm_param() from file: Plane/Operations/safety-script.py -> {e}")

print("Setting maximum airspeed... (Desired value: 15)")
max_speed = 55 / 3.6 # 55 km/h converted to m/s
vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'AIRSPEED_MAX',
        max_speed,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )
confirm_param()

print("Setting minimum airspeed... (Desired value: 11)")
min_speed = 40 / 3.6 # 40 km/h converted to m/s
vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'AIRSPEED_MIN',
        min_speed,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )
confirm_param()

print("Setting waypoint radius... (Desired value: 0)")
vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'WP_RADIUS',
        0,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )
confirm_param()

print("Setting waypoint loiter radius... (Desired value: 50)")
vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'WP_LOITER_RAD',
        50,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )
confirm_param()

print("Setting RTL radius... (Desired value: 50)")
vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'RTL_RADIUS',
        50,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )
confirm_param()