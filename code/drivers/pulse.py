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
import utime

#boot_low: no pulse status 0 means low 1 means high
class gpio_pulse(object):
    def set(self, mdelay, cnt):
        self.cnt = cnt 
        while self.cnt > 0:
            self.cnt = self.cnt - 1
            self.pin.write(self.dis_value)
            utime.sleep_ms(mdelay)
            self.pin.write(self.en_value)
            utime.sleep_ms(mdelay)
        print('pulse set: gpio=%s en=%d delay=%d cnt=%d'%(self.name,self.en_value,mdelay,self.cnt))  

    def clear(self):
        self.cnt = 0
        self.pin.write(self.en_value)
        print('pulse clear: gpio=%s en=%d'%(self.name,self.en_value))

    def __init__(self, pin, boot_low, name):
        self.name = name        
        self.pin = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        if boot_low == 0:
            self.en_value = 1
            self.dis_value = 0
        else:
            self.en_value = 0
            self.dis_value = 1           

if __name__ == "__main__":
    #ap2mcu = gpio_pulse(AP2MCU_PIN, 1, "ap2mcu")
    #ap2mcu.set(100, 1)  
    netmode_en = gpio_pulse(Pin.GPIO14, 1, "netmode_en")
    netstatus_en = gpio_pulse(Pin.GPIO28, 0, "netstatus_en")
    netmode_en.set(1000, 10)
    netstatus_en.set(6000, 2)
