import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.initialize as initialize
import General.Operations.mode as mode
import General.Operations.mission as mission
import Plane.Operations.waypoint as waypoint

vehicle_connection = initialize.connect_to_vehicle('udpin:172.20.128.1:14550')

waypoints = {}
# dummy waypoint
waypoints[0] = waypoint.set_mission_waypoint(vehicle_connection, -35.3603037, 149.1628575, 50, 0)
waypoints[1] = waypoint.set_mission_waypoint(vehicle_connection, -35.3603037, 149.1628575, 50, 1)
waypoints[2] = waypoint.set_mission_waypoint(vehicle_connection, -35.3609686, 149.1606474, 140, 2)
waypoints[3] = waypoint.set_mission_loiter_waypoint(vehicle_connection, -35.3620974, 149.1624109, 190, 5, 3)

mission.upload_mission_waypoints(vehicle_connection, waypoints)
mode.set_mode(vehicle_connection, 10)
