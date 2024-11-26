from pymavlink import mavutil
import pymavlink.dialects.v20.all as dialect
import time
import math

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

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True) # Print command ACK to confirm successful execution
    print(msg)