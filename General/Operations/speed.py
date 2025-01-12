# Provides functionality to change the speed

# Created by: Bryce Ilcan, November 7th, 2024
# Valid Speed Check added by: Nathan Jourdain, November 30th, 2024

#TODO: Conduct safety checks with physical vehicle [IMPORTANT!]

from pymavlink import mavutil
import General.Operations.initialize as initialize

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

max_speed = 55 / 3.6 # 55 km/h converted to m/s
min_speed = 40 / 3.6 # 40 km/h converted to m/s

vehicle_connection.mav.param_set_send(
        vehicle_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        param_id=b'AIRSPEED_MAX',
        max_speed=max_speed,
        param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

vehicle_connection.mav.param_set_send(
        vehicle_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        param_id=b'AIRSPEED_MIN',
        min_speed=min_speed,
        param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

def check_valid_speed(speed):
    #PROMISES: Returns 1 if the speed value is not between the max and min values
    #REQUIRES: "speed" is a positive, real number
    
    if(speed > max_speed):
        print("ERROR: requested speed above maximum allowed speed")
        return 1
    if(speed < min_speed):
        print("ERROR: requested speed below the minimum allowed speed")
        return 1
    return 0


def change_speed(vehicle_connection, speed, throttle=-1):
    # PROMISES: The vehicle's speed can be dynamically changed
    # REQUIRES: Vehicle connection, and speed

    if(check_valid_speed(speed) == 1): #if speed is invalid, exit function
        return

    vehicle_connection.mav.command_long_send( # Specify COMMAND_LONG
        vehicle_system=vehicle_connection.target_system, # Specify vehicle target system
        target_component=vehicle_connection.target_component, # Specify the vehicle target component
        command=mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, # Specify speed command
        confirmation=0, # Confirmation - 0: First transmission of this cmd, 1-255: Confirmation transmissions (e.g. kill)
        speed_type=mavutil.mavlink.SPEED_TYPE_GROUNDSPEED, # Param 1 - setting speed type
        speed=speed, # Param 2 - speed in m/s
        throttle=throttle, # Param 3 - throttle in percent
        _unused_1=0, # Param 4 - Unused, set to zero to populate all 7 parameters
        _unused_2=0, # Param 5 - Unused, set to zero to populate all 7 parameters
        _unused_3=0, # Param 6 - Unused, set to zero to populate all 7 parameters
        _unused_4=0 # Param 7 - Unused, set to zero to populate all 7 parameters
    )

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True) # Print ACK to confirm successful execution
    print(msg)

def set_cruise_speed(vehicle_connection, speed):
    # PROMISES: Sets fixed-wing vehicle speed in m/s
    # REQUIRES: Vehicle connection, the desired vehicle speed

    if(check_valid_speed(speed) == 1): #if speed is invalid, exit function
        return

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
