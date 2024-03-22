# MAVLink Autopilot

Interoperability system for integration between custom Ground Control System and autonomous aerial vehicles with ArduPilot. Currently integrated and tested for quadcopter designs. Developed for Schulich Unmanned Aerial Vehicles at the University of Calgary.

## Operations
initialize.py - Establishes and verifies the connection to the vehicle.<br>
arm.py - Provides methods to arm and disarm the aerial vehicle.<br>
takeoff.py - Allows the vehicle to takeoff to a target altitude (relative to home altitude)<br>
mode.py - Switches flight modes<br>
waypoint.py - Flies to a specified waypoint relative to the current position, or through geo-coordinates<br>

## Simple Terminal Interface
main.py - Simple terminal interface to trigger Autopilot commands.

## Testing
To run physics simulation on autopilot code, use Software in the Loop (SITL). Documentation: https://ardupilot.org/dev/docs/SITL-setup-landingpage.html.

It is recommended to use a Linux distribution, or install WSL on Windows systems. Clone the ArduPilot repository and run SITL/MAVProxy in the Linux terminal with "sim_vehicle.py". SITL and MAVProxy will start, and will output the simulated vehicle port connection to terminal. Use this port as an input to run this program (main.py). View live vehicle movement and control through any GCS software (Mission Planner, QGroundControl, etc.).
