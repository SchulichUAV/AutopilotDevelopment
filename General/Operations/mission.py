import pymavlink.dialects.v20.all as dialect
import modules.AutopilotDevelopment.Plane.Operations.waypoint as waypoint
import modules.AutopilotDevelopment.General.Operations.monitor_waypoint as monitor_waypoint
import modules.AutopilotDevelopment.General.Operations.speed as speed
import modules.payload as payload
import time
import json
import sys
import os

northing_offset = 1000
waypoint_radius = 15
drop_waypoint_radius = 1
default_speed = 18
loiter_radius = 40

def read_mission_json():
    try:
        base_dir = os.path.dirname(__file__)
        # file_path = os.path.join(base_dir, "airdrie.json") # Airdrie Flying Club
        # file_path = os.path.join(base_dir, "zone1.json") # Competition - zone 1 (left side, west end of runway)
        # file_path = os.path.join(base_dir, "zone2.json") # Competition - zone 2 (right side, east end of runway)
        file_path = os.path.join(base_dir, "test.json")
        

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Mission file not found at {file_path}")

        with open(file_path, 'r') as file:
            data = json.load(file)

        return data

    except Exception as e:
        raise ValueError("Failed to read mission JSON")

def drop_distance_json():
    try:
        data = read_mission_json()
        return data["drop_distance"]
    except Exception as e:
        raise ValueError("Failed to read drop distance")

def upload_payload_drop_mission(vehicle_connection, payload_object_coord):
    # PROMISES: Will upload a collection of waypoints to a ArduPilot vehicle
    # REQUIRES: A vehicle connection and a payload object location
    # Note:
    # - Waypoint 0 (Home position) is typically managed by the autopilot and will be ignored by the autopilot
    # - The autopilot will still request waypoint 0, but this function will send the "first" waypoint regardless
    # - The function will block until all waypoints are uploaded or a failure occurs.
    # - This function is specifically for payload missions. It will do extra checks to ensure all
    #   waypoints are uploaded correctly

    try:
        data = read_mission_json()
        waypoints = data.get("waypoints", {})
        entry = waypoints.get("entry")
        exit = waypoints.get("exit")

        if entry is None or exit is None:
            print("Missing 'entry' or 'exit' waypoint in mission file.")
            return

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
                waypoint.set_mission_waypoint(vehicle_connection, entry["lat"], entry["lon"], payload_object_coord[2], waypointId, waypoint_radius)
            
            # drop waypoint
            elif waypointId == 2:
                waypoint.set_mission_waypoint(vehicle_connection, payload_object_coord[0], payload_object_coord[1], payload_object_coord[2], waypointId, drop_waypoint_radius)
            
            # exit waypoint
            elif waypointId == 3:
                waypoint.set_mission_loiter_waypoint(vehicle_connection, exit["lat"], exit["lon"], payload_object_coord[2], loiter_radius, waypointId)
            
            # Payload waypoint and seq 0 waypoint, which is ignored by the autopilot
            else:
                waypoint.set_mission_waypoint(vehicle_connection, payload_object_coord[0], payload_object_coord[1], payload_object_coord[2], waypointId, waypoint_radius)

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
    
def upload_mission_waypoints(vehicle_connection):
    # PROMISES: Will upload a collection of waypoints to a ArduPilot vehicle
    # REQUIRES: A vehicle connection
    # Note:
    # - Waypoint 0 (Home position) is typically managed by the autopilot and will be ignored by the autopilot
    # - The autopilot will still request waypoint 0, but this function will send the "first" waypoint regardless
    # - The function will block until all waypoints are uploaded or a failure occurs.
    # - This function is for general mission uploads.

    try:
        data = read_mission_json()
        waypoints = data.get("waypoints", {})

        count = len(waypoints) + 1
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

            # assumes that waypoints are named with an id number, may be changed later
            upload_wp = waypoints.get(str(waypointId))

            # waypoint 0 - ignored by autopilot
            if waypointId == 0:
                waypoint.set_mission_waypoint(vehicle_connection, 0, 0, 0, waypointId, waypoint_radius)
            
            else:
                waypoint.set_mission_waypoint(vehicle_connection, upload_wp["lat"], upload_wp["lon"], upload_wp["alt"], waypointId, drop_waypoint_radius)

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

def check_distance_and_drop(vehicle_connection, current_servo, kit, vehicle_data):
    try:
        drop_distance = drop_distance_json()
    except Exception as e:
        print(f"[Error] Failed to load drop distance config: {e}")
        return

    try:
        while True:
            msg = vehicle_connection.recv_match(type='MISSION_CURRENT', blocking=False, timeout=5)
            if msg is not None and msg.seq == 2:
                try:
                    print(f"Setting cruise speed to minimum for drop.")
                    # speed.set_min_cruise_speed(vehicle_connection)
                except Exception as e:
                    print(f"[Error] Failed to set min cruise speed: {e}")
                break
    except Exception as e:
        print(f"[Error] Failed during MISSION_CURRENT check: {e}")
        return

    drop_done = False
    try:
        while not drop_done:
            try:
                distance = monitor_waypoint.receive_wp(vehicle_connection).wp_dist
                print(f"[Debug] Waypoint distance: {distance}")
            except Exception as e:
                print(f"[Error] Failed to get waypoint distance: {e}")
                break

            try:
                msg = vehicle_connection.recv_match(type='MISSION_ITEM_REACHED', blocking=False, timeout=0.5)
            except Exception as e:
                print(f"[Warning] Failed to read MISSION_ITEM_REACHED: {e}")
                msg = None

            if (msg is not None and msg.seq == 2) or distance < drop_distance:
                try:
                    payload.payload_release(kit, current_servo, vehicle_data)
                    print(f"Dropping payload for servo #{current_servo}")
                except Exception as e:
                    print(f"[Error] Failed to release payload: {e}")
                drop_done = True

            time.sleep(0.1)
    except Exception as e:
        print(f"[Error] Failed during drop distance monitoring loop: {e}")
        return

    try:
        print(f"Setting cruise speed back to {default_speed} m/s")
        # speed.set_cruise_speed(vehicle_connection, default_speed)
    except Exception as e:
        print(f"[Error] Failed to reset cruise speed: {e}")
    finally:
        print(f"[Thread] Payload drop thread for bay {current_servo + 1} exited")
