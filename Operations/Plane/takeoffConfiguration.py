# Connects to the vehicle and allows the operator to change fixed-wing takeoff configurations

# Created by: Liam Mah, November 2024

from pymavlink import mavutil

def set_takeoff_altitude(vehicle_connection, takeoff_height):
    # PROMISES: Sets fixed-wing vehicle takeoff altitude configuration
    # REQUIRES: Vehicle connection, the desired height to take off to
    vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'TKOFF_ALT',
        takeoff_height,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True) # Print command ACK to confirm successful execution
    print(msg)

def set_takeoff_angle(vehicle_connection, takeoff_pitch_angle):
    # PROMISES: Sets fixed-wing vehicle takeoff pitch angle configuration
    # REQUIRES: Vehicle connection, the pitch ascent angle
    vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'TKOFF_ALT',
        takeoff_pitch_angle,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True) # Print command ACK to confirm successful execution
    print(msg)
    
