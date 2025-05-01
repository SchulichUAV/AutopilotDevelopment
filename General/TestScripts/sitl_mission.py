import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.initialize as initialize
import General.Operations.mode as mode
import General.Operations.mission as mission
import Plane.Operations.waypoint as waypoint

vehicle_connection = initialize.connect_to_vehicle('udpin:172.25.176.1:14550')

object_location = [-35.3634185, 149.1604543, 50]

mission.upload_payload_drop_mission(vehicle_connection, object_location)
mode.set_mode(vehicle_connection, 10)
mission.check_distance_and_drop(vehicle_connection, 95)
