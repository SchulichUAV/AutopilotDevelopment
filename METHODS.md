# Methods and Properties

- [vehicle_connection.mav methods](#methods)
  - [.param_set_send()](#param_set_send)
  - [.send()](#send)
  - [.command_long_send()](#command_long_send)
  - [.mission_ack_send()](#mission_ack_send)
  - [.param_request_read_send()](#param_request_read_send)

---

## vehicle_connection.mav methods

### `.param_set_send()`

**Description**: Sends a parameter set request to the target system and component.

**Template**:
```python
vehicle_connection.mav.param_set_send(
    target_system=<TARGET_SYSTEM>,
    target_component=<TARGET_COMPONENT>,
    param_id=<PARAM_ID_FROM_LIST>,  # Parameter name as bytes
    param_value=<PARAM_VALUE>,  # Desired parameter value
    param_type=<PARAM_TYPE_FROM_LIST>  # MAVLink parameter type
)
```
**Example**:
```python
vehicle_connection.mav.param_set_send(
    target_system=vehicle_connection.target_system,
    target_component=vehicle_connection.target_component,
    param_id=b'TKOFF_LVL_PITCH',
    pitch_angle=15,
    param_type=mavutil.mavlink.MAV_PARAM_TYPE_UINT32
)
```
---
### `.send()`
**Description**: Sends a generic MAVLink message to the target system. The specific message to be sent depends on the use case and the MAVLink dialect being used.

**Template**:

```python
mavlink_message = dialect.<MAVLink_Message_Type>(
    target_system=<TARGET_SYSTEM>,
    target_component=<TARGET_COMPONENT>,
    sequence_number=<SEQUENCE_NUMBER>,  # Sequence number for the message
    coordinate_frame=<COORDINATE_FRAME_FROM_LIST>,  # Coordinate system (if applicable)
    command=<COMMAND_FROM_LIST>,  # MAVLink command (if applicable)
    current=<CURRENT>,  # Whether the command is current (specific to the message type)
    autocontinue=<AUTOCONTINUE>,  # Autocontinue to next command
    hold_time=<HOLD_TIME>,  # Hold time (specific to the message type)
    acceptance_radius=<ACCEPTANCE_RADIUS>,  # Acceptance radius (if applicable)
    pass_radius=<PASS_RADIUS>,  # Pass-through radius (if applicable)
    yaw=<YAW>,  # Desired yaw (if applicable)
    latitude=<LATITUDE>,  # Latitude * 1e7 (if applicable)
    longitude=<LONGITUDE>,  # Longitude * 1e7 (if applicable)
    altitude=<ALTITUDE>  # Altitude (if applicable)
)

vehicle_connection.mav.send(mavlink_message)
```

**Example**:

```python
mavlink_message = dialect.MAVLink_mission_item_int_message(
    target_system=vehicle_connection.target_system,
    target_component=vehicle_connection.target_component,
    sequence_number=0,  # Sequence number of the message
    coordinate_frame=dialect.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # Coordinate frame
    command=dialect.MAV_CMD_NAV_WAYPOINT,  # Command (optional, depends on use case)
    current=2,  # Whether this is the current command (specific to the message type)
    autocontinue=0,  # Autocontinue to next command
    hold_time=0,  # Hold time at position (specific to the message type)
    acceptance_radius=0,  # Radius for acceptance (specific to the message type)
    pass_radius=0,  # Pass-through radius (specific to the message type)
    yaw=0,  # Desired yaw
    latitude=int(latitude * 1e7),  # Latitude in degrees * 1e7
    longitude=int(longitude * 1e7),  # Longitude in degrees * 1e7
    altitude=altitude  # Altitude in meters
)
vehicle_connection.mav.send(mavlink_message)
```

---
### `command_long_send()`
**Description**: Sends a COMMAND_LONG MAVLink message to the target.

**Template:**

```python
vehicle_connection.mav.command_long_send(
    target_system=<TARGET_SYSTEM>,
    target_component=<TARGET_COMPONENT>,
    command=<COMMAND_FROM_LIST>,  # MAVLink command ID or enum
    confirmation=<CONFIRMATION>,  # 0 for first transmission, >0 for retries
    param1=<PARAM1>,  # Command-specific parameter
    param2=<PARAM2>,
    param3=<PARAM3>,
    param4=<PARAM4>,
    param5=<PARAM5>,  # Latitude or 0 to use current position
    param6=<PARAM6>,  # Longitude or 0 to use current position
    param7=<PARAM7>   # Altitude or command-specific parameter
)
```
**Example:**

```python
vehicle_connection.mav.command_long_send(
    vehicle_connection.target_system,
    vehicle_connection.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,
    0, 0, 0, 0,
    0, 0,
    takeoff_height
)
```
---
### `.mission_ack_send()`
**Description**: Acknowledges the receipt of a mission message.

**Template**:

```python
vehicle_connection.mav.mission_ack_send(
    target_system=<TARGET_SYSTEM>,
    target_component=<TARGET_COMPONENT>,
    mav_mission_result=<MISSION_RESULT>,  # Mission status (e.g., MAV_MISSION_ACCEPTED)
    mav_mission_type=<MISSION_TYPE>,  # Type of mission (e.g., MAV_MISSION_TYPE_MISSION)
    opaque_id=<OPAQUE_ID>  # Plan ID if supported, else 0
)
```
**Example**:

```python
vehicle_connection.mav.mission_ack_send(
    target_system=vehicle_connection.target_system,
    target_component=vehicle_connection.target_component,
    mav_mission_result=0,
    mav_mission_type=0,
    opaque_id=0
)
```
---
### `.param_request_read_send()`
**Description**: Requests a specific parameter value from the target system.

**Template**:

```python
vehicle_connection.mav.param_request_read_send(
    target_system=<TARGET_SYSTEM>,
    target_component=<TARGET_COMPONENT>,
    param_id=<PARAM_ID_FROM_LIST>,  # Parameter name as bytes
    param_index=<PARAM_INDEX>  # -1 to use param ID, or parameter index
)
```
**Example**:

```python
vehicle_connection.mav.param_request_read_send(
    target_system=vehicle_connection.target_system,
    target_component=vehicle_connection.target_component,
    param_id=param_id_bytes,
    param_index=-1
)
```
---

vehicle_connection methods to now document later
    - .send()
    - .recv_match()
    - .wait_heartbeat()

vehicle_connection (properties) to document later
    - target_system
    - target_component

we're gonna have to make the FROM_LIST items into parameter or command lists
or at least provide like a link to the lists

