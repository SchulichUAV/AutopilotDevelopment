# Connects to the vehicle and allows the operator to change waypoint error and loiter radius
# Created by: Liam Mah, November 2024

from pymavlink import mavutil

'''
WP_RADIUS helps us define the maximum distance from a waypoint that when crossed, indicates a completed waypoint.

A navigation controller may decide to turn later than WP_RADIUS before a waypoint, depending on sharpness of the turn
and speed of the aircraft. Typically you want to set WP_RADIUS to be much larger than the turn radius of your aircraft
so that the navigation controller can determine when to turn. If WP_RADIUS is too small, you will overshoot turns.

In summary, we want to tighten this ONLY for payload drops. We want to widen this by a large margin when flying a mission.
'''

def set_waypoint_radius(vehicle_connection, radius):
    # PROMISES: Sets fixed-wing vehicle waypoint radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint radius [m]
    if (radius < 1):
        print("ERROR! Your radius cannot be less than one.")
        return
    elif (radius > 32767):
        print("ERROR: Your radius is too large.")
        return

    vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'WP_RADIUS',
        radius,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (message['param_id'], message['param_value']))
    

def set_waypoint_loiter_radius(vehicle_connection, loiter_radius):
    # PROMISES: Sets fixed-wing vehicle waypoint loiter radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint loiter radius [m]
    if (loiter_radius < -32767):
        print("ERROR! Your radius is too large.")
        return
    elif (loiter_radius > 32767):
        print("ERROR: Your radius is too large.")
        return
    
    if (loiter_radius < 0):
        print("Loitering in clockwise circular motion.")
    else:
        print("Loitering in counter-clockwise circular motion.")

    vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'WP_LOITER_RAD',
        loiter_radius,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (message['param_id'], message['param_value']))

def set_waypoint_loiter_radius(vehicle_connection, rtl_loiter_radius):
    # PROMISES: Sets fixed-wing vehicle waypoint RTL loiter radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint RTL loiter radius [m]
    if (rtl_loiter_radius < -32767):
        print("ERROR! Your radius is too large.")
        return
    elif (rtl_loiter_radius > 32767):
        print("ERROR: Your radius is too large.")
        return
    
    if (rtl_loiter_radius < 0):
        print("Loitering in clockwise circular motion.")
    else:
        print("Loitering in counter-clockwise circular motion.")

    vehicle_connection.mav.param_set_send(
        vehicle_connection.target_system,
        vehicle_connection.target_component,
        b'RTL_RADIUS',
        rtl_loiter_radius,
        mavutil.mavlink.MAV_PARAM_TYPE_UINT32
    )

    message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    print('name: %s\tvalue: %d' %
        (message['param_id'], message['param_value']))