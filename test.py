import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

import Operations.arm as arm
import Operations.initialize as initialize
import Operations.mode as mode
import Operations.takeoff as takeoff
import Operations.waypoint as waypoint

# Some flight mode IDs...
# 0 - Stabilize
# 3 - Loiter
# 6 - RTL (Return to Launch)
# 15 - Guided (Autonomous Mode)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        vehicle_port = sys.argv[1]

    BAUD = 57600
    vehicle_port = 'COM6'

    print(f"Attempting to connect to port: {vehicle_port}")
    vehicle_connection = initialize.connect_to_vehicle(vehicle_port, BAUD)
    print("Vehicle connection established.")
    retVal = initialize.verify_connection(vehicle_connection)
    print("Vehicle connection verified.")
    
    if retVal != True:
        print("Connection failed. Exiting application.")
        exit(1)

    mode = input("Enter mode: ")
    mode = int(mode)

    mode.set_mode(vehicle_connection, mode)