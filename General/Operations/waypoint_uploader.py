import pymavlink.dialects.v20.all as dialect
import modules.AutopilotDevelopment.Plane.Operations.waypoint as waypoint
from modules.AutopilotDevelopment.General.Operations.mission_pathfinding import find_best_waypoint_sequence, calculate_heading, calculate_cost, geofence_vectors, generate_random_waypoints
from modules.AutopilotDevelopment.General.TestScripts.test_mission_pathfinding import testFunction

waypoint_radius = 15

waypoints = testFunction()

def upload_mission_waypoints(vehicle_connection, waypoints):
    # PROMISES: Will upload a collection of waypoints to a ArduPilot vehicle
    # REQUIRES: A vehicle connection and a list of waypoints
    # Note:
    # - Waypoint 0 (Home position) is typically managed by the autopilot and will be ignored by the autopilot
    # - The autopilot will still request waypoint 0, but this function will send the "first" waypoint regardless
    # - The expected format for waypoint data is a list of {"lat":[num], "lon":[num], "alt":[num]}
    # - The function will block until all waypoints are uploaded or a failure occurs.
    # - This function is for general mission uploads.

    try:
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

        print(waypoints)
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

            # assumes that waypoints are named with an id number, may be changed later
            

            # waypoint 0 - ignored by autopilot
            if waypointId == 0:
                print(f"Sending waypoint {waypointId}: { {"lat":0, "lon": 0, "alt": 0} }")
                waypoint.set_mission_waypoint(vehicle_connection, 0, 0, 0, waypointId, waypoint_radius)
            
            else:
                upload_wp = waypoints[waypointId - 1]
                print(f"Sending waypoint {waypointId}: {upload_wp}")
                waypoint.set_mission_waypoint(vehicle_connection, upload_wp["lat"], upload_wp["lon"], upload_wp["alt"], waypointId, waypoint_radius)

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
