# Switches the current flight mode

# Created by: Liam Mah, May 2024

from pymavlink import mavutil

plane_modes = {
    "PLANE_MODE_MANUAL": 0,
    "PLANE_MODE_CIRCLE": 1,
    "PLANE_MODE_STABILIZE": 2,
    "PLANE_MODE_TRAINING": 3,
    "PLANE_MODE_ACRO": 4,
    "PLANE_MODE_FLY_BY_WIRE_A": 5,
    "PLANE_MODE_FLY_BY_WIRE_B": 6,
    "PLANE_MODE_CRUISE": 7,
    "PLANE_MODE_AUTOTUNE": 8,
    "PLANE_MODE_AUTO": 10,
    "PLANE_MODE_RTL": 11,
    "PLANE_MODE_LOITER": 12,
    "PLANE_MODE_TAKEOFF": 13,
    "PLANE_MODE_AVOID_ADSB": 14,
    "PLANE_MODE_GUIDED": 15,
    "PLANE_MODE_INITIALIZING": 16,
    "PLANE_MODE_QSTABILIZE": 17,
    "PLANE_MODE_QHOVER": 18,
    "PLANE_MODE_QLOITER": 19,
    "PLANE_MODE_QLAND": 20,
    "PLANE_MODE_QRTL": 21,
    "PLANE_MODE_QAUTOTUNE": 22,
    "PLANE_MODE_QACRO": 23,
    "PLANE_MODE_THERMAL": 24 
}

def set_mode(vehicle_connection, mode_id):
    # PROMISES: The vehicle will switch to the specified flight mode
    # REQUIRES: Vehicle connection, mode ID
    vehicle_connection.mav.command_long_send( # Specify COMMAND_LONG
        vehicle_system=vehicle_connection.target_system, # Specify target system
        target_component=vehicle_connection.target_component, # Specify target component
        command=mavutil.mavlink.MAV_CMD_DO_SET_MODE, # Command ID (or enum of command) - Set mode command
        confirmation=0, # Confirmation - 0: First transmission of this cmd, 1-255: Confirmation transmissions (e.g. kill)
        custom_mode_identification=mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, # Param 1 - MAV_MODE_FLAG_CUSTOM_MODE_ENABLED=1 (Enable custom mode identification)
        mode=mode_id, # Param 2 - Flight mode number
        _unused=0, # Param 3 - Unused, set to zero to populate all 7 parameters
        _unused=0, # Param 4 - Unused, set to zero to populate all 7 parameters
        _unused=0, # Param 5 - Unused, set to zero to populate all 7 parameters
        _unused=0, # Param 6 - Unused, set to zero to populate all 7 parameters
        _unused=0 # Param 7 - Unused, set to zero to populate all 7 parameters
    )

    msg = vehicle_connection.recv_match(type='COMMAND_ACK', blocking=True) 
    print(msg)
