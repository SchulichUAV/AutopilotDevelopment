import pymavlink.dialects.v20.all as dialect

def request_and_receive_wind(vehicle_connection, frequency_hz=1):
    # PROMISES: Requests and receives WIND message from the vehicle
    # REQUIRES: A MAVLink vehicle connection

    try:
        mavlink_message = dialect.MAVLink_command_long_message(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            command=dialect.MAV_CMD_SET_MESSAGE_INTERVAL,
            confirmation=0,
            param1=dialect.MAVLINK_MSG_ID_WIND,
            param2=1e6 / frequency_hz,
            param3=0,
            param4=0,
            param5=0,
            param6=0,
            param7=0
        )
        # Send request to vehicle
        vehicle_connection.mav.send(mavlink_message)
        print(f"Requested WIND message at {frequency_hz} Hz.")

        # Wait to receive the WIND message
        msg = vehicle_connection.recv_match(type='WIND', blocking=True, timeout=5)
        if msg:
            print(f"Direction: {msg.direction}, Speed: {msg.speed}, Vertical: {msg.speed_z}")
            return {
                "wind_direction": msg.direction,   # in degrees
                "wind_speed": msg.speed,           # in m/s
                "wind_vertical_speed": msg.speed_z # in m/s
            }
        else:
            print("No WIND message received!")
            return None

    except Exception as e:
        print(f"Error in function: request_and_receive_wind_cov() from file: General/Operations/wind.py -> {e}")
        return None
