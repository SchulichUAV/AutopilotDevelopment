# mission_ack(47) implementation

def mission_acknowledge(vehicle_connection):
    vehicle_connection.mav.mission_ack_send(
        vehicle_connection.target_system, 
        vehicle_connection.target_component,
        0,0,0
    )

    msg = connection.recv_match(type='MISSION_ACK', blocking=True, timeout=5)

    if msg:
        print("Recieved MISSION_ACK!")
    else:
        print("No MISSION_ACK response recieved!")
