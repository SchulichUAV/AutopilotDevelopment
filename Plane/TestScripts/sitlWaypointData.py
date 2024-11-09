from pymavlink import mavutil
import time
import sys
import os

script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import General.Operations.arm as arm
import General.Operations.initialize as initialize
import General.Operations.mode as mode

import Plane.Operations.takeoffConfiguration as takeoff_configuration

vehicle_connection, valid_connection= initialize.connect_to_vehicle('udpin:127.0.0.1:14550')

def receive_wp(vehicle_con):
    '''
    PROMISES: Returns data about the current target waypoint
    REQUIRES: vehicle_con recieves the vehicle connection as an input
    '''
    return vehicle_con.recv_match(type='NAV_CONTROLLER_OUTPUT', blocking=True)


def receive_speeds(vehicle_con):
    '''
    PROMISES: Returns data about the airspeed, groundspeed, throttle, etc.
    REQUIRES: vehicle_con recieves the vehicle connection as an input
    '''
    speed_data = vehicle_con.recv_match(type='VFR_HUD', blocking=True)
    return speed_data

def waypoint_ETA(vehicle_con):
    '''
    PROMISES: Returns the estimated time (in seconds) until the current target waypoint is reached
    REQUIRES: vehicle_con recieves the vehicle connection as an input
    '''
    wp_distance = receive_wp(vehicle_con).wp_dist # find the distance to the target waypoint
    airspeed = receive_speeds(vehicle_con).airspeed # find the current airspeed

    wp_ETA = wp_distance / airspeed #calculate the ETA until the waypoint is reached
    return wp_ETA