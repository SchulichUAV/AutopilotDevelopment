def mission_acknowledge(vehicle_connection):
    # PROMISES: status of mission_ack (rec or not rec) 
    # REQUIRES: vehicle connection
    
    vehicle_connection.mav.mission_ack_send(
        target_system=vehicle_connection.target_system, 
        target_component=vehicle_connection.target_component,
        mav_mission_result=0, # MAV_MISSION_ACCEPTED
        mav_mission_type=0, # MAV_MISSION_TYPE_MISSION (items are mission commands for main mission)
        opaque_id=0 # 0 since plan ids aren't supported (multiple mission uploads to vehicle)
    )

    msg = vehicle_connection.recv_match(type='MISSION_ACK', blocking=True, timeout=5)

    if msg:
        print("Received MISSION_ACK!")
    else:
        print("No MISSION_ACK response received!")
