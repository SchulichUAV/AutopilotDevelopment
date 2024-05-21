from flask import Flask, jsonify, request
from flask_cors import CORS

from FlightOperations import FlightOperations

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
    
    FlightOperations.absolute_movement(vehicle_connection, latitude, longitude, altitude)
    
    return jsonify({'message': 'Waypoint set successfully'}), 200


if __name__ == '__main__':
    vehicle_connection = FlightOperations.connect_to_vehicle()
    app.run(debug=True, host='0.0.0.0')