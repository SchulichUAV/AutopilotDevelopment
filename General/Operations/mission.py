import pymavlink.dialects.v20.all as dialect
import Plane.Operations.waypoint as waypoint
import General.Operations.monitor_waypoint as monitor_waypoint
import time

northing_offset = 1000
waypoint_radius = 15

def upload_payload_drop_mission(vehicle_connection, payload_object_coord):
    # PROMISES: Will upload a collection of waypoints to a ArduPilot vehicle
    # REQUIRES: A vehicle connection and a payload object location
    # Note:
    # - Waypoint 0 (Home position) is typically managed by the autopilot and will be ignored by the autopilot
    # - The autopilot will still request waypoint 0, but this function will send the "first" waypoint regardless
    # - The function will block until all waypoints are uploaded or a failure occurs.

    try:
        count = 3
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

            # payload waypoint
            if waypointId == 2:
                waypoint.set_mission_loiter_waypoint(vehicle_connection, payload_object_coord[0], payload_object_coord[1], payload_object_coord[2], waypoint_radius, waypointId)
            # offset waypoint
            else:
                waypoint.set_mission_waypoint_with_offset(vehicle_connection, payload_object_coord[0], payload_object_coord[1], payload_object_coord[2], waypointId, northing_offset)

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

def check_distance_and_drop(vehicle_connection, drop_distance):
    while 1:
        msg = vehicle_connection.recv_match(type='MISSION_CURRENT', blocking=False, timeout=5)
        if msg is not None and msg.seq == 2:
            break

    drop_done = False
    while not drop_done:
        distance = monitor_waypoint.receive_wp(vehicle_connection).wp_dist
        print(distance)
        
        msg = vehicle_connection.recv_match(type='MISSION_ITEM_REACHED', blocking=False, timeout=0.5)
        if (msg is not None and msg.seq == 2) or distance < drop_distance:
            ### TODO add code to drop payload
            print("Dropping payload...")
            drop_done = True
        time.sleep(0.1)        
