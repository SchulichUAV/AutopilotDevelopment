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
    
    #for every point from this one, calculate its cost and update the lowest cost and best sequence
    for i, point in enumerate(waypointsLeft):
        stepCost = calculate_cost(currentPoint, point, currentHeading)
        
        #calculate the heading
        newHeading = calculate_heading(currentPoint, point)

        # Create new sequence with this point added
        newSeq = currentSeq + [point]
        
        # Create new list of remaining waypoints (excluding current point)
        newWaypointsLeft = waypointsLeft[:i] + waypointsLeft[i+1:]
        
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


def best_start_point(waypoints: list, currentPoint: list):
    """
    Given waypoints and current position find best start waypoint
    """
    #TODO: impliment function 
    return waypoints[0]


def calculate_cost(currentPoint, point, currentHeading):
    """calculate the cost of flying from the current point to the next point"""
    return 0

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
    direction = np.array(point) - np.array(currentPoint)
    
    norm = np.linalg.norm(direction)
    if norm > 0:
        heading = direction / norm
    else:
        heading = np.array([1, 0, 0])
    
    return heading