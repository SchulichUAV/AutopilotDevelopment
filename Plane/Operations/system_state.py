# Connects to the vehicle and retrieves the general system vehicle system state

from pymavlink import mavutil

def receive_system_status(vehicle_connection):
    # PROMISES: Retreives general system state information of plane
    # REQUIRES: Vehicle connection
    return vehicle_connection.recv_match(type='SYS_STATUS', blocking='True')

def receive_param_request_read(vehicle_connection, param_id):
    # PROMISES: Retreives value of parameter thats passed in
    # REQUIRES: Vehicle connection, the desired parameter thats passed in
    param_id_bytes = param_id.encode('utf-8')
    
    vehicle_connection.mav.param_request_read_send(
        target_system=vehicle_connection.target_system,
        target_component=vehicle_connection.target_component,
        param_id=param_id_bytes,
        param_index=-1, # -1 to use param ID field as identifier
    )

    while True:
        message = vehicle_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5)
        if message is None:
            print("Timeout: No response recieved.")
            return None

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
    return vehicle_connection.recv_match(type='GPS_RAW_INT', blocking='True')

# def receive_gps_status(vehicle_connection):
#     # PROMISES:
#     # REQUIRES:
#     return vehicle_connection.recv_match(type='GPS_STATUS', blocking='True')

# def receive_scaled_imu(vehicle_connection):
#     # PROMISES:
#     # REQUIRES:
#     vehicle_connection.recv_match(type='SCALED_IMU', blocking='True')