# Development Overview

## Purpose

### Flight Computer & Electronics

This repository is focused on developing flight control endpoints for a Flask server running on the flight computer (Raspberry Pi). The Raspberry Pi will support all embedded systems on the drone, including:
- Imaging and camera systems
- Payload release mechanisms
- Battery monitoring
- External sensor systems (e.g., Lidar)

Once flight commands are finalized here, they will be ported to our electronics repository for integration. The purpose of this isolated repository is to facilitate initial development and testing of flight systems throughout the year in preparation for competition.

### Why Use This Alongside Mission Planner GCS?

Standard missions and waypoint management will be handled by Mission Planner, which also allows us to create geofences to stay within competition boundaries. This repository's custom flight control endpoints will integrate with our Ground Control System (GCS) to support additional state monitoring and payload drop capabilities. Key functionalities include:
- Pulling battery status and GPS information for display on our GCS
- Accessing GPS uncertainties for enhanced location accuracy and algorithms
- Executing flight to drop coordinates identified by the convolutional neural network
- Determining optimal payload release positions for accurate targeting

### MAVLink

Instead of direct control over each flight surface (e.g., props, ailerons, rudders), we use MAVLink with ArduPilot for sending commands. This is done using Pymavlink (the Python MAVLink library), which simplifies flight control without requiring deep aerodynamic knowledge. Basic flight concepts are still helpful, and Pymavlink enables us to send commands and retrieve information efficiently.

## Development

### Getting Started Tips

Our experience with MAVLink is evolving, and we rely on its documentation along with SITL (Software in the Loop) for testing. There are four main MAVLink functions you'll need to use:
1. **Setting Parameters**: Single configurations (key-value pairs) used by ArduPilot.
2. **Commands**: Used to control vehicle state or instruct specific actions.
3. **Requested Information Retrieval**: Queries for specific data from the flight controller.
4. **Packet Information Retrieval**: Accesses periodic data sent automatically by the controller.

Always check for an existing parameter before writing a new command. Parameters can be adjusted in-flight and are generally simpler to implement.

#### Setting `Parameters`

Setting parameters is straightforward. Refer to Pymavlink’s documentation or existing code examples, such as `Plane/Operations/takeoffConfiguration.py`. The `param_set_send` command can be used to change specific parameters by specifying a byte array for the parameter and a new value.

#### Writing `Commands`

Commands to control vehicle state are prefixed with `MAV_` in MAVLink documentation and sent with `COMMAND_INT` or `COMMAND_LONG`:
- **`COMMAND_LONG`**: For commands without specific positioning (latitude, longitude, altitude).
- **`COMMAND_INT`**: For commands with precise positioning.

For example, `General/Operations/arm.py` uses `COMMAND_LONG` to arm or disarm the vehicle.

#### Writing `Requested Information Retrieval` Requests

These requests query specific non-periodic data from the flight controller. Locate the MAVLink command needed, then use `_send` to retrieve the information.

#### Writing `Packet Information Retrieval` Queries

Periodic data packets, like heartbeats, can be queried directly. For instance, `General/Operations/waypoint_data.py` uses the `recv_match` function to read required data from the vehicle connection.

### Repository Structure

The repository is organized into three main folders: `Copter`, `Plane`, and `General`. 
- **General**: Code supporting all vehicle types (copter and plane).
- **Plane**: Code specific to planes, potentially pulling from `General`.
- **Copter**: Code specific to copters, potentially pulling from `General`.

#### Operations

The `Operations` folder contains Pymavlink commands for querying, requesting, and commanding the vehicle.

#### TestScripts

Scripts in `TestScripts` verify the functionality of Mavlink commands in `Operations`. In the future, these could be converted to a unit testing suite for verifying ACKs.

#### ServerScripts

`ServerScripts` contain Flask server scripts allowing Mavlink commands to be triggered via API requests from our GCS, typically developed towards the end of the cycle, close to competition.

### Testing

Rigorous testing is crucial to ensure safety-critical flight control software functions as expected. Schulich UAV’s two main testing methods are:
- **SITL**: A physics simulation mimicking various aerial vehicles, allowing localhost testing of flight responses. Setup involves either an Ubuntu VM or WSL on Windows, with documentation available in Google Docs.
- **Branching and PRs**: Avoid merging directly into `main`. Code reviews by a technical lead ensure reliability before merging into the mainline.
