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

import utime
from usr.drivers.LB2209conf import *

#[vadc,vlux] vadc from low to high
adc2lux = [[1000, 500],[1100, 600],[1200, 700],[1300, 800],[1400, 900],
           [1500,1000],[1600,1100],[1700,1200],[1800,1300],[1900,1400]]

def voltage_to_light(adc):
    i=0
    while i<len(adc2lux):
        if adc < adc2lux[0][0]:
            lux = adc2lux[0][1]
            break
        else:
            if adc < adc2lux[i][0]:
                lux = adc2lux[i-1][1] + (adc - adc2lux[i-1][0])*(adc2lux[i][1]-adc2lux[i-1][1])/(adc2lux[i][0]-adc2lux[i-1][0])
                break
        if i == len(adc2lux)-1:
            lux=adc2lux[i][1]
        i=i+1
    print('adc is %d light is %d'%(adc,lux))
    return lux

def get_light():
    AdcDevice = ADC()
    vadc = AdcDevice.read(LIGHT_ADC)
    vlux = voltage_to_light(vadc)
    return vlux

if __name__ == "__main__":
   for i in range(100):
        i = i+1
        light = get_light()
        utime.sleep(1) 
