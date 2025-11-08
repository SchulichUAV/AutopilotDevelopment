import pytest
import numpy as np
import sys
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Operations')))

from mission_pathfinding import find_best_waypoint_sequence, calculate_heading, calculate_cost

# 2025 Reference waypoints (lat, lon, alt in meters)
CURRENT_POS = [35.05932, -118.149, 25]
WAYPOINT_A = [35.05987, -118.156, 50]
WAYPOINT_B = [35.05991, -118.152, 100]
WAYPOINT_C = [35.06121, -118.153, 75]
WAYPOINT_D = [35.06312, -118.155, 50]
WAYPOINT_E = [35.06127, -118.157, 50]
WAYPOINT_F = [35.06206, -118.159, 75]
WAYPOINT_G = [35.05989, -118.16, 100]
all_waypoints = [WAYPOINT_A, WAYPOINT_B, WAYPOINT_C, WAYPOINT_D, WAYPOINT_E, WAYPOINT_F, WAYPOINT_G]
readDict = {"waypoint_A": WAYPOINT_A,
            "waypoint_B": WAYPOINT_B,
            "waypoint_C": WAYPOINT_C,
            "waypoint_D": WAYPOINT_D,
            "waypoint_E": WAYPOINT_E,
            "waypoint_F": WAYPOINT_F,
            "waypoint_G": WAYPOINT_G}

# Geofence boundaries
GF_POINT_A = [35.05932, -118.149, 0]
GF_POINT_B = [35.06496, -118.156, 0]
GF_POINT_C = [35.06062, -118.163, 0]
GF_POINT_D = [35.05932, -118.163, 0]

GEOFENCE = [(35.05932, -118.149), (35.06496, -118.156), (35.06062, -118.163), (35.05932, -118.163)]

'''
TESTING MOVING FORWARD
    - write out some example paths
    - have an ideal path in mind
    - see if pure function output generates that ideal path
    - take height into account here
    - see the output: which should be the list of waypoints in correct order

'''

def testFunction():
    current_heading = calculate_heading(CURRENT_POS, WAYPOINT_A, GEOFENCE)
    directions_to_mcdonalds = find_best_waypoint_sequence(all_waypoints, CURRENT_POS, current_heading, GEOFENCE)

    for waypoint in directions_to_mcdonalds:
        for key, value in readDict.items():
            if value == waypoint:
                print(f"{key} - {value}")
                break

testFunction()