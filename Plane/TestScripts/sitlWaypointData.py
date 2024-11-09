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

def recieve_wp(vehicle_con):
    '''
    PROMISES: Returns data about the current target waypoint
    REQUIRES: vehicle_con recieves the vehicle connection as an input
    '''
    return vehicle_con.recv_match(type='NAV_CONTROLLER_OUTPUT', blocking=True)


def recieve_speeds(vehicle_con):
    '''
    PROMISES: Returns a list of the x, y, and z speeds of the aircraft
    REQUIRES: vehicle_con recieves the vehicle connection as an input
    '''
    speed_data = vehicle_con.recv_match(type='LOCAL_POSITION_NED', blocking=True)

    return [speed_data.vx, speed_data.vy, speed_data.vz]

def waypoint_ETA():
    pass
print(recieve_wp(vehicle_connection))