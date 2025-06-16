import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import modules.AutopilotDevelopment.General.Operations.initialize as initialize
import modules.AutopilotDevelopment.General.Operations.mode as mode
import modules.AutopilotDevelopment.General.Operations.mission as mission
import modules.AutopilotDevelopment.Plane.Operations.waypoint as waypoint

vehicle_connection = initialize.connect_to_vehicle('udpin:172.25.176.1:14550')

object_location = [51.25996053, -113.9266562, 20]

mission.upload_payload_drop_mission(vehicle_connection, object_location)
print("Will need to manually put into AUTO mode...")
input("Press Enter to begin distance check and payload drop...")
mission.check_distance_and_drop(vehicle_connection, 1)
