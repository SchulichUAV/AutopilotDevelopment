# Connects to the vehicle and allows the operator to change waypoint error radius
# Created by: Liam Mah, November 2024

from pymavlink import mavutil

def set_waypoint_radius(vehicle_connection, radius):
    # PROMISES: Sets fixed-wing vehicle waypoint radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint radius
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