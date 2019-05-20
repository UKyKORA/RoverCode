# BeltControl.py
#
# Description:
#   Code for controlling the offload and excavation belt systems.
#

#
# Revision History:
#   Matt R. 2019-04-20 Initial Version.
#

import time
from roboclaw_3 import Roboclaw


class BeltControl:

    def __init__(self, addr):
        self.act =  Roboclaw(addr, 115200)
        self.currents = [0,0]
        while self.act.Open()==0:
            print("Failed to open actuator comms, trying again.")
            time.sleep(1)
        print("Opened Belt roboclaw to ",addr)

    ############# public methods #############

    def updateCurrents(self):    
        con1 = self.act.ReadCurrents(0x80)
        digCurr = float(con1[1]) / 100
        offCurr = float(con1[2]) / 100
        
        self.currents = [digCurr, offCurr] 
    # method for reading the blet currents
    def readCurrents(self, i):
        return self.currents[i]

    # control the offload belt
    def offload(self, speed):
        speed = self.verify_speed(speed)
        direction = "s"
        if speed <= 1800:
            # move actuator forward
            adjusted_speed = self.translate_value(speed, 1800,0,0,127)
            direction = "b"
        elif speed >= 2200:
            #move actuator backward
            adjusted_speed = self.translate_value(speed, 2200, 4095,0,127)
            direction = "f"
        else :
            #do not move actuator
            direction = "s"
            adjusted_speed = 0

        if direction == "f" :
            self.act.ForwardM1(0x80, int(adjusted_speed))
        elif direction == "b":
            self.act.BackwardM1(0x80, int(adjusted_speed))
        else:
            self.act.ForwardM1(0x80, 0)
        self.updateCurrents()

    # control the digging belt
    def dig(self, speed):
        speed = self.verify_speed(speed)
        direction = "s"
        if speed <= 1800:
            # move actuator forward
            adjusted_speed = self.translate_value(speed, 1800,0,0,127)
            direction = "b"
        elif speed >= 2200:
            #move actuator backward
            adjusted_speed = self.translate_value(speed, 2200, 4095,0,127)
            direction = "f"
        else :
            #do not move actuator
            direction = "s"
            adjusted_speed = 0

        if direction == "f" :
            self.act.ForwardM2(0x80, int(adjusted_speed))
        elif direction == "b":
            self.act.BackwardM2(0x80, int(adjusted_speed))
        else:
            self.act.ForwardM2(0x80, 0)
        self.updateCurrents()
        ############# private methods #############

    # verifies speed and position
    def verify_speed(self, speed):
        # set maximum speed that the actuator can go
        maximum = 4095

        # cap the speed at the max in either direction
        if speed > maximum:
            speed = maximum
        elif speed < 0:
            speed = 0
        else:
            speed = speed

        return speed

    # translates vale from left range to right range
    def translate_value(self, value, leftMin, leftMax, rightMin, rightMax):
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
        valueScaled = float(value-leftMin)/float(leftSpan)
        return rightMin + (valueScaled * rightSpan)
