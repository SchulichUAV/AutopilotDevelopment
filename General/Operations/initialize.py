# Connects to the vehicle and tests heartbeat

# Created by: Liam Mah, May 2024

from pymavlink import mavutil

def verify_connection(vehicle_connection):
    # PROMISES: Vehicle heartbeat will be verified
    # REQUIRES: Vehicle connection
    # Verify vehicle heartbeat
    try:
        vehicle_connection.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" %
            (vehicle_connection.target_system, vehicle_connection.target_component))
        return True
    except Exception as e:
        print(f"Error in function: verify_connection() from file: General/Operations/initialize.py -> {e}")
        return False

def connect_to_vehicle(port='172.23.192.1:14500'):
    # PROMISES: Connection to the vehicle will be established
    # REQUIRES: Vehicle network port
    # Connect to the vehicle
    try:
        vehicle_connection = mavutil.mavlink_connection(port)
        valid_connection = verify_connection(vehicle_connection)
        if valid_connection:
            return vehicle_connection
        else:
            print("Error trying to verify connection. Exiting.")
            exit(1)
    except Exception as e:
        print(f"Error in function: connect_to_vehicle() from file: General/Operations/initialize.py -> {e}")