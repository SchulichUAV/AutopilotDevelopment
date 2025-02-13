# Connects to the vehicle and allows the operator to change fixed-wing takeoff configurations

# Created by: Liam Mah, November 2024

from pymavlink import mavutil

def set_takeoff_altitude(vehicle_connection, takeoff_height):
    # PROMISES: Sets fixed-wing vehicle takeoff altitude configuration
    # REQUIRES: Vehicle connection, the desired height to take off to
    try:
        vehicle_connection.mav.param_set_send(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            param_id=b'TKOFF_ALT', # takeoff altitude in metres
            param_value=takeoff_height,
            param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
        )

        message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5).to_dict()
        print('name: %s\tvalue: %d' %
            (message['param_id'], message['param_value']))
    except Exception as e:
        print(f"Error in function: set_takeoff_altitude() from file: Plane/Operations/takeoff.py -> {e}")

def set_takeoff_angle(vehicle_connection, takeoff_pitch_angle):
    # PROMISES: Sets fixed-wing vehicle takeoff pitch angle configuration
    # REQUIRES: Vehicle connection, the pitch ascent angle
    try:
        vehicle_connection.mav.param_set_send(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            param_id=b'TKOFF_LVL_PITCH',
            param_value=takeoff_pitch_angle,
            param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
        )

        message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5).to_dict()
        print('name: %s\tvalue: %d' %
            (message['param_id'], message['param_value']))
    except Exception as e:
        print(f"Error in function: set_takeoff_angle() from file: Plane/Operations/takeoff.py -> {e}")

