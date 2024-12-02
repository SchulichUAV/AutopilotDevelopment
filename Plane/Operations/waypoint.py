# Provides all fixed-wing waypoint functionality.

# Created by: Liam Mah, November 2024

from pymavlink import mavutil
import pymavlink.dialects.v20.all as dialect

def set_waypoint(vehicle_connection, latitude, longitude, altitude):
    # Create target location message
    vehicle_connection.mav.send(dialect.MAVLink_mission_item_int_message(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        0, # Sequence number
        dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        dialect.MAV_CMD_NAV_WAYPOINT,
        2, # Current can be 2 to work in guided mode
        0, # Autocontinue (do not continue to next waypoint)
        0, # Hold time at waypoint for rotor, ignored by fixed wing
        0, # Acceptance radius for waypoint
        0, # Pass radius
        0, # Yaw
        int(latitude * 1e7),
        int(longitude * 1e7),
        altitude
    ))

    msg = vehicle_connection.recv_match(type='MISSION_ACK', blocking=True)
    print(msg)

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
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'WP_RADIUS',
        radius,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (message['param_id'], message['param_value']))
    

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
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'WP_LOITER_RAD',
        loiter_radius,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (message['param_id'], message['param_value']))

def set_waypoint_loiter_radius(vehicle_connection, rtl_loiter_radius):
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
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'RTL_RADIUS',
        rtl_loiter_radius,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (message['param_id'], message['param_value']))