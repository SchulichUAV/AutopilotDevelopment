from pymavlink import mavutil


def set_current_altitude(vehicle_connection, altitude):

    msg = vehicle_connection.mav.command_long_send(
            vehicle_connection.target_system,
            vehicle_connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_ALTITUDE,
            0,
            altitude,
            0, 0, 0, 0, 0, 0
    )

    vehicle_connection.mav.send(msg)

    print('Sent new altitude value set to {altitude} meters.')
