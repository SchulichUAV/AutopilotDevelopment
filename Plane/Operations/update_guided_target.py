#!/usr/bin/env python
import pymavlink.mavutil as mavutil
import pymavlink.dialects.v20.all as dialect
import time

def set_target(target_location):
    # Create target location message
    message = dialect.MAVLink_mission_item_int_message(
            target_system=plane.target_system,
            target_component=plane.target_component,
            seq=0,
            frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            command=dialect.MAV_CMD_NAV_WAYPOINT,
            current=2,
            autocontinue=0,
            param1=0,
            param2=0,
            param3=0,
            param4=0,
            x=int(target_location['latitude'] * 1e7),
            y=int(target_location['longitude'] * 1e7),
            z=100
        )
    # Send target location command to the vehicle
    plane.mav.send(message)

    return

if __name__ == '__main__':
    # Connect to Plane
    print('Attempting connect...')
    plane = mavutil.mavlink_connection(device="172.23.192.1:14500")
    plane.wait_heartbeat()
    print('Connected!')

    target_location = {
        'latitude': 51.107101210,
        'longitude': -1.79835804
    }

    while True:
        set_target(target_location)
        target_location['latitude'] = target_location['latitude'] + 0.001
        time.sleep(3)