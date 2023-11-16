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
LTR308_MAIN_CTRL		= 0x00                     
LTR308_ALS_MEAS_RATE	= 0x04                   
LTR308_ALS_GAIN			= 0x05                     
LTR308_PART_ID			= 0x06                     
LTR308_MAIN_STATUS		= 0x07                   
LTR308_ALS_DATA_0		= 0x0D                     
LTR308_ALS_DATA_1		= 0x0E                     
LTR308_ALS_DATA_2		= 0x0F                     
LTR308_INT_CFG			= 0x19                     
LTR308_INT_PST 			= 0x1A                     
LTR308_ALS_THRES_UP_0	= 0x21                   
LTR308_ALS_THRES_UP_1	= 0x22                   
LTR308_ALS_THRES_UP_2	= 0x23                   
LTR308_ALS_THRES_LOW_0	= 0x24                 
LTR308_ALS_THRES_LOW_1	= 0x25                 
LTR308_ALS_THRES_LOW_2	= 0x26                 
                                                                      
MODE_ALS_Range1			= 0x00 
MODE_ALS_Range3			= 0x01
MODE_ALS_Range6			= 0x02
MODE_ALS_Range9			= 0x03 
MODE_ALS_Range18		= 0x04
                                             
ALS_RANGE_1				= 1                          
ALS_RANGE_3 			= 3                          
ALS_RANGE_6 			= 6                          
ALS_RANGE_9 			= 9                          
ALS_RANGE_18			= 18                         
                                             
ALS_RESO_MEAS			= 0x22                       
WIN_FAC					= 1                            
WAKEUP_DELAY			= 10   
         
als_gainrange = 3
intg_val = 1


# Bind it to the external interrupt pin。
class ltr308(object):
    i2c_dev = None
    address = None
    int_pin = None

    def init(self, slave_address):
        self.address = slave_address
        self.i2c_dev = I2C(LTR308_I2C_DEV, I2C.STANDARD_MODE)
        self.int_pin = Pin(ALS_PIN, Pin.IN, Pin.PULL_PU, 0)  # Interrupt pin
        self.enable(1)        
        self.sensor_init()
        pass

    def get_lux(self):
        luxval0 = self.read_data(LTR308_ALS_DATA_0, 1)
        luxval1 = self.read_data(LTR308_ALS_DATA_1, 1)
        luxval2 = self.read_data(LTR308_ALS_DATA_2, 1)
        luxval = (luxval2[0] * 256 * 256) + (luxval1[0] * 256) + luxval0[0]
        if luxval == 0:
            luxval_int = 0
        else:
            luxval_int = luxval * 8 * WIN_FAC / als_gainrange / intg_val / 10
        return luxval_int

    def enable(self,enable):
        readdata = self.read_data(LTR308_MAIN_CTRL, 1)
        if enable == 1:
            regdata = readdata[0] | 0x02
        else:
            regdata = readdata[0] & 0xfd
        self.write_data(LTR308_MAIN_CTRL, regdata)
        utime.sleep_ms(WAKEUP_DELAY)

    def read_data(self, regaddr, datalen, debug=False):
        r_data = [0x00 for _ in range(datalen)]
        r_data = bytearray(r_data)
        reg_addres = bytearray([regaddr])
        self.i2c_dev.read(self.address, reg_addres, 1, r_data, datalen, 1)
        ret_data = list(r_data)
        if debug is True:
            print('ltr308 read_data reg=0x%x value=0x%x'%(regaddr,ret_data[0]))
        return ret_data

    def write_data(self, regaddr, data, debug=False):
        w_data = bytearray([regaddr, data])
        # Temporarily put the address to be transmitted in the data bit
        self.i2c_dev.write(self.address, bytearray(0x00), 0, bytearray(w_data), len(w_data))
        if debug is True:
            print('ltr308 write_data reg=0x%x value=0x%x'%(regaddr,data))

    def sensor_init(self):
        self.write_data(LTR308_ALS_GAIN, MODE_ALS_Range3)
        self.write_data(LTR308_ALS_MEAS_RATE, ALS_RESO_MEAS)

    def processing_data(self):
        lux = self.get_lux()
        print('ltr308 processing_data lux=%d'%(lux))
        pass

    def intfucn(self):
        value = self.int_pin.read()
        print('ltr308 int value=%d event'%(value))

    def exti_init(self):
        self.int = ExtInt(ALS_INT, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, self.intfucn)
        self.int.enable()

    def exti_processing_data(self):
        value = self.int_pin.read()
        if value == 1:  # Interrupt signal detected
            self.processing_data()
            return 1
        else:
            return 0

def ltr308_thread(state, delay, retryCount):
    dev = ltr308()
    dev.init(LTR308_ADDRESS)
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
    _thread.start_new_thread(ltr308_thread, (0, 1000, 30))
