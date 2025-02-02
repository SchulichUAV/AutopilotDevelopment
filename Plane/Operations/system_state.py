# Connects to the vehicle and retrieves the general system vehicle system state

from pymavlink import mavutil

def receive_system_status(vehicle_connection):
    # PROMISES: Retreives general system state information of plane
    # REQUIRES: Vehicle connection
    try: 
        return vehicle_connection.recv_match(type='SYS_STATUS', blocking='True')
    except Exception as e:
        print(f"Error receiving system status: {e}")
        return None

def receive_param_request_read(vehicle_connection, param_id):
    # PROMISES: Retreives value of parameter thats passed in
    # REQUIRES: Vehicle connection, the desired parameter thats passed in
    param_id_bytes = param_id.encode('utf-8')
    
    try:
        vehicle_connection.mav.param_request_read_send(
            target_system=vehicle_connection.target_system,
            target_component=vehicle_connection.target_component,
            param_id=param_id_bytes,
            param_index=-1, # -1 to use param ID field as identifier
        )
    except Exception as e:
        print(f"Error sending param_request_read: {e}")
        return None 
    

    while True:
        try:
            message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5)
            if message is None:
                print("Timeout: No response recieved.")
                return None
        except Exception as e:
            print(f"Error receiving parameter value message: {e}")
        param_id_value = message.param_id

        if isinstance(param_id_value, bytes):
            param_id_value = param_id_value.decode('utf-8').strip('\x00')
        else:
            param_id_value= param_id_value.strip('\x00')

        if param_id_value == param_id:
            return message.param_value

def receive_gps_raw(vehicle_connection):
    # PROMISES: Retrieves general gps data
    # REQUIRES: Vehicle connection
    try:
        message = vehicle_connection.recv_match(type='GPS_RAW_INT', blocking='True')
        if message is None:
            print("Timeout: No GPS data received.")
            return None
        return message
    except Exception as e:
        print(f"Error receiving GPS data: {e}")
        return None

# def receive_gps_status(vehicle_connection):
#     # PROMISES:
#     # REQUIRES:
#     return vehicle_connection.recv_match(type='GPS_STATUS', blocking='True')

# def receive_scaled_imu(vehicle_connection):
#     # PROMISES:
#     # REQUIRES:
#     vehicle_connection.recv_match(type='SCALED_IMU', blocking='True')