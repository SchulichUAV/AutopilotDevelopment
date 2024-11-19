from pymavlink import mavutil
import pymavlink.dialects.v20.all as dialect
import time
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

def set_waypoint(vehicle_connection, latitude, longitude, altitude):
    # PROMISES: A waypoint will be set for the plane (will need to switch into guided or auto mode to activate)
    # REQUIRES: Vehicle connection, target latitude, longitude, and altitude
    vehicle_connection.mav.mission_count_send(
            vehicle_connection.target_system,
            vehicle_connection.target_component,
            1 # Specify a singular waypoint
    )

    vehicle_connection.mav.send(dialect.MAVLink_mission_item_int_message(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        0,  # Waypoint number (0, 1, 2, ...)
        3,  # MAV_FRAME_GLOBAL_RELATIVE_ALT (WGS84 altitude relative to home position)
        dialect.MAV_CMD_NAV_WAYPOINT,  # Specify mission item int message
        1,  # current (1 if this is the current waypoint, 0 otherwise)
        1,  # autocontinue to next point (1 to enable, 0 to disable)
        0,  # parameter 1 (hold time in seconds)
        0,  # parameter 2 (acceptance radius in meters)
        0,  # parameter 3 (pass radius in meters)
        0,  # parameter 4 (yaw angle)
        int(latitude * 1e7), # latitude (WGS84)
        int(longitude * 1e7), # longitude (WGS84)
        altitude  # Altitude in meters
    ))

    start_time = time.time()
    timeout = 5  # seconds
    while time.time() - start_time < timeout:
        # Fetch messages from the vehicle
        message = vehicle_connection.recv_match(type='MISSION_ACK', blocking=True, timeout=1)
        if message:
            if message.type == 0:  # MAV_MISSION_ACCEPTED
                print("Waypoint successfully set.")
                return
            else:
                print(f"Waypoint setting failed: {message.type}")
                return
    print("Timeout waiting for acknowledgment.")

    vehicle_connection.mav.mission_count_send(
            vehicle_connection.target_system,
            vehicle_connection.target_component,
            1
    )
