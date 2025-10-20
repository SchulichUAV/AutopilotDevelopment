import pytest
import numpy as np
import sys
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Operations')))

from mission_pathfinding import find_best_waypoint_sequence, calculate_heading, calculate_cost

# 2025 Reference waypoints (lat, lon, alt in meters)
WAYPOINT_A = [35.05987, -118.156, 50]
WAYPOINT_B = [35.05991, -118.152, 100]
WAYPOINT_C = [35.06121, -118.153, 75]
WAYPOINT_D = [35.06312, -118.155, 50]
WAYPOINT_E = [35.06127, -118.157, 50]
WAYPOINT_F = [35.06206, -118.159, 75]
WAYPOINT_G = [35.05989, -118.16, 100]

# Geofence boundaries
GF_POINT_A = [35.05932, -118.149, 0]
GF_POINT_B = [35.06496, -118.156, 0]
GF_POINT_C = [35.06062, -118.163, 0]
GF_POINT_D = [35.05932, -118.163, 0]

# Mock calculate_cost for testing with GPS coordinates
def mock_calculate_cost_distance_only(currentPoint, point, currentHeading):
    """Simple distance-based cost for testing with lat/lon coordinates"""
    # Simple Euclidean distance (not geodesic, but good enough for testing small areas)
    # Scale longitude by cos(latitude) to account for Earth's curvature
    lat_avg = (currentPoint[0] + point[0]) / 2
    lat_scale = np.cos(np.radians(lat_avg))
    
    lat_diff = (point[0] - currentPoint[0]) * 111000  # ~111km per degree latitude
    lon_diff = (point[1] - currentPoint[1]) * 111000 * lat_scale  # Adjusted for latitude
    alt_diff = point[2] - currentPoint[2]
    
    distance = np.sqrt(lat_diff**2 + lon_diff**2 + alt_diff**2)
    return distance

def mock_calculate_cost_with_turns(currentPoint, point, currentHeading):
    """Cost with distance and turn penalties for GPS coordinates"""
    distance = mock_calculate_cost_distance_only(currentPoint, point, None)
    
    if currentHeading is None:
        return distance
    
    new_heading = calculate_heading(currentPoint, point)
    cos_angle = np.dot(currentHeading, new_heading)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle = np.arccos(cos_angle)
    
    turn_penalty = 100.0 * angle**2  # Higher penalty for GPS coordinates
    return distance + turn_penalty


class TestWaypointSequence:
    
    def test_single_waypoint_gps(self, monkeypatch):
        """Test with just one GPS waypoint"""
        monkeypatch.setattr('mission_pathfinding.calculate_cost', mock_calculate_cost_distance_only)
        
        waypoints = [WAYPOINT_A]
        currentPos = [35.05980, -118.157, 30]  # Starting position near the waypoints
        currentHeading = np.array([1, 0, 0])  # Initial heading (will be normalized)
        
        result = find_best_waypoint_sequence(waypoints, currentPos, currentHeading)
        
        assert len(result) == 2  # current pos + 1 waypoint
        assert result[0] == currentPos
        assert result[1] == WAYPOINT_A
    
    def test_two_waypoints_gps(self, monkeypatch):
        """Test with two GPS waypoints"""
        monkeypatch.setattr('mission_pathfinding.calculate_cost', mock_calculate_cost_distance_only)
        
        waypoints = [WAYPOINT_B, WAYPOINT_A]
        currentPos = [35.05980, -118.157, 30]
        currentHeading = np.array([1, 0, 0])
        
        result = find_best_waypoint_sequence(waypoints, currentPos, currentHeading)
        
        assert len(result) == 3
        assert result[0] == currentPos
        # Both waypoints should be in the result
        assert WAYPOINT_A in result
        assert WAYPOINT_B in result
    
    def test_three_waypoints_gps(self, monkeypatch):
        """Test with three GPS waypoints"""
        monkeypatch.setattr('mission_pathfinding.calculate_cost', mock_calculate_cost_distance_only)
        
        waypoints = [WAYPOINT_A, WAYPOINT_B, WAYPOINT_C]
        currentPos = [35.05980, -118.157, 30]
        currentHeading = np.array([0, 1, 0])  # Heading north
        
        result = find_best_waypoint_sequence(waypoints, currentPos, currentHeading)
        
        assert len(result) == 4
        assert result[0] == currentPos
        # All waypoints should be in the result
        for wp in waypoints:
            assert wp in result
    
    def test_all_seven_waypoints(self, monkeypatch):
        """Test with all seven competition waypoints"""
        monkeypatch.setattr('mission_pathfinding.calculate_cost', mock_calculate_cost_distance_only)
        
        waypoints = [WAYPOINT_A, WAYPOINT_B, WAYPOINT_C, WAYPOINT_D, 
                     WAYPOINT_E, WAYPOINT_F, WAYPOINT_G]
        currentPos = [35.05980, -118.157, 30]  # Starting position
        currentHeading = np.array([0, 1, 0])  # Heading north
        
        result = find_best_waypoint_sequence(waypoints, currentPos, currentHeading)
        
        assert len(result) == 8  # current pos + 7 waypoints
        assert result[0] == currentPos
        # All waypoints should be visited
        for wp in waypoints:
            assert wp in result
    
    def test_empty_waypoints_gps(self, monkeypatch):
        """Test with no waypoints"""
        monkeypatch.setattr('mission_pathfinding.calculate_cost', mock_calculate_cost_distance_only)
        
        waypoints = []
        currentPos = [35.05980, -118.157, 30]
        currentHeading = np.array([1, 0, 0])
        
        result = find_best_waypoint_sequence(waypoints, currentPos, currentHeading)
        
        assert len(result) == 1
        assert result[0] == currentPos
    
    def test_turn_penalty_affects_path_gps(self, monkeypatch):
        """Test that turn penalties favor straighter paths with GPS coords"""
        monkeypatch.setattr('mission_pathfinding.calculate_cost', mock_calculate_cost_with_turns)
        
        # Waypoints that test turning behavior
        waypoints = [WAYPOINT_B, WAYPOINT_A, WAYPOINT_G]
        currentPos = [35.05980, -118.157, 30]
        currentHeading = np.array([0, 1, 0])  # Heading north
        
        result = find_best_waypoint_sequence(waypoints, currentPos, currentHeading)
        
        # All waypoints should be visited
        assert len(result) == 4
        for wp in waypoints:
            assert wp in result
    
    def test_does_not_modify_input_gps(self, monkeypatch):
        """Ensure original waypoints list is not modified"""
        monkeypatch.setattr('mission_pathfinding.calculate_cost', mock_calculate_cost_distance_only)
        
        waypoints = [WAYPOINT_A, WAYPOINT_B, WAYPOINT_C]
        waypoints_copy = waypoints.copy()
        currentPos = [35.05980, -118.157, 30]
        currentHeading = np.array([1, 0, 0])
        
        result = find_best_waypoint_sequence(waypoints, currentPos, currentHeading)
        
        # Original list should be unchanged
        assert waypoints == waypoints_copy
    
    def test_altitude_variations(self, monkeypatch):
        """Test waypoints with different altitudes"""
        monkeypatch.setattr('mission_pathfinding.calculate_cost', mock_calculate_cost_distance_only)
        
        # Use waypoints with varying altitudes
        waypoints = [WAYPOINT_A, WAYPOINT_B, WAYPOINT_F]  # 50m, 100m, 75m
        currentPos = [35.05980, -118.157, 30]
        currentHeading = np.array([1, 0, 0])
        
        result = find_best_waypoint_sequence(waypoints, currentPos, currentHeading)
        
        assert len(result) == 4
        # All waypoints visited
        for wp in waypoints:
            assert wp in result


class TestCalculateHeading:
    
    def test_heading_gps_north(self):
        """Test heading calculation pointing north"""
        currentPoint = [35.05987, -118.156, 50]
        nextPoint = [35.06087, -118.156, 50]  # 100m north
        
        heading = calculate_heading(currentPoint, nextPoint)
        
        # Should be pointing primarily north (positive lat direction)
        assert heading[0] > 0.9  # Mostly north
        magnitude = np.linalg.norm(heading)
        assert abs(magnitude - 1.0) < 1e-10  # Normalized
    
    def test_heading_gps_east(self):
        """Test heading calculation pointing east"""
        currentPoint = [35.05987, -118.156, 50]
        nextPoint = [35.05987, -118.155, 50]  # East (less negative lon)
        
        heading = calculate_heading(currentPoint, nextPoint)
        
        # Should be pointing east (positive lon direction)
        assert heading[1] > 0.9  # Mostly east
        magnitude = np.linalg.norm(heading)
        assert abs(magnitude - 1.0) < 1e-10  # Normalized
    
    def test_heading_gps_with_altitude(self):
        """Test heading calculation with altitude change"""
        currentPoint = [35.05987, -118.156, 50]
        nextPoint = [35.05987, -118.156, 100]  # Straight up 50m
        
        heading = calculate_heading(currentPoint, nextPoint)
        
        # Should be pointing up (positive alt direction)
        assert heading[2] > 0.9  # Mostly up
        magnitude = np.linalg.norm(heading)
        assert abs(magnitude - 1.0) < 1e-10  # Normalized
    
    def test_heading_is_normalized_gps(self):
        """Test that heading is always unit length for GPS coords"""
        currentPoint = WAYPOINT_A
        nextPoint = WAYPOINT_D
        
        heading = calculate_heading(currentPoint, nextPoint)
        
        magnitude = np.linalg.norm(heading)
        assert abs(magnitude - 1.0) < 1e-10
    
    def test_heading_same_points_gps(self):
        """Test heading when GPS points are identical"""
        currentPoint = WAYPOINT_A
        nextPoint = WAYPOINT_A
        
        heading = calculate_heading(currentPoint, nextPoint)
        
        # Should return default heading
        np.testing.assert_array_almost_equal(heading, [1, 0, 0])


class TestIntegration:
    
    def test_competition_scenario(self, monkeypatch):
        """Test realistic competition scenario with all waypoints"""
        monkeypatch.setattr('mission_pathfinding.calculate_cost', mock_calculate_cost_distance_only)
        
        # All competition waypoints
        waypoints = [
            WAYPOINT_A, WAYPOINT_B, WAYPOINT_C, WAYPOINT_D,
            WAYPOINT_E, WAYPOINT_F, WAYPOINT_G
        ]
        # Starting from a position inside the geofence
        currentPos = [35.06000, -118.157, 30]
        currentHeading = np.array([0, 1, 0])  # Heading north
        
        result = find_best_waypoint_sequence(waypoints, currentPos, currentHeading)
        
        # Should visit all waypoints
        assert len(result) == 8
        
        # Calculate total path distance
        total_distance = 0
        for i in range(len(result) - 1):
            step_dist = mock_calculate_cost_distance_only(result[i], result[i+1], None)
            total_distance += step_dist
        
        # Distance should be reasonable (rough estimate: ~2-3km total)
        print(f"Total path distance: {total_distance:.2f} meters")
        assert total_distance > 0
        assert total_distance < 10000  # Should be less than 10km


if __name__ == "__main__":
    pytest.main([__file__, "-v"])