from pymavlink import mavutil


def set_current_altitude(vehicle_connection, altitude):
    # PROMISES: The vehicle will fly to the spcified height
    # REQUIRES: Vehicle connection, desired altitude (AGL in metres)
    try:
        vehicle_connection.mav.command_int_send(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, # Global (WGS84) coordinate frame + altitude relative to home position
            command=mavutil.mavlink.MAV_CMD_GUIDED_CHANGE_ALTITUDE,
            current=0, # Not used here, arbitrary value
            autocontinue=0, # Not used here, arbitrary value
            param1=0, # Not used here, arbitrary value
            param2=0, # Not used here, arbitrary value
            param3=0, # Not used here, arbitrary value
            param4=0, # Not used here, arbitrary value
            x=0, # Not used here, arbitrary value
            y=0, # Not used here, arbitrary value
            z=altitude
        )
    except Exception as e:
        print(f"Error in function: set_current_altitude() from file: Plane/Operations/altitude.py -> {e}")

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)
    print(msg)
