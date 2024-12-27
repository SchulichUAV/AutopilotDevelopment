# Provides all fixed-wing waypoint functionality.

# Created by: Liam Mah, November 2024

from pymavlink import mavutil
import pymavlink.dialects.v20.all as dialect

def set_waypoint(vehicle_connection, latitude, longitude, altitude):
    # PROMISES: Will set a waypoint to fly to in guided mode
    # REQUIRES: A vehicle connection, latitude, longitude, and altitude to fly to

    mavlink_message = dialect.MAVLink_mission_item_int_message(
        target_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        sqeuence_number=0, # Waypoint ID: Starts at zero, increases monotonically (0,1,2,3,...)
        coordinate_frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # Coordinate system of waypoint
        command=dialect.MAV_CMD_NAV_WAYPOINT,
        current=2, # Current can be set to 2 to work in guided mode
        autocontinue=0, # Autocontinue to next waypoint (0 to pause mission after item completes)
        hold_time=0, # Hold time [s] at waypoint, ignored by fixed wing 
        acceptance_radius=0, # Acceptance radius [m] (if sphere with this radius is hit, waypoint counts as reached) 
        pass_radius=0, # 0 to pass through WP. if >0, will CW orbit, <0 will have CCW orbit [m]
        yaw=0, # Desired yaw [degrees] at WP (NaN to use current system yaw heading mode)
        latitude=int(latitude * 1e7),
        longitude=int(longitude * 1e7),
        altitude=altitude # altitude [m]
    )
    vehicle_connection.mav.send(mavlink_message)

    received_message = vehicle_connection.recv_match(type='MISSION_ACK', blocking=True)
    print(received_message)

def set_waypoint_radius(vehicle_connection, radius):
    # PROMISES: Sets fixed-wing vehicle waypoint radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint radius [m]

    if (radius < 1):
        print("ERROR! Your radius cannot be less than one.")
        return
    elif (radius > 32767):
        print("ERROR: Your radius is too large.")
        return

    vehicle_connection.mav.param_set_send(
        target_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        param_id=b'WP_RADIUS',
        param_value=radius,
        param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    received_message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (received_message['param_id'], received_message['param_value']))
    

def set_waypoint_loiter_radius(vehicle_connection, loiter_radius):
    # PROMISES: Sets fixed-wing vehicle waypoint loiter radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint loiter radius [m]

    if (loiter_radius < -32767):
        print("ERROR! Your radius is too large.")
        return
    elif (loiter_radius > 32767):
        print("ERROR: Your radius is too large.")
        return
    
    if (loiter_radius < 0):
        print("Loitering in clockwise circular motion.")
    else:
        print("Loitering in counter-clockwise circular motion.")

    vehicle_connection.mav.param_set_send(
        target_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        param_id=b'WP_LOITER_RAD',
        param_value=loiter_radius,
        param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    received_message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (received_message['param_id'], received_message['param_value']))

def set_waypoint_rtl_loiter_radius(vehicle_connection, rtl_loiter_radius):
    # PROMISES: Sets fixed-wing vehicle waypoint RTL loiter radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint RTL loiter radius [m]

    if (rtl_loiter_radius < -32767):
        print("ERROR! Your radius is too large.")
        return
    elif (rtl_loiter_radius > 32767):
        print("ERROR: Your radius is too large.")
        return
    
    if (rtl_loiter_radius < 0):
        print("Loitering in clockwise circular motion.")
    else:
        print("Loitering in counter-clockwise circular motion.")

    vehicle_connection.mav.param_set_send(
        target_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        param_id=b'RTL_RADIUS',
        param_value=rtl_loiter_radius,
        param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    received_message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (received_message['param_id'], received_message['param_value']))