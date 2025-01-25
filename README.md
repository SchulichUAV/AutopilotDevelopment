# MAVLink Autopilot

Interoperability system for integration between custom Ground Control System and autonomous aerial vehicles with ArduPilot. Currently integrated and tested for quadcopter designs. Fixed wing (non-quadplan configurations) are in development). Developed for Schulich Unmanned Aerial Vehicles at the University of Calgary.

## Testing
To run physics simulation on autopilot code, use Software in the Loop (SITL). Documentation: https://ardupilot.org/dev/docs/SITL-setup-landingpage.html.

It is recommended to use a Linux distribution, or install WSL on Windows systems. Clone the ArduPilot repository and run SITL/MAVProxy in the Linux terminal with "sim_vehicle.py --console --map -w". SITL and MAVProxy will start, and will output the simulated vehicle port connection to terminal. Use this port as an input to run this program (main.py). View live vehicle movement and control through any GCS software (Mission Planner, QGroundControl, etc.).

## Operations

### Note: Files in Copter folder is only supported by copter configurations, Plane folder only supports plane operations, and General supports both.

Please see `Development.md` and `Methods.md` for development guidance.