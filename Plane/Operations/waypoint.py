# Provides all fixed-wing waypoint functionality.

# Created by: Liam Mah, November 2024

from pymavlink import mavutil
import pymavlink.dialects.v20.all as dialect

def set_waypoint(vehicle_connection, latitude, longitude, altitude, autocontinue=0):
    # PROMISES: Will set a waypoint to fly to in guided mode
    # REQUIRES: A vehicle connection, latitude, longitude, and altitude to fly to
    try:
        mavlink_message = dialect.MAVLink_mission_item_int_message(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            seq=0, # Waypoint ID: Starts at zero, increases monotonically (0,1,2,3,...)
            frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # Coordinate system of waypoint
            command=dialect.MAV_CMD_NAV_WAYPOINT,
            current=2, # Current can be set to 2 to work in guided mode
            autocontinue=autocontinue, # Autocontinue to next waypoint (0 to pause mission after item completes)
            param1=0, # Ignored
            param2=0, # Acceptance radius [m] (if sphere with this radius is hit, waypoint counts as reached) 
            param3=0, # Pass radius, 0 to pass through WP. if >0, will CW orbit, <0 will have CCW orbit [m]
            param4=0, # Ignored
            x=int(latitude * 1e7), # latitude in degrees *10^7
            y=int(longitude * 1e7), # longitude in degrees *10^7
            z=altitude # altitude [m] - relative or absolute depending on frame
        )
        vehicle_connection.mav.send(mavlink_message)

        received_message = vehicle_connection.recv_match(type='MISSION_ACK', blocking=True, timeout=5)
        print(received_message)
    except Exception as e:
        print(f"Error in function: set_waypoint() from file: Plane/Operations/waypoint.py -> {e}")

def set_mission_waypoint(vehicle_connection, latitude, longitude, altitude, seq, acceptance_radius=15):
    # PROMISES: Will attempt to send mission waypoint message
    # REQUIRES: A vehicle connection, latitude, longitude, altitude, and a sequence number for the waypoint.
    try:
        mavlink_message = dialect.MAVLink_mission_item_int_message(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            seq=seq, # Waypoint ID
            frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # Coordinate system of waypoint
            command=dialect.MAV_CMD_NAV_WAYPOINT,
            current=0, # Current should be set to 0 for missions, really only used for download
            autocontinue=0, # Ignored by ArduPlane, as fixed-wing aircraft continuously follow mission waypoints in and do not pause at waypoints.
            param1=0, # Ignored 
            param2=acceptance_radius, # Acceptance radius [m] (if sphere with this radius is hit, waypoint counts as reached) 
            param3=0, # Pass radius, 0 to pass through WP. if >0, will CW orbit, <0 will have CCW orbit [m]
            param4=0, # Ignored
            x=int(latitude * 1e7), # latitude in degrees *10^7
            y=int(longitude * 1e7), # longitude in degrees *10^7
            z=altitude # altitude [m] - relative or absolute depending on frame
        )
        vehicle_connection.mav.send(mavlink_message)
        print(f"Sent mission message for sequence number {seq}")
    except Exception as e:
        print(f"Error in function: set_mission_waypoint() from file: Plane/Operations/waypoint.py -> {e}")

def set_mission_waypoint_with_offset(vehicle_connection, latitude, longitude, altitude, seq, northing_offset):
    # PROMISES: Will attempt to send mission waypoint message
    # REQUIRES: a vehicle connection, latitude, longitude, altitude, a sequence number for the waypoint, and a northing offset.

    # 1 degree of latitude ~ 111,320 meters
    lat_offset = northing_offset / 111320  
    # Apply the northing offset
    new_latitude = latitude + lat_offset
    try:
        set_mission_waypoint(vehicle_connection, new_latitude, longitude, altitude, seq)
    except Exception as e:
        print(f"Error in function: set_mission_waypoint() from file: Plane/Operations/waypoint.py -> {e}")    

def set_mission_loiter_waypoint(vehicle_connection, latitude, longitude, altitude, radius, seq):
    # PROMISES: Will return a MISSION_ITEM_INT message
    # REQUIRES: a vehicle connection, latitude, longitude, altitude, waypoint radius, and a sequence number for the waypoint.
    try:
        mavlink_message = dialect.MAVLink_mission_item_int_message(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            seq=seq, # Waypoint ID
            frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # Coordinate system of waypoint
            command=dialect.MAV_CMD_NAV_LOITER_UNLIM,
            current=0, # Current should be set to 0 for missions
            autocontinue=0, # Ignored by ArduPlane, as fixed-wing aircraft continuously follow mission waypoints in and do not pause at waypoints.
            param1=0, # Ignored 
            param2=0, # Ignored 
            param3=radius, # Loiter radius. if >0, will loiter CW, <0 will loiter CCW [m]
            param4=0, # Ignored
            x=int(latitude * 1e7), # latitude in degrees *10^7
            y=int(longitude * 1e7), # longitude in degrees *10^7
            z=altitude # altitude [m] - relative or absolute depending on frame
        )
        vehicle_connection.mav.send(mavlink_message)
        print(f"Sent mission message for sequence number {seq}")

    except Exception as e:
        print(f"Error in function: set_mission_waypoint() from file: Plane/Operations/waypoint.py -> {e}")


def set_waypoint_radius(vehicle_connection, radius):
    # PROMISES: Sets fixed-wing vehicle waypoint radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint radius [m]
    try:
        if (radius < 1):
            print("ERROR! Your radius cannot be less than one.")
            return
        elif (radius > 32767):
            print("ERROR: Your radius is too large.")
            return

        vehicle_connection.mav.param_set_send(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            param_id=b'WP_RADIUS',
            param_value=radius,
            param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
        )

        received_message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5).to_dict()
        print('name: %s\tvalue: %d' %
            (received_message['param_id'], received_message['param_value']))
    except Exception as e:
        print(f"Error in function: set_waypoint_radius() from file: Plane/Operations/waypoint.py -> {e}")


def set_waypoint_loiter_radius(vehicle_connection, loiter_radius):
    # PROMISES: Sets fixed-wing vehicle waypoint loiter radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint loiter radius [m]
    try:
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
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            param_id=b'WP_LOITER_RAD',
            param_value=loiter_radius,
            param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
        )

        received_message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5).to_dict()
        print('name: %s\tvalue: %d' %
            (received_message['param_id'], received_message['param_value']))
    except Exception as e:
        print(f"Error in function: set_waypoint_loiter_radius() from file: Plane/Operations/waypoint.py -> {e}")


def set_waypoint_rtl_loiter_radius(vehicle_connection, rtl_loiter_radius):
    # PROMISES: Sets fixed-wing vehicle waypoint RTL loiter radius configuration
    # REQUIRES: Vehicle connection, the desired waypoint RTL loiter radius [m]
    try:
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
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            param_id=b'RTL_RADIUS',
            param_value=rtl_loiter_radius,
            param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
        )

        received_message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5).to_dict()
        print('name: %s\tvalue: %d' %
            (received_message['param_id'], received_message['param_value']))
    except Exception as e:
        print(f"Error in function: set_waypoint_rtl_loiter_radius() from file: Plane/Operations/waypoint.py.py -> {e}")
