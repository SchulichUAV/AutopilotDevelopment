from pymavlink import mavutil


def set_current_altitude(vehicle_connection, altitude):
    # PROMISES: The vehicle will fly to the spcified height
    # REQUIRES: Vehicle connection, desired altitude (AGL in metres)
    vehicle_connection.mav.command_int_send(
        target_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, # Global (WGS84) coordinate frame + altitude relative to home position
        command=mavutil.mavlink.MAV_CMD_DO_CHANGE_ALTITUDE,
        current=0, # Not used here, arbitrary value
        autocontinue=0, # Not used here, arbitrary value
        param1=altitude,
        param2=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
        param3=0, # Not used here, arbitrary value
        param4=0, # Not used here, arbitrary value
        x=0, # Not used here, arbitrary value
        y=0, # Not used here, arbitrary value
        z=0 # Not used here, arbitrary value
    )

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)