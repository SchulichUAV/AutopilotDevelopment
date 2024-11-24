#!/usr/bin/env python3

import math
from pymavlink import mavutil

class mission_item:
    def __init__(self, i, current, x, y, z):
        self.seq = i
        self.frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        self.command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
        self.current = current
        self.auto = 1
        self.param1 = 0.0
        self.param2 = 2.00
        self.param3 = 20.00
        self.param4 = math.nan
        self.param5 = x
        self.param6 = y
        self.param7 = z
        self.mission_type = 0

def arm(the_connection):
    print("-- Arming")

    the_connection.mav.command_long_send( 
        the_connection.target_system, 
        the_connection.target_component, 
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, # Confirmation - 0: First transmission of this cmd, 1-255: Confirmation transmissions (e.g. kill)
        1, # Param 1 - Arm/Disarm Control [0: Disarm, 1: Arm]
        0, # Param 2 - Force [0: Arm-disarm unless prevented  by safety checks (i.e. when landed), 21196: Force arm/disarm to override preflight check and disarm during flight]
        0, # Param 3 - Unused, set to zero to populate all 7 parameters
        0, # Param 4 - Unused, set to zero to populate all 7 parameters
        0, # Param 5 - Unused, set to zero to populate all 7 parameters
        0, # Param 6 - Unused, set to zero to populate all 7 parameters
        0 # Param 7 - Unused, set to zero to populate all 7 parameters
    )

def takeoff(the_connection):
    print("-- Takeoff initiated")

    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, math.nan, 0, 0, 10)
    ack(the_connection, "COMMAND_ACK")

def upload_mission(the_connection, mission_items):
    n = len(mission_items)
    print("-- Sending Message out")

    the_connection.mav.mission_count_send(the_connection.target_system, the_connection.target_component, n, 0)

    ack(the_connection, "MISSION_REQUEST")

    for waypoint in mission_items:
        print("-- Creating a waypoint")

        the_connection.nav.mission_item_send(the_connection.target_system,
                                             the_connection.target_component,
                                             waypoint.seq,
                                             waypoint.frame,
                                             waypoint.command,
                                             waypoint.current,
                                             waypoint.auto,
                                             waypoint.param1,
                                             waypoint.param2,
                                             waypoint.param3,
                                             waypoint.param4,
                                             waypoint.param5,
                                             waypoint.param6,
                                             waypoint.param7,
                                             waypoint.mission_type)
    if waypoint != mission_items[n-1]:
        ack(the_connection, "MISSION_REQUEST")

    ack(the_connection, "MISSION_ACK")
    
def set_return(the_connection):
    print("-- Set Return to launch")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0)

    ack(the_connection, "COMMAND_ACK")

def start_mission(the_connection):
    print("-- Mission Start")
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                         mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0)
    ack(the_connection, "COMMAND_ACK")

def ack(the_connection, keyword):
    print("-- Message Read " + str(the_connection.recv_match(type=keyword, blocking=True)))

if __name__ == "__main__":
    print(" -- Program started")
    the_connection, valid_connection = mavutil.mavlink_connection('udpin:127.0.0.1:14550')

    while(the_connection.target_system == 0):
        print("Checking heartbeat")
        the_connection.wait_heartbeat()
        print("Heartbeat detected and connected successfully.")

        mission_waypoints = []
        mission_waypoints.append(mission_item(0, 0, 42.434193622721835, -83.98698183753619, 10)) # Above takeoff point
        mission_waypoints.append(mission_item(1, 0, 42.43432724637685, -83.98613425948624, 10)) # Above destination POint
        mission_waypoints.append(mission_item(2, 0, 42.43432724637685, -83.98613425948624, 5))  # Destination point

        upload_mission(the_connection, mission_waypoints)

        arm(the_connection)

        takeoff(the_connection)

        start_mission(the_connection)

        for mission_item in mission_waypoints:
            print("-- Message Read " + str(the_connection.recv_match(type="MISSION_ITEM_REACDHED")))

        set_return(the_connection)


