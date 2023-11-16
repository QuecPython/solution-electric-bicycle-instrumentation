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

#lowactive: 0 means en
class gpio_en(object):
    def enable(self):
        self.pin.write(self.en_value)
        print('gpio=%s en=%d'%(self.name,self.en_value))

    def disable(self):
        self.pin.write(self.dis_value)
        print('gpio=%s en=%d'%(self.name,self.en_value))

    def __init__(self, pin, low_active, name):
        self.name = name        
        self.pin = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        if low_active == 0:
            self.en_value = 1
            self.dis_value = 0
        else:
            self.en_value = 0
            self.dis_value = 1           

if __name__ == "__main__":
    netmode_en = gpio_en(Pin.GPIO14, 0, "netmode_en")
    netmode_en.enable()
    #boot_5v_en = gpio_en(BOOST_5V_EN_PIN, 0, "boot_5v_en")
    #audio_pa_en = gpio_en(AUDIO_PA_EN_PIN, 0, "audio_pa_en")
    #icn6211_en = gpio_en(ICN6211_EN_PIN, 0, "icn6211_en")
    #gps_en = gpio_en(GPS_EN_PIN, 0, "gps_en")
    #charger_en = gpio_en(CHARGER_EN_PIN, 0, "charger_en")
