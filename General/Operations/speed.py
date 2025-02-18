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
        target_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        param_id=b'AIRSPEED_MAX',
        param_value=max_speed,
        param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

vehicle_connection.mav.param_set_send(
        target_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        param_id=b'AIRSPEED_MIN',
        param_value=min_speed,
        param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

def check_valid_speed(speed):
    #PROMISES: Returns 1 if the speed value is not between the max and min values
    #REQUIRES: "speed" is a positive, real number
    try:
        if(speed > max_speed):
            print("ERROR: requested speed above maximum allowed speed")
            return 1
        if(speed < min_speed):
            print("ERROR: requested speed below the minimum allowed speed")
            return 1
        return 0
    except Exception as e:
        print(f"Error in function: check_valid_speed() from file: General/Operations/speed.py -> {e}")


def set_guided_airspeed(vehicle_connection, speed, throttle=-1):
    # PROMISES: The vehicle's speed can be dynamically changed
    # REQUIRES: Vehicle connection, and speed
    try:
        if(check_valid_speed(speed) == 1): #if speed is invalid, exit function
            return

        vehicle_connection.mav.command_int_send(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, # Not used here, passing arbitrary value
            command=mavutil.mavlink.MAV_CMD_GUIDED_CHANGE_SPEED,
            current=0, # Not used here, arbitrary value
            autocontinue=0, # Not used here, arbitrary value
            param1=0, # Speed type: 0 = Airspeed
            param2=speed, # Not used here, arbitrary value
            param3=-1, # Throttle: -1 = no throttle change
            param4=0, # Not used here, arbitrary value
            x=0, # Not used here, arbitrary value
            y=0, # Not used here, arbitrary value
            z=0 # Not used here, arbitrary value
        )

        msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=5) # Print ACK to confirm successful execution
        print(msg)
    except Exception as e:
        print(f"Error in function: change_speed() from file: General/Operations/speed.py -> {e}")

def set_cruise_speed(vehicle_connection, speed):
    # PROMISES: Sets fixed-wing vehicle speed in m/s
    # REQUIRES: Vehicle connection, the desired vehicle speed
    try:
        if(check_valid_speed(speed) == 1): #if speed is invalid, exit function
            return

        vehicle_connection.mav.param_set_send(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            param_id=b'AIRSPEED_CRUISE',
            param_value=speed,
            param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
        )

        message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5).to_dict()
        print('name: %s\tvalue: %d' %
            (message['param_id'], message['param_value']))
    except Exception as e:
        print(f"Error in function: set_cruise_speed() from file: General/Operations/speed.py -> {e}")