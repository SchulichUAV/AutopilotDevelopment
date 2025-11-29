import pytest
import sys
import os
import time
import json


script_dir = os.path.abspath('./../..')
sys.path.append(script_dir)

import modules.AutopilotDevelopment.General.Operations.initialize as initialize
import modules.AutopilotDevelopment.General.Operations.mode as mode
import modules.AutopilotDevelopment.Plane.Operations.altitude as altitude
import modules.AutopilotDevelopment.General.Operations.speed as speed
import modules.AutopilotDevelopment.Plane.Operations.system_state as system_state
import modules.AutopilotDevelopment.Plane.Operations.takeoff as takeoff_configuration
import modules.AutopilotDevelopment.General.Operations.battery_data as get_battery
import modules.AutopilotDevelopment.Plane.Operations.waypoint as waypoint
import modules.AutopilotDevelopment.General.Operations.arm as arm

sys.path.append(os.path.abspath('./../'))
from plane import Plane



class TestSITL:
    @pytest.fixture(scope="class", autouse=True)
    def setup_class(cls):
       
        plane = Plane()

        cls.vehicle_connection = plane.vehicle_connection
        
        # Validate connection
        if cls.vehicle_connection is None:
            pytest.fail("Failed to establish vehicle connection")
        
        yield
        
    def test_change_altitude(self):
        """Test changing altitude in guided mode."""
        mode.set_mode(self.vehicle_connection, 15)
        altitude.set_current_altitude(self.vehicle_connection, 90)
    
    def test_change_speed(self):
        """Test changing airspeed in guided mode."""
        mode.set_mode(self.vehicle_connection, 15)
        speed.set_guided_airspeed(self.vehicle_connection, 90)
    
    def test_retrieve_state(self):
        for _ in range(3):
            sys_status = system_state.receive_system_status(self.vehicle_connection)
            print(sys_status)
            
            gps_raw = system_state.receive_gps_raw(self.vehicle_connection)
            print(gps_raw)
            
            param_value = system_state.receive_param_request_read(
                self.vehicle_connection, 'TKOFF_ALT'
            )
            if param_value is not None:
                print(f"TAKEOFF ALT: {param_value}")
            else:
                print("Failed to receive parameter value.")
            
            time.sleep(5)
    
    def test_takeoff(self):
        takeoff_configuration.set_takeoff_altitude(self.vehicle_connection, 100)
        takeoff_configuration.set_takeoff_angle(self.vehicle_connection, 20)
        time.sleep(1)
        
        arm.arm(self.vehicle_connection)
        time.sleep(1)
        
        mode.set_mode(self.vehicle_connection, 13)
    
    def test_battery(self):
        for _ in range(5):
            get_battery.receive_battery_data(self.vehicle_connection)
            time.sleep(1)
    
    def test_waypoint(self):
        mode.set_mode(self.vehicle_connection, 15)
        waypoint.set_waypoint(self.vehicle_connection, 51.100000, 2.000000, 100)

