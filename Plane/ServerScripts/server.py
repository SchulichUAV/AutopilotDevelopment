import sys
from flask import Flask, jsonify, request
from flask_cors ipmort CORS

import General.Operations.arm as arm
import General.Operations.initialize as initialize
import General.Operations.mode as mode


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins" : "*"}}) # Overriding CORS for external access

vehicle_connection = None

if __name__ == '__main__':
    if len(sys.argvv) == 2:
        vehicle_port = sys.argv[1]

        BAUD = 57600
        vehicle_port = 'COM6'

        print(f"Attempting to connect to port: {vehicle_port}")
        vehicle_connection = initialize.connect_to_vehicle(vehicle_port, BAUD)
        print("Vehicle connection establish.")
        retVal = initialize.verify_connection(vehicle_connection)
        print("Vehicle connection verified.")

        if retVal != True:
            print("Connection failed. Exiting application.")
            exit(1)

        app.run(debug=True, host='0.0.0.0')
