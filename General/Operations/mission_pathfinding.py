from typing import Optional
import numpy as np

ABORT_COST = 10000


def find_best_waypoint_sequence(waypoints: list, currentPos: list, currentHeading: list):
    """
    takes a list of waypoints as 3D vectors and the current position of the UAV and return the best sequence of waypoints for navigation


    Args:
        waypoints (list): list of list in form [[a,b,c],[x,y,z]...]
        currentPos (list): list in form [a,b,c]


    Returns:
        list: list of list in form [[a,b,c],[x,y,z]...]
    """

    lowestCost, sequence = find_best_seq(currentPos, [currentPos], waypoints, 0, currentHeading)

    return sequence


def find_best_seq(currentPoint, currentSeq, waypointsLeft, cost, currentHeading):
    # Base case: if there are no waypoints left, return the accumulated cost
    if len(waypointsLeft) == 0:
        return cost, currentSeq

    # Prune infeasible paths early
    if cost > ABORT_COST:
        return float('inf'), []

    lowestCost = float('inf')
    bestSequence = []

    # for every point from this one, calculate its cost and update the lowest cost and best sequence
    for i, point in enumerate(waypointsLeft):
        stepCost = calculate_cost(currentPoint, point, currentHeading)

        # calculate the heading
        newHeading = calculate_heading(currentPoint, point)

        # Create new sequence with this point added
        newSeq = currentSeq + [point]

        # Create new list of remaining waypoints (excluding current point)
        newWaypointsLeft = waypointsLeft[:i] + waypointsLeft[i + 1:]

        # Recursively find best path from this point
        totalCost, resultingSeq = find_best_seq(
            point,
            newSeq,
            newWaypointsLeft,
            cost + stepCost,
            newHeading
        )

        # Update best solution if this path is better
        if totalCost < lowestCost:
            lowestCost = totalCost
            bestSequence = resultingSeq

    return lowestCost, bestSequence


def relative_coordinates(coord):
    """
    This function converts latitude / longitude points in space into meters from the center of geofence;
    the goal is to improve precision and consistency since height is in meters and latitude measurements
    are different from longitude measurements.
    """
    #### Conversion Factors: ###
    latitude_to_meters = 111100
    longitude_to_meters = 92300
    # STEP 1) To make the conversions we need the center of the geofence; geofence will come as an arument in the future.
    geofence = [(35.05932, -118.149), (35.06496, -118.156), (35.06062, -118.163), (35.05932, -118.163)]
    middle_lat = (geofence[0][0] + geofence[1][0] + geofence[2][0] + geofence[3][0]) / 4
    middle_long = (geofence[0][1] + geofence[1][1] + geofence[2][1] + geofence[3][1]) / 4
    #### Converting Coordinate to Meters From the Center of the Geofence: ####
    x_coord = (coord[0] - middle_lat) * latitude_to_meters
    y_coord = (coord[1] - middle_long) * longitude_to_meters
    z_coord = coord[2]
    relative_coord = (x_coord, y_coord, z_coord)
    return relative_coord


def calculate_heading(currentPoint, point):
    """calculates the heading"""
    """
    Calculate the heading vector from one point to another.
 
    Args:
        currentPoint: current position (x, y, z)
        point: next waypoint (x, y, z)
 
    Returns:
        heading: normalized direction vector
    """
    relativeCurrentPoint = relative_coordinates(currentPoint)
    relativePoint = relative_coordinates(point)
    direction = np.array(relativePoint) - np.array(relativeCurrentPoint)

    norm = np.linalg.norm(direction)
    if norm > 0:
        heading = direction / norm
    else:
        heading = np.array([1, 0, 0])

    return heading


def calculate_cost(currentPoint, point, currentHeading):
    """
    Steps:
        1) convert all coordinates to meters from geofence center to make calculations simpler
        2) determine parameters to adjust weights and decide which path to go
        3) convert back to latitude and longitude and return results
    """
    ### Data Recieved and Transformed: ###
    previousVector = currentHeading
    currentNode = currentPoint
    prospectiveNode = point

    ################### Converting Coordinates to Meters Based on Their Distances from geofence center ##################
    relativeCurrentNode = relative_coordinates(currentNode)  # currentNode -> Meters From Center of Geofence
    relativeNxtNode = relative_coordinates(prospectiveNode)  # relativeNxtNode -> Meters From Center of Geofence

    ############################## Calculating weigths of proposed path ######################################
    """
    Evaluating weights:
    Distances: visualizing distances as vectors, the bigger the distance from head to tail the higher the weight
    Angle: we can't turn more than 1.5 degrees per meter, sharp turns will lead to big weights
    """
    # Nearest Neighbour weight calculation:
    # angle weight factors:
    angleWeightFactor = 100  # greater values makes angle more impactful
    angleSteepnessFactor = 4  # this number defines how impactful it is to increase the angle

    current_weight = 0
    # Vector from current position to prospective waypoint
    vectorTail = np.array(relativeCurrentNode)
    vectorHead = np.array(relativeNxtNode)
    prospectiveVector = vectorHead - vectorTail  # vector from current node to endpoint
    # Weight 1: Distance from tail to head
    distance = np.linalg.norm(prospectiveVector)
    current_weight += distance
    # Weight 2: Angle per meter (skip on first iteration)
    dotProduct = np.dot(prospectiveVector, previousVector)
    normPrevious = np.linalg.norm(previousVector)
    normProspective = np.linalg.norm(prospectiveVector)
    # Included angle formula from linear algebra, clip to avoid errors, then convert to degrees
    cosAngle = dotProduct / (normProspective * normPrevious)
    # Clip to handle floating-point precision errors
    cosAngle = np.clip(cosAngle, -1.0, 1.0)
    # Calculate the included angle in degrees
    includedAngle = np.degrees(np.arccos(cosAngle))
    anglePerMeter = includedAngle / distance
    # exponential function since path gets exponentially worse when angle/meter increases
    current_weight += angleWeightFactor ** (anglePerMeter * angleSteepnessFactor)
    return current_weight
