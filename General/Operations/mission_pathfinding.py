from typing import Optional
import numpy as np
import random

##### Constants: ####
ABORT_COST = 10000
# Conversion Factors: 
LATITUDE_TO_METERS = 111100
LONGITUDE_TO_METERS = 92300


def find_best_waypoint_sequence(waypoints: list, currentPos: list, currentHeading: list, geofence: list):
    """
    takes a list of waypoints as 3D vectors and the current position of the UAV and return the best sequence of waypoints for navigation


    Args:
        waypoints (list): list of list in form [[a,b,c],[x,y,z]...]
        currentPos (list): list in form [a,b,c]


    Returns:
        list: list of list in form [[a,b,c],[x,y,z]...]

    Post processing: 
        Format must be compatible with waypoint_uploader
        Convert the list of waypoints into a list of dict, waypoint_list = [{'lat': , 'lon': ,'alt': }, ...].
    """
    lowestCost, sequence = find_best_seq(currentPos, [currentPos], waypoints, 0, currentHeading, geofence)
    waypoint_list = []
    for waypoint in sequence:
        waypoint_dict = {'lat': waypoint[0], 'lon': waypoint[1], 'alt': waypoint[2]}
        waypoint_list.append(waypoint_dict)

    return waypoint_list


def find_best_seq(currentPoint, currentSeq, waypointsLeft, cost, currentHeading, geofence):
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
        stepCost = calculate_cost(currentPoint, point, currentHeading, geofence)

        # calculate the heading
        newHeading = calculate_heading(currentPoint, point, geofence)

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
            newHeading,
            geofence
        )

        # Update best solution if this path is better
        if totalCost < lowestCost:
            lowestCost = totalCost
            bestSequence = resultingSeq

    return lowestCost, bestSequence


def relative_coordinates(coord, geofence):
    """
    This function converts latitude / longitude points in space into meters from the center of geofence;
    the goal is to improve precision and consistency since height is in meters and latitude measurements
    are different from longitude measurements.
    """
    # STEP 1) To make the conversions we need the center of the geofence; geofence will come as an arument in the future.
    middleLat, middleLong = geofence_center(geofence)

    #### Converting Coordinate to Meters From the Center of the Geofence: ####
    if len(coord) > 2:
        xCoord = (coord[0] - middleLat) * LATITUDE_TO_METERS
        yCoord = (coord[1] - middleLong) * LONGITUDE_TO_METERS
        zCoord = coord[2]
        relative_coord = (xCoord, yCoord, zCoord)
    else:
        xCoord = (coord[0] - middleLat) * LATITUDE_TO_METERS
        yCoord = (coord[1] - middleLong) * LONGITUDE_TO_METERS
        relative_coord = (xCoord, yCoord,0)
    return relative_coord

def geofence_vectors(geofence):
    """
    This function connects each pair of consecutive geofence points with direction vectors and stores them at a list called geofenceV.
    The lists geofence and geofenceV will share the same indexing:
        - geofence[i] represents the position of the tail of geofenceV[i] direction vector.
    """
    geofenceV = []
    for i in range(len(geofence)): # loop through geofence points
        preVectorTail = relative_coordinates(geofence[i], geofence)
        preVectorHead = relative_coordinates(geofence[(i + 1) % len(geofence)], geofence) # "%len(geofence)" ensures we loop back to the first point after the last
        vectorTail = np.array(preVectorTail)
        vectorHead = np.array(preVectorHead) 
        vector = vectorHead - vectorTail
        geofenceV.append(vector)
    return geofenceV

def calculate_heading(currentPoint, point, geofence):
    """calculates the heading"""
    """
    Calculate the heading vector from one point to another.
 
    Args:
        currentPoint: current position (x, y, z)
        point: next waypoint (x, y, z)
 
    Returns:
        heading: normalized direction vector
    """
    relativeCurrentPoint = relative_coordinates(currentPoint, geofence)
    relativePoint = relative_coordinates(point, geofence)
    direction = np.array(relativePoint) - np.array(relativeCurrentPoint)

    norm = np.linalg.norm(direction)
    if norm > 0:
        heading = direction / norm
    else:
        heading = np.array([1, 0, 0])

    return heading


def calculate_cost(currentPoint, point, currentHeading, geofence):
    """
    Steps:
        1) convert all coordinates to meters from geofence center to make calculations simpler
        2) determine parameters to adjust weights and decide which path to go
        3) convert back to latitude and longitude and return results
    """
    ### Data Recieved: ###
    previousVector = currentHeading
    currentNode = currentPoint
    prospectiveNode = point

    ################### Converting Coordinates to Meters Based on Their Distances from geofence center ##################
    relativeCurrentNode = relative_coordinates(currentNode, geofence)  # currentNode -> Meters From Center of Geofence
    relativeNxtNode = relative_coordinates(prospectiveNode, geofence)  # relativeNxtNode -> Meters From Center of Geofence

    ############################## Calculating weigths of proposed path ######################################
    """
    Evaluating weights:
    Weight 1 - Distance: visualizing distances as vectors, the bigger the distance from head to tail the higher the weight
    Weight 2 - Angle: we can't turn more than 1.5 degrees per meter, sharp turns will lead to big weights
    Weight 3 - Risk: paths that approach the geofence borders at dangerous angles (close to perpendicular) will have big weights
    """
    currentWeight = 0
    ### Parameters for Weights Calculation: ###
    # Angle Weight Factors: -- parameters associated with Weight 2
    angleWeightFactor = 6  # greater values makes angle more impactful
    angleSteepnessFactor = 5.5  # this number defines how impactful it is to increase the angle
    # Risk Weight Factors: -- parameters associated with Weight 3
    safetyDistance = 80  # distance from geofence border to start considering risk
    perpendicularAngleLow = 70  # lower bound of angle to consider it perperdicular-ish
    perpendicularAngleHigh = 110  # upper bound of angle to consider it perperdicular-ish
    riskWeightPenalty = 5000  # greater values makes riskier paths more impactful

    # Vector from current position to prospective waypoint
    vectorTail = np.array(relativeCurrentNode)
    vectorHead = np.array(relativeNxtNode)
    prospectiveVector = vectorHead - vectorTail  # vector from current node to next node

    ### Weight 1: Distance from current position to prospective waypoint ###
    distance = np.linalg.norm(prospectiveVector)
    currentWeight += distance

    ### Weight 2: Angle per meter between previous vector and prospective vector ###
    dotProductTurn = prospectiveVector @ previousVector
    normPrevious = np.linalg.norm(previousVector)
    normProspective = np.linalg.norm(prospectiveVector)
    # Included angle formula from linear algebra, clip to avoid errors, then convert to degrees
    cosAngleTurn = dotProductTurn / (normProspective * normPrevious)
    cosAngleTurn = np.clip(cosAngleTurn, -1.0, 1.0) # Clip to handle floating-point precision errors
    # Calculate the included angle in degrees
    includedAngleTurn = np.degrees(np.arccos(cosAngleTurn))
    anglePerMeter = includedAngleTurn / distance
    # exponential function since path gets exponentially worse when angle/meter increases
    currentWeight += (cosAngleTurn + (angleWeightFactor ** (anglePerMeter * angleSteepnessFactor)))//2

    ### Weight 3: Distance from geofence borders, this weight will "prohibit" dangerous paths while ignoring safe ones ###
    """ 
    Explanation on Weight 3:
    Goal: prevent the UAV from approaching the geofence border at a dangerous angles (close to perperdicular).
    Steps:
        1) Call the function "geofence_vectors" to get the vectors connecting each geofence point.
        2) Loop through each geofence border and calculate the distance from the prospective path to each border using the point-to-vector distance formula.
        3) Loop through close borders and calculate the included angle between them and our prospective path using the included angle formula.
        4) If the included angle is close to perpendicular (between 70 and 110 degrees) it means the path is dangerous, so we add a huge weight to it. 
    """
    closeBorders = []  # list of geofence borders that are close to the prospective path
    borders = geofence_vectors(geofence) # vectors connecting the geofence borders
    pointToCheck = np.array(relativeNxtNode) # The endpoint of the prospective path
    # Loop through geofence borders and store close vectors
    for i, borderVector in enumerate(borders): 
        borderStart = np.array(relative_coordinates(geofence[i], geofence)) # "geofence" and "borders" lists share the same indexing, so geofence[i] is the start point of borders[i]
        projectionFactor = ((pointToCheck - borderStart) @ borderVector) / (borderVector @ borderVector) # Compute the scalar projection of the point onto the border vector    
        closestPointOnBorder = borderStart + projectionFactor * borderVector # Compute the closest point on the border segment to our point
        distanceToBorder = np.linalg.norm(pointToCheck - closestPointOnBorder) # Calculate the distance from our point to this closest point on the border
        if distanceToBorder < safetyDistance: # If the path endpoint is too close to this border, we must store it for angle evaluation
            closeBorders.append(borderVector)
    # Evaluate angles between prospective path and close borders to avoid leaving the geofence boundaries
    for closeBorderVector in closeBorders:
        dotProductBorder = prospectiveVector @ closeBorderVector
        normBorder = np.linalg.norm(closeBorderVector)
        cosAngleBorder = dotProductBorder / (normProspective * normBorder)
        cosAngleBorder = np.clip(cosAngleBorder, -1.0, 1.0) # Clip to avoid floating-point precision errors
        includedAngleBorder = np.degrees(np.arccos(cosAngleBorder)) # Calculate the included angle in degrees
        if includedAngleBorder > perpendicularAngleLow and includedAngleBorder < perpendicularAngleHigh: # if angle is perpendicular-ish
            currentWeight += riskWeightPenalty # big penalty for dangerous path, not worth it
    return currentWeight


def geofence_center(geofence):
    # Calculate the center of the geofence
    middleLat = (geofence[0][0] + geofence[1][0] + geofence[2][0] + geofence[3][0]) / 4
    middleLong = (geofence[0][1] + geofence[1][1] + geofence[2][1] + geofence[3][1]) / 4
    return middleLat, middleLong


def generate_random_waypoints(borders, geofence):
    """
    Generate random waypoints within geofence boundaries.
    Waypoints must be at least 60 meters apart from geofence border.
    Waypoints must be at least 250 meters apart from each other.
    """
    
    # Get geofence center in lat/long:
    middleLat, middleLong = geofence_center(geofence)
    newWaypoints = []
    possibleAltitudes = [50, 75, 100]

    # count attempts to avoid infinite loops:
    maxAttempts = 2000 
    attempts = 0

    # Generate 7 random waypoints:
    while len(newWaypoints) < 7:
        attempts += 1
        if attempts > maxAttempts:
            newWaypoints.clear() # reset list
            attempts = 0 # reset counter
            continue # restart waypoint generation from scratch

        # Generate random offset in meters:
        randomCoordX = random.randint(-200, 200)
        randomCoordY = random.randint(-330, 330)
        wayAltitude = random.choice(possibleAltitudes)
        
        # Create point in relative coordinates (meters from center of geofence)
        pointToCheck = np.array([randomCoordX, randomCoordY, wayAltitude])
        
        # Check distance from all borders
        validDistance = True
        for i, borderVector in enumerate(borders):
            borderStart = np.array(relative_coordinates(geofence[i], geofence))
            projectionFactor = ((pointToCheck - borderStart) @ borderVector) / (borderVector @ borderVector)
            closestPointOnBorder = borderStart + projectionFactor * borderVector
            distanceToBorder = np.linalg.norm(pointToCheck - closestPointOnBorder)
            if distanceToBorder <= 60:
                validDistance = False
                break
        
        # Check distance from all existing waypoints (must be at least 300m apart)
        if validDistance:
            for createdWaypoint in newWaypoints:
                normalizedCreatedWaypoint = np.array(relative_coordinates(createdWaypoint, geofence))
                vectorTail = normalizedCreatedWaypoint
                vectorHead = pointToCheck
                prospectiveVector = vectorHead - vectorTail
                distance = np.linalg.norm(prospectiveVector)
                if distance < 250:
                    validDistance = False
                    break
    
        # If point is valid, convert back to lat/long and add to waypoints
        if validDistance:
            wayLat = middleLat + (randomCoordX / LATITUDE_TO_METERS)
            wayLong = middleLong + (randomCoordY / LONGITUDE_TO_METERS)
            newWaypoints.append([wayLat, wayLong, wayAltitude])
            
    return newWaypoints