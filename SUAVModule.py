#!/usr/bin/env python
'''module template'''
import time, math
from pymavlink import mavutil
from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib.mp_settings import MPSetting

class TestModule(mp_module.MPModule):
  def __init__(self, mpstate):
    super(TestModule, self).__init__(mpstate, "test", "test module")
    '''initialisation code'''

  def mavlink_packet(self, m):
    '''handle a mavlink packet'''
    

def init(mpstate):
  '''initialise module'''
  return TestModule(mpstate)  