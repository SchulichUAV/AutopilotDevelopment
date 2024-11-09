# Allows the aerial vehicle to navigate to a waypoint in guided mode without planning a mission
# Flies to a set of coordinates (latitude, longitude, altitude)

# Created by: Liam Mah, May 2024

from pymavlink import mavutil

def reposition(vehicle_connection, ground_speed, loiter_radius, loiter_direction, latitude, 
                  longitude, altitude):
    vehicle_connection.mav.send(vehicle_connection.mav.command_int_send( # Specify COMMAND_LONG
        vehicle_connection.target_system, # Specify target system
        vehicle_connection.target_component, # Specify target component
        mavutil.mavlink.MAV_CMD_DO_REPOSITION, # Command ID (or enum of command) - Set mode command
        0, # Confirmation - 0: First transmission of this cmd, 1-255: Confirmation transmissions (e.g. kill)
        ground_speed, 
        1, # Param 2 - 0: Don't put into guided automatically, 1: put into guided automatically 
        loiter_radius,
        loiter_direction,
        latitude, 
        longitude, 
        altitude 
    ))

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True) # Print command ACK to confirm successful execution
    print(msg)
