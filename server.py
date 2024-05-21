import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

import Operations.arm as arm
import Operations.initialize as initialize
import Operations.mode as mode
import Operations.takeoff as takeoff
import Operations.waypoint as waypoint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # Overriding CORS for external access

vehicle_connection = None

@app.route('/coordinate_waypoint', methods=['POST'])
def coordinate_waypoint():
    data = request.json
    try:
        latitude = int(data['latitude'])
        longitude = int(data['longitude'])
        altitude = 25
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400
    
    waypoint.absolute_movement(vehicle_connection, latitude, longitude, altitude)
    
    return jsonify({'message': 'Waypoint set successfully'}), 200

@app.route('/relative_waypoint', methods=['POST'])
def relative_waypoint():
    data = request.json
    try:
        north = int(data['north'])
        east = int(data['east'])
        down = int(data['down'])
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400
    
    waypoint.relative_movement(vehicle_connection, north, east, down)
    
    return jsonify({'message': 'Waypoint set successfully'}), 200

@app.route('/arm', methods=['POST'])
def arm():
    arm.arm(vehicle_connection)
    return jsonify({'message': 'Vehicle armed successfully'}), 200

@app.route('/disarm', methods=['POST'])
def disarm():
    arm.disarm(vehicle_connection)
    return jsonify({'message': 'Vehicle disarmed successfully'}), 200

@app.route('/set_mode', methods=['POST'])
def set_mode():
    data = request.json
    try:
        mode_id = int(data['mode_id'])
        mode.set_mode(vehicle_connection, mode_id)
    except Exception as e:
        return jsonify({'error': 'Invalid data.'}), 400
    
    return jsonify({'message': 'Mode set successfully'}), 200

@app.route('/takeoff', methods=['POST'])
def takeoff():
    data = request.json
    try:
        takeoff_height = int(data['takeoff_height'])
        takeoff.takeoff(vehicle_connection, takeoff_height)
    except Exception as e:
        return jsonify({'error': 'Invalid data.'}), 400
    
    return jsonify({'message': 'Vehicle took off successfully'}), 200

if __name__ == '__main__':
    if len(sys.argv) == 2:
        vehicle_port = sys.argv[1]
    vehicle_connection = initialize.connect_to_vehicle(vehicle_port)
    retVal = initialize.verify_connection(vehicle_connection)
    if retVal != True:
        print("Connection failed. Exiting application.")
        exit(1)
        
    app.run(debug=True, host='0.0.0.0')