# mission_ack(47) implementation

def mission_acknowledge(vehicle_connection):
    vehicle_connection.mav.mission_ack_send(
            vehicle_connection.target_system, 
            vehicle_connection.target_component,
            0,0,0
        )

    print(f"Sent MISSION_ACK!")
