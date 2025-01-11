import time

while(1):
    print(vehicle_connection.recv_match(type='BATTERY_STATUS', blocking=True))
    time.sleep(1)