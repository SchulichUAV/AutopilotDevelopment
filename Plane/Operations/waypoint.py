from pymavlink import mavutil
import pymavlink.dialects.v20.all as dialect
import time

def try_mav_reposition(vehicle_connection, latitude, longitude, altitude):
    vehicle_connection.mav.command_long_send()

def set_waypoint(vehicle_connection, latitude, longitude, altitude):
    # PROMISES: 
    # REQUIRES: 
    vehicle_connection.mav.mission_count_send(
            vehicle_connection.target_system,
            vehicle_connection.target_component,
            1, # Let's try to only do a single waypoint for now
            dialect.MAV_MISSION_TYPE_MISSION,
            10 # Some random number for testing purposes for now, seems to only be ID of current mission (used on download)
    )

    time.sleep(1)

    vehicle_connection.mav.send(dialect.MAVLink_mission_item_int_message(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        0,  # Waypoint number (0, 1, 2, ...)
        3,  # MAV_FRAME_GLOBAL_RELATIVE_ALT (WGS84 altitude relative to home position)
        dialect.MAV_CMD_NAV_WAYPOINT,  # Specify mission item int message
        2,  # current = 2 (indicate guided mode "goto" message: https://ardupilot.org/dev/docs/plane-commands-in-guided-mode.html)
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

    time.sleep(1)

    vehicle_connection.mav.command_long_send(vehicle_connection.target_system, vehicle_connection.target_component, 
                                             mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0)
    print("Starting mission")

