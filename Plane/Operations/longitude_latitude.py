# Retrieves the longitude and latitude from the plane using GPS_RAW_INT

def get_long_lat(vehicle_connection):
    # PROMISES: Retrieve longitude and latitude from aircraft
    # REQUIRES: Vehicle connection

    try:
        message = vehicle_connection.recv_match(type='GPS_RAW_INT', blocking='True')
        if message is None:
            print("Timeout: No Longitude and Latitude data recieved.")
            return None
        
        longitude = message.lon / 1e7  # convert from 1e-7 degrees to decimal degrees
        latitude = message.lat / 1e7   # convert from 1e-7 degrees to decimal degrees
        # do not know if the above conversion is necessary 

        print(f"Longitude: {longitude}, Latitude: {latitude}")

    except Exception as e:
        print(f"Error in recieving GPS data: {e}")
        return None
                                                