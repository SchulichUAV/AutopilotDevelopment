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
        altitude = int(data['altitude'])
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400
    
    waypoint.absolute_movement(vehicle_connection, latitude, longitude, altitude)
    
    return jsonify({'message': 'Waypoint set successfully'}), 200

@app.route('/testing', methods=['POST'])
def hello():
    print("hi")
    data = request.json
    try:
        latitude = int(data['latitude'])
        longitude = int(data['longitude'])
    except Exception as e:
        return jsonify({'error': 'Invalid data'}), 400

    return ({'message': 'success'}), 200

if __name__ == '__main__':
    # vehicle_connection = initialize.connect_to_vehicle()
    app.run(debug=True, host='0.0.0.0')