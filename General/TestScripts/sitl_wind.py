import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import modules.AutopilotDevelopment.General.Operations.initialize as initialize
import modules.AutopilotDevelopment.General.Operations.wind as wind

vehicle_connection = initialize.connect_to_vehicle('udpin:172.20.128.1:14550')

wind.request_and_receive_wind(vehicle_connection)