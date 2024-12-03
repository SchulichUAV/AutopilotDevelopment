from pymavlink import mavutil
import time
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)


import General.Operations.initialize as initialize
import Plane.Operations.system_state as system_state

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')


while True:
    sys_status = system_state.receive_system_status(vehicle_connection)
    print(sys_status)
    gps_raw = system_state.receive_gps_raw(vehicle_connection)
    print(gps_raw)
    param_value = system_state.receive_param_request_read(vehicle_connection, 'TKOFF_ALT')
    if param_value is not None:
        print(f"TAKEOFF ALT: {param_value}")
    else:
        print("Failed to recieve parameter value.")

    time.sleep(5)