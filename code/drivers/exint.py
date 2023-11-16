# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
 
#     http://www.apache.org/licenses/LICENSE-2.0
 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from machine import Pin
from machine import ExtInt 

#irqtype: 0-rising   1-falling
class gpio_exint(object):
    def intfucn(self, args):
        gpionum=args[0]
        irqtype=args[1]
        #need add msg to main here
        print('gpio=%s falling=%d'%(self.name,irqtype))         

    def __init__(self, pin, int, name):
        self.name = name
        self.pin = Pin(pin, Pin.IN, Pin.PULL_PU, 0)
        self.int = ExtInt(int, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, self.intfucn)
        self.int.enable()
        pass

if __name__ == "__main__":
    led10 = gpio_exint(Pin.GPIO10, ExtInt.GPIO10, "exint10")
    led13 = gpio_exint(Pin.GPIO13, ExtInt.GPIO13, "exint13")
    #brake = gpio_exint(BRAKE_PIN, BRAKE_INT, "brake")
    #mcu2ap = gpio_exint(MCU2AP_PIN, MCU2AP_INT, "mcu2ap")