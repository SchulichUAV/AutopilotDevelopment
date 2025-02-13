import time
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.initialize as initialize
import General.Operations.battery_data as get_battery

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')


while(1):
    get_battery.receive_battery_data(vehicle_connection)
    time.sleep(1)