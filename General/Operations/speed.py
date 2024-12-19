# Provides functionality to change the speed

# Created by: Bryce Ilcan, november 7 2024

#TODO: Conduct safety checks with physical vehicle [IMPORTANT!]

from pymavlink import mavutil

def change_speed(vehicle_connection, speed, throttle=-1):
    # PROMISES: The vehicle's speed can be dynamically changed
    # REQUIRES: Vehicle connection, and speed

    vehicle_connection.mav.command_long_send( # Specify COMMAND_LONG
        vehicle_system=vehicle_connection.target_system, # Specify vehicle target system
        target_component=vehicle_connection.target_component, # Specify the vehicle target component
        command=mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, # Specify speed command
        confirmation=0, # Confirmation - 0: First transmission of this cmd, 1-255: Confirmation transmissions (e.g. kill)
        speed_type=mavutil.mavlink.SPEED_TYPE_GROUNDSPEED, # Param 1 - setting speed type
        speed=speed, # Param 2 - speed in m/s
        throttle=throttle, # Param 3 - throttle in percent
        _unused=0, # Param 4 - Unused, set to zero to populate all 7 parameters
        _unused=0, # Param 5 - Unused, set to zero to populate all 7 parameters
        _unused=0, # Param 6 - Unused, set to zero to populate all 7 parameters
        _unused=0 # Param 7 - Unused, set to zero to populate all 7 parameters
    )

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True) # Print ACK to confirm successful execution
    print(msg)

def set_cruise_speed(vehicle_connection, speed):
    # PROMISES: Sets fixed-wing vehicle speed in m/s
    # REQUIRES: Vehicle connection, the desired vehicle speed
    vehicle_connection.mav.param_set_send(
        vehicle_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        param_id=b'AIRSPEED_CRUISE',
        pitch_angle=speed,
        param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (message['param_id'], message['param_value']))