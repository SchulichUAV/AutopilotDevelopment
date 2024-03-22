# Connects to the vehicle and tests heartbeat

from pymavlink import mavutil

def verify_connection(vehicle_connection):
    # PROMISES: Vehicle heartbeat will be verified
    # REQUIRES: Vehicle connection
    # Verify vehicle heartbeat

    vehicle_connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" %
        (vehicle_connection.target_system, vehicle_connection.target_component))
    return True

def connect_to_vehicle(port='172.23.192.1:14500'):
    # PROMISES: Connection to the vehicle will be established
    # REQUIRES: Vehicle network port
    # Connect to the vehicle

    vehicle_connection = mavutil.mavlink_connection(port)
    valid_connection = verify_connection(vehicle_connection)   
    return vehicle_connection, valid_connection
