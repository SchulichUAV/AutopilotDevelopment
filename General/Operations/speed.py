# Provides functionality to change the speed

# Created by: Bryce Ilcan, november 7 2024

#TODO: Conduct safety checks with physical vehicle [IMPORTANT!]

from pymavlink import mavutil

def change_speed(vehicle_connection, speed, throttle=-1):
    # PROMISES: The vehicle's speed can be dynamically changed
    # REQUIRES: Vehicle connection, and speed

    vehicle_connection.mav.command_long_send( # Specify COMMAND_LONG
        vehicle_connection.target_system, # Specify vehicle target system
        vehicle_connection.target_component, # Specify the vehicle target component
        mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, # Specify speed command
        0, # Confirmation - 0: First transmission of this cmd, 1-255: Confirmation transmissions (e.g. kill)
        mavutil.mavlink.SPEED_TYPE_GROUNDSPEED, # Param 1 - setting speed type
        speed, # Param 2 - speed in m/s
        throttle, # Param 3 - throttle in percent
        0, # Param 4 - Unused, set to zero to populate all 7 parameters
        0, # Param 5 - Unused, set to zero to populate all 7 parameters
        0, # Param 6 - Unused, set to zero to populate all 7 parameters
        0 # Param 7 - Unused, set to zero to populate all 7 parameters
    )

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True) # Print ACK to confirm successful execution
    print(msg)

def set_airspeed_cruise(vehicle_connection, speed, throttle=-1):
    # PROMISES: Sets fixed-wing vehicle takeoff altitude configuration
    # REQUIRES: Vehicle connection, the desired height to take off to
    vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, # Specify speed command
        0, # Confirmation - 0: First transmission of this cmd, 1-255: Confirmation transmissions (e.g. kill)
        mavutil.mavlink.SPEED_TYPE_AIRSPEED, # Param 1 - setting speed type
        speed, # Param 2 - speed in m/s
        throttle, # Param 3 - throttle in percent
        0, # Param 4 - Unused, set to zero to populate all 7 parameters
        0, # Param 5 - Unused, set to zero to populate all 7 parameters
        0, # Param 6 - Unused, set to zero to populate all 7 parameters
        0 # Param 7 - Unused, set to zero to populate all 7 parameters
    )
    print(vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True))