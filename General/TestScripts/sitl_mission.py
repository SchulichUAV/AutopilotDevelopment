import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import modules.AutopilotDevelopment.General.Operations.initialize as initialize
import modules.AutopilotDevelopment.General.Operations.mode as mode
import modules.AutopilotDevelopment.General.Operations.mission as mission
import modules.AutopilotDevelopment.Plane.Operations.waypoint as waypoint

vehicle_connection = initialize.connect_to_vehicle('udpin:172.18.192.1:14550')

object_location = {"lat":-35.36500000, "lon": 149.16700000, "alt": 60.0}

mission.upload_payload_drop_mission(vehicle_connection, object_location)
