import pymavlink.dialects.v20.all as dialect
import Plane.Operations.waypoint as waypoint
import General.Operations.monitor_waypoint as monitor_waypoint
import General.Operations.speed as speed
import time
import json
import sys
import os

northing_offset = 1000
waypoint_radius = 15
altitude = 25

def read_mission_json():

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "missionWaypoint.json")

    with open(file_path, 'r') as file:
        data = json.load(file)

    return data.get("waypoints", {})


def upload_payload_drop_mission(vehicle_connection, payload_object_coord):
    # PROMISES: Will upload a collection of waypoints to a ArduPilot vehicle
    # REQUIRES: A vehicle connection and a payload object location
    # Note:
    # - Waypoint 0 (Home position) is typically managed by the autopilot and will be ignored by the autopilot
    # - The autopilot will still request waypoint 0, but this function will send the "first" waypoint regardless
    # - The function will block until all waypoints are uploaded or a failure occurs.

    try:
        data = read_mission_json()
        entry = data.get("entry")
        exit = data.get("exit")
        count = 4
        # Begin mission upload
        mission_count_msg = dialect.MAVLink_mission_count_message(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            count=count,  # Number of waypoints, including waypoint 0
            mission_type=0  # 0 = standard mission
        )
        vehicle_connection.mav.send(mission_count_msg)
        print(f"Sent mission count: {count}")

        # Loop through each waypoint request from the autopilot
        for waypointId in range(count):
            msg = vehicle_connection.recv_match(
                type=['MISSION_REQUEST_INT', 'MISSION_REQUEST'], 
                blocking=True, 
                timeout=5
            )

            if msg is None and msg.seq == waypointId:
                print("Mission upload failed: No valid request received from autopilot.")
                return False

            print(f"Sending waypoint {waypointId}")

            # entry waypoint
            if waypointId == 1:
                waypoint.set_mission_waypoint(vehicle_connection, entry["lat"], entry["lon"], altitude, waypointId)
            # payload waypoint
            elif waypointId == 2:
                waypoint.set_mission_waypoint(vehicle_connection, payload_object_coord[0], payload_object_coord[1], payload_object_coord[2], waypointId)
            # exit waypoint
            elif waypointId == 3:
                waypoint.set_mission_loiter_waypoint(vehicle_connection, exit["lat"], exit["lon"], altitude, waypoint_radius, waypointId)
            # Handle sequence number 0, which is ignored by the autopilot
            else:
                waypoint.set_mission_waypoint(vehicle_connection, payload_object_coord[0], payload_object_coord[1], payload_object_coord[2], waypointId)

        # Wait for final mission acknowledgment from autopilot
        msg = vehicle_connection.recv_match(type='MISSION_ACK', blocking=True, timeout=5)
        if msg is None:
            print("Mission upload failed: No MISSION_ACK received.")
            return False

        print("Mission upload completed successfully.")
        return True

    except Exception as e:
        print(f"Error in upload_mission_waypoints: {e}")
        return False

def check_distance_and_drop(vehicle_connection, drop_distance, current_servo):
    while 1:
        msg = vehicle_connection.recv_match(type='MISSION_CURRENT', blocking=False, timeout=5)
        if msg is not None and msg.seq == 2:
            speed.set_min_cruise_speed(vehicle_connection)
            break

    drop_done = False
    while not drop_done:
        distance = monitor_waypoint.receive_wp(vehicle_connection).wp_dist
        print(distance)
        
        msg = vehicle_connection.recv_match(type='MISSION_ITEM_REACHED', blocking=False, timeout=0.5)
        if (msg is not None and msg.seq == 2) or distance < drop_distance:
            ### TODO add code to drop payload
            print(f"Dropping payload for servo #{current_servo}")
            drop_done = True
        time.sleep(0.1)        
    speed.set_max_cruise_speed(vehicle_connection)

