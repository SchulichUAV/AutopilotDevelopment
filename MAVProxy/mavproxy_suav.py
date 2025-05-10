import socket
import time
import math

from MAVProxy.modules.lib import mp_module

class suav(mp_module.MPModule):
    def __init__(self, mpstate):
        """Initialise module"""
        super(suav, self).__init__(mpstate, "suav", "SUAV information extraction")
        self.emit_interval = 0.1
        self.last_emitted = time.time()
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

        self.lat = 0
        self.lon = 0
        self.rel_alt = 0
        self.alt = 0

        self.pitch = 0
        self.yaw = 0
        self.roll = 0

        self.dlat = 0
        self.dlon = 0
        self.dalt = 0
        self.heading = 0

        self.airspeed = 0
        self.groundspeed = 0
        self.throttle = 0
        self.climb = 0

        self.num_satellites = 0
        self.position_uncertainty = 0
        self.alt_uncertainty = 0
        self.speed_uncertainty = 0
        self.heading_uncertainty = 0

        self.flight_mode = 0

        self.battery_voltage = 0
        self.battery_current = 0
        self.battery_remaining = 0

    def idle_task(self):
        '''called rapidly by mavproxy'''
        now = time.time()
        if now-self.last_emitted > self.emit_interval:
            self.last_emitted = now

            if self.lat != 0:
                self.send_data()

    def mavlink_packet(self, m):
        '''handle mavlink packets'''
        if self.settings.target_system == 0 or self.settings.target_system == m.get_srcSystem():
            if m.get_type() == 'GLOBAL_POSITION_INT':
                (lat, lon, alt, relative_alt, dlat, dlon, dalt, heading) = (m.lat*1.0e-7, m.lon*1.0e-7, m.alt/1000,
                                                                                    m.relative_alt/1000, m.vx/100, m.vy/100, m.vz/100, m.hdg/100)
                self.lat = lat # Latitude
                self.lon = lon # Longitude
                self.alt = alt # Altitude (MSL)
                self.rel_alt = relative_alt # Altitude above home
                self.dlat = dlat # Ground X speed (Latitude, positive north)
                self.dlon = dlon # Ground y Speed (Longitude, positive east)
                self.dalt = dalt # Ground Z speed (Altitude, postive down)
                self.heading = heading # Vehicle heading, yaw angle
            
            elif m.get_type() == 'ATTITUDE':
                (roll, pitch, yaw) = (m.roll, m.pitch, m.yaw)
                self.roll = roll * 180 / math.pi # Roll (-pi, pi)
                self.pitch = pitch * 180 / math.pi # Pitch (-pi, pi)
                self.yaw = yaw * 180 / math.pi # Yaw (-pi, pi)
            elif m.get_type() == 'GPS_RAW_INT':
                (num_satellites, position_uncertainty, alt_uncertainty, speed_uncertainty, heading_uncertainty) = (m.satellites_visible, 
                                                                                                                        m.h_acc, m.v_acc, m.vel_acc, m.hdg_acc)
                self.num_satellites = num_satellites # Number of visible satellites
                self.position_uncertainty = position_uncertainty # Position uncertainty (mm)
                self.alt_uncertainty = alt_uncertainty # Altitude uncertainty (mm)
                self.speed_uncertainty = speed_uncertainty # Speed uncertainty (mm)
                self.heading_uncertainty = heading_uncertainty # Heading uncertainty (mm)

            elif m.get_type() == 'VFR_HUD':
                self.airspeed = m.airspeed
                self.groundspeed = m.groundspeed
                self.throttle = m.throttle
                self.climb = m.climb
            
            elif m.get_type() == 'HEARTBEAT':
                self.flight_mode = m.custom_mode
            
            elif m.get_type() == 'SYS_STATUS':
                self.battery_voltage = m.voltage_battery
                self.battery_current = m.current_battery
                self.battery_remaining = m.battery_remaining
            
    def send_data(self):
        t = time.time()
        heartbeat_data = (t, self.lon, self.lat, self.rel_alt, self.alt, self.roll, self.pitch, self.yaw, self.dlat, self.dlon, self.dalt, self.heading,
                self.airspeed, self.groundspeed, self.throttle, self.climb, self.num_satellites, self.position_uncertainty, self.alt_uncertainty, self.speed_uncertainty, 
                          self.heading_uncertainty, self.flight_mode, self.battery_voltage, self.battery_current, self.battery_remaining)

        heartbeat_message = f"{heartbeat_data}".encode()
        self.sock.sendto(heartbeat_message, ("127.0.0.1", 5005))

    def encode_message(self, items):
        message = ""
        for index, item in enumerate(items):
            message += str(item)
            if index != len(items) - 1:
                message += ","
        return message.encode()

def init(mpstate):
    '''initialise module'''
    return suav(mpstate)
