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
import sys_bus


#irqtype: 0-rising   1-falling
class gpio_in_led(object):
    def intfucn(self, args):
        gpionum=args[0]
        irqtype=args[1]
        #need add msg to main here
        print('led=%s off=%d'%(self.name,irqtype))
        sys_bus.publish('LED_EVENT', [self.name, irqtype == 0])

    def __init__(self, pin, int, name):
        self.name = name
        self.pin = Pin(pin, Pin.IN, Pin.PULL_PU, 0)
        self.int = ExtInt(int, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, self.intfucn)
        self.int.enable()
        pass

if __name__ == "__main__":
    led10 = gpio_in_led(Pin.GPIO10, ExtInt.GPIO10, "led10")
    led13 = gpio_in_led(Pin.GPIO13, ExtInt.GPIO13, "led13")
    #l_led = gpio_in_led(L_LED_PIN, L_LED_INT, "l_led")    
    #a_led = gpio_in_led(A_LED_PIN, A_LED_INT, "a_led")
    #n_led = gpio_in_led(N_LED_PIN, N_LED_INT, "n_led")
    #f_led = gpio_in_led(F_LED_PIN, F_LED_INT, "f_led")
    #r_led = gpio_in_led(R_LED_PIN, R_LED_INT, "r_led")
     