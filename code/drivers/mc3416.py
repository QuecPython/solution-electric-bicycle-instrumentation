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
import _thread
from machine import I2C
from machine import Pin
from machine import ExtInt
from usr.drivers.LB2209conf import *
# Rate value
MC3416_128HZ=0
MC3416_256HZ=1
MC3416_512HZ=2
MC3416_1024HZ=5

# Range value
MC3416_2G=0x00
MC3416_4G=0x10
MC3416_8G=0x20
MC3416_16G=0x30
MC3416_12G=0x40

# Mode value
WAKEMODE=1
STANDBYMODE=3

# Interrupt register
IPP_PUSHPULL = 0x40
IPP_OPENDRAIN = 0x00
IAH_ACTIVEHIGH = 0x80
IAH_ACTIVELOW = 0x00


# Bind it to the external interrupt pin。
class mc3416(object):
    i2c_dev = None
    address = None
    int_pin = None

    def init(self, slave_address):
        self.address = slave_address
        self.i2c_dev = I2C(MC3416_I2C_DEV, I2C.STANDARD_MODE)
        self.int_pin = Pin(ACCL_PIN, Pin.IN, Pin.PULL_PU, 0)  # Interrupt pin, which changes according to different hardware connections
        self.sensor_init()
        self.start_sensor()
        pass

    def read_xyz(self):
        data = []
        xyz = [0,0,0]
        for i in range(6):
            r_data = self.read_data(0x0d + i, 1)
            data.append(r_data[0])
        xyz[0] = data[1]*256 + data[0]
        xyz[1] = data[3]*256 + data[2]
        xyz[2] = data[5]*256 + data[4]
        print(data)
        return xyz

    def setShakeParameters(self,thr,p2pduration,cnt):
        regdata = thr&0xff
        self.write_data(0x46, regdata)
        regdata = (thr&0xff00)>>8
        self.write_data(0x47, regdata)                
        regdata = p2pduration&0xff
        self.write_data(0x48, regdata)
        if cnt > 7:
            cnt = 7
        regdata = ((p2pduration&0xff00)>>8|(cnt<<4))
        self.write_data(0x49, regdata)

    def setAnymotionParameters(self,thr,debounce):
        regdata = thr&0xff
        self.write_data(0x43, regdata)
        regdata = (thr&0xff00)>>8
        self.write_data(0x44, regdata)                
        regdata = debounce       
        self.write_data(0x45, regdata)

    def setTiltParameters(self,thr,debounce):
        regdata = thr&0xff
        self.write_data(0x40, regdata)
        regdata = (thr&0xff00)>>8
        self.write_data(0x41, regdata)                
        regdata = debounce       
        self.write_data(0x42, regdata)

    def setIntsource(self,anymotion, tilt , shake, flip, tilt35, acq, autoclr):
        regdata = (tilt|
				(flip<<1)|
				(anymotion<<2)|
				(shake<<3)|
				(tilt35<<4)|
				(autoclr<<6)|
				(acq<<7))
        self.write_data(0x6, regdata)

    def setMotionctrl(self,anymotion, tiltflip , shake, tilt35):
        regdata = (tiltflip|
				(anymotion<<2)|
				(shake<<3)|
				(tilt35<<4))
        self.write_data(0x9, regdata)

    def setPowermode(self,mode):
        if mode == 1:
            regdata = 0x1
        else:
            regdata = 0x3
        regdata = regdata | IPP_PUSHPULL | IAH_ACTIVELOW
        self.write_data(0x07, regdata)

    def setRate(self,rate):        
        regdata = rate
        self.write_data(0x08, regdata)
 
    def setRangelpf(self,range):
        regdata = 0x09|range
        self.write_data(0x20, regdata)

    def reset(self,slave_address):
        self.sensor_reset
        pass

    def read_data(self, regaddr, datalen, debug=False):
        r_data = [0x00 for _ in range(datalen)]
        r_data = bytearray(r_data)
        reg_addres = bytearray([regaddr])
        self.i2c_dev.read(self.address, reg_addres, 1, r_data, datalen, 1)
        ret_data = list(r_data)
        if debug is True:
            print('mc3413 read_data reg=0x%x value=0x%x'%(regaddr,ret_data[0]))
        return ret_data

    def write_data(self, regaddr, data, debug=False):
        w_data = bytearray([regaddr, data])
        # Temporarily put the address to be transmitted in the data bit
        self.i2c_dev.write(self.address, bytearray(0x00), 0, bytearray(w_data), len(w_data))
        if debug is True:
            print('mc3413 write_data reg=0x%x value=0x%x'%(regaddr,data))

    def sensor_init(self):
        self.setPowermode(STANDBYMODE)
        self.setRate(MC3416_1024HZ)
        self.setRangelpf(MC3416_8G)

    def start_sensor(self):
        self.setAnymotionParameters(0x2aa,0x20)
        self.setShakeParameters(0xaaa,0x555,0x1)
        self.setMotionctrl(1,0,1,0)
        self.setIntsource(0,0,1,0,0,0,1)
        self.setPowermode(WAKEMODE)
        self.exti_init()

    def processing_data(self):
        xyz = self.read_xyz()
        print('mc3413 read_data x=%d y=%d z=%d'%(xyz[0], xyz[1], xyz[2]))
        pass

    def intfucn(self):
        value = self.int_pin.read()
        print('mc3413 int value=%d event'%(value))

    def exti_init(self):
        self.int = ExtInt(ACCL_INT, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, self.intfucn)
        self.int.enable()

    def exti_processing_data(self):
        value = self.int_pin.read()
        if value == 1:  # Interrupt signal detected
            self.processing_data()
            return 1
        else:
            return 0

# Parameter description
# retryCount: number of reads
def mc3416_thread(state, delay, retryCount):
    dev = mc3416()
    dev.init(MC3416_ADDRESS)
    while True:
        if state == 1:
            if dev.exti_processing_data() == 1:
                retryCount -= 1
        elif state == 0:
            dev.processing_data()
            utime.sleep_ms(delay)
            retryCount -= 1
        if retryCount == 0:
            break
    print("detection end exit")

if __name__ == "__main__":
    _thread.start_new_thread(mc3416_thread, (0, 1000, 100))
