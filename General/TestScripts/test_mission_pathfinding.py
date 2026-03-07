import pytest
import modules.AutopilotDevelopment.General.Operations.waypoint_uploader as wu
import modules.AutopilotDevelopment.General.Operations.initialize as init
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Operations')))

from mission_pathfinding import find_best_waypoint_sequence, calculate_heading, calculate_cost, geofence_vectors, generate_random_waypoints

############################################### RECIEVE WAYPOINTS AS A DICT OF DICTS #################################################
'''
FORMAT:
waypoints = [
    {"waypointID": 1,"alt": 19,"lat": 9, "lon": 9},
    {"waypointID": 2, "alt": 19, "lat": 9,"lon": 9},
]
'''

all_waypoints = []
CURRENT_POS = [35.05932, -118.149, 25]
'''waypoint_list_of_dicts = [
    {"waypointID": 1, "alt": 50, "lat": 35.05987, "lon": -118.156},
    {"waypointID": 2, "alt": 100, "lat": 35.05991, "lon": -118.152},
    {"waypointID": 3, "alt": 75, "lat": 35.06121, "lon": -118.153},
    {"waypointID": 4, "alt": 50, "lat": 35.06312, "lon": -118.155},
    {"waypointID": 5, "alt": 50, "lat": 35.06127, "lon": -118.157},
    {"waypointID": 6, "alt": 75, "lat": 35.06206, "lon": -118.159},
    {"waypointID": 7, "alt": 100, "lat": 35.05989, "lon": -118.16},
]'''

for waypoint in waypoint_list_of_dicts:
    waypoint_coords = [waypoint["lat"], waypoint["lon"], waypoint["alt"]]
    all_waypoints.append(waypoint_coords)
    # You can now use waypoint_coords as needed
    
'''
#### Format Goal#####
# 2025 Reference waypoints (lat, lon, alt in meters)
WAYPOINT_A = [35.05987, -118.156, 50]
WAYPOINT_B = [35.05991, -118.152, 100]
WAYPOINT_C = [35.06121, -118.153, 75]
WAYPOINT_D = [35.06312, -118.155, 50]
WAYPOINT_E = [35.06127, -118.157, 50]
WAYPOINT_F = [35.06206, -118.159, 75]
WAYPOINT_G = [35.05989, -118.16, 100]
'''
############ Uncoment this section and comment out lines 37 & 38 to use data from the 2025 competition ############
#all_waypoints = [WAYPOINT_A, WAYPOINT_B, WAYPOINT_C, WAYPOINT_D, WAYPOINT_E, WAYPOINT_F, WAYPOINT_G]

readDict = {"waypoint_A": all_waypoints[0],
            "waypoint_B": all_waypoints[1],
            "waypoint_C": all_waypoints[2],
            "waypoint_D": all_waypoints[3],
            "waypoint_E": all_waypoints[4],
            "waypoint_F": all_waypoints[5],
            "waypoint_G": all_waypoints[6]}

# Geofence boundaries
GF_POINT_A = [35.05932, -118.149, 0]
GF_POINT_B = [35.06496, -118.156, 0]
GF_POINT_C = [35.06062, -118.163, 0]
GF_POINT_D = [35.05932, -118.163, 0]

GEOFENCE = [(35.05932, -118.149), (35.06496, -118.156), (35.06062, -118.163), (35.05932, -118.163)]
borders = geofence_vectors(GEOFENCE)
'''
all_waypoints = generate_random_waypoints(borders, GEOFENCE)

'''
'''
TESTING MOVING FORWARD
    - write out some example paths
    - have an ideal path in mind
    - see if pure function output generates that ideal path
    - take height into account here
    - see the output: which should be the list of waypoints in correct order
'''

'''
#########   Uncomment this function to run the test with the 2025 competition data    #########
                        # to do so must comment out the function below it #

def testFunction():
    current_heading = calculate_heading(CURRENT_POS, WAYPOINT_A, GEOFENCE)
    directions_to_mcdonalds = find_best_waypoint_sequence(all_waypoints, CURRENT_POS, current_heading, GEOFENCE)

    for waypoint in directions_to_mcdonalds:
        for key, value in readDict.items():
            if value == waypoint:
                print(f"{key} - {value}")
                break
'''

def testFunction():
    current_heading = calculate_heading(CURRENT_POS, all_waypoints[0], GEOFENCE)
    directions_to_mcdonalds = find_best_waypoint_sequence(all_waypoints, CURRENT_POS, current_heading, GEOFENCE)

    #print("Generated Waypoint Sequence:")
    #for waypoint in directions_to_mcdonalds:
        #print(waypoint)
    return directions_to_mcdonalds


if __name__ == "__main__":
    vehicle_connection = init.connect_to_vehicle(r"172.21.128.1:14550")
    wp = testFunction()
    wu.upload_mission_waypoints(vehicle_connection, wp)