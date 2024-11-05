from pymavlink import mavutil
import time, os, sys

import Operations.General.arm as arm
import Operations.General.initialize as initialize
import Operations.General.mode as mode
import Operations.Copter.takeoff as takeoff
import Operations.General.waypoint as waypoint

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

master = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
master.wait_heartbeat()

def arm_and_takeoff(altitude):

    
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,
        1, 0, 0, 0, 0, 0, 0)
    time.sleep(4)
    print("Arming motors")


    mode.set_mode(master, 15)
    print("Set to GUIDED mode")
    time.sleep(4)

    
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0, 0, 0, 0,
        0, 0, altitude)

  
    while True:
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg.relative_alt >= altitude * 1000 * 0.95:
            print(f"Reached target altitude of {altitude} meters")
            break
        time.sleep(1)

def goto_position_target_global_int(aLat, aLon, aAlt):
    
    master.mav.set_position_target_global_int_send(
        0,
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b0000111111111000,
        int(aLat * 1e7),
        int(aLon * 1e7),
        aAlt,
        0, 0, 0,
        0, 0, 0,
        0, 0)

def return_to_launch():
   
    mode.set_mode(master, 10)
    print("Returning to launch")


arm_and_takeoff(10)


target_lat = 49.397742
target_lon = 7.545594
target_alt = 10
goto_position_target_global_int(target_lat, target_lon, target_alt)
return_to_launch()