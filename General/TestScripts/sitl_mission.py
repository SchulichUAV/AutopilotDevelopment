import sys
import os

# 1. Anchor to this file's folder, then jump up 4 steps to hit the '2025Electronics' root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))

# 2. Add the root directory to the Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 3. Now the modules imports will resolve perfectly!
import modules.AutopilotDevelopment.General.Operations.initialize as initialize
import modules.AutopilotDevelopment.General.Operations.mode as mode
import modules.AutopilotDevelopment.General.Operations.mission as mission
import modules.AutopilotDevelopment.Plane.Operations.waypoint as waypoint

# 3. Rest of your connection code...
vehicle_connection = initialize.connect_to_vehicle('udpin:0.0.0.0:14550')

# object_location = {"lat":-35.36500000, "lon": 149.16700000, "alt": 60.0}

mission.upload_payload_drop_mission(vehicle_connection)
mission.check_distance_and_drop(vehicle_connection, 0, None, None)