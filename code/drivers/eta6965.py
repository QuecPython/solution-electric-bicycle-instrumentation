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
from machine import I2C
from machine import Pin
from machine import ExtInt
from usr.drivers.LB2209conf import *

#INT VBUS REG
INT_VBUS_REG  = 0x0a
INT_VBUS_MASK  = 0x80
#INT FAULT REG
INT_FAULT_REG  = 0x09
INT_WDOG_MASK = 0x80
INT_CHG_MASK = 0x30
INT_BOVP_MASK = 0x08
INT_NTC_MASK = 0x07
NTC_BAT_COLD = 0x5
NTC_BAT_HOT = 0x6
#ICHG REG:BIT0-5 fast charge current
ICHG_REG	= 0x02
ICHG_CURR_60 = 0x01             
ICHG_CURR_120 = 0x02
ICHG_CURR_240 = 0x04             
ICHG_CURR_480 = 0x08
ICHG_CURR_960 = 0x10             
ICHG_CURR_1920 = 0x20
ICHG_CURR_420 = ICHG_CURR_60 | ICHG_CURR_120 | ICHG_CURR_240
ICHG_CURR_300 = ICHG_CURR_60 | ICHG_CURR_240 
ICHG_CLEAR_MASK = 0xc0  

#wdog reg bit4-5 00 disable
WDOG_REG      = 0x05
WDOG_EN_40S   = 0x10
WDOG_DISABLE  = 0x00
WDOG_CLEAR_MASK  = 0xcf

# Bind it to the external interrupt pin。
class eta6965(object):
    i2c_dev = None
    address = None
    int_pin = None

    def init(self, slave_address):
        self.address = slave_address
        self.i2c_dev =  I2C(ETA6959_I2C_DEV, I2C.STANDARD_MODE)
        self.en_pin  = Pin(CHARGER_EN_PIN, Pin.OUT, Pin.PULL_DISABLE, 0)  # en pin
        self.int_pin = Pin(CHARGER_PIN, Pin.IN, Pin.PULL_PU, 0)  # Interrupt pin
        self.int = ExtInt(CHARGER_INT, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, self.intfucn)       
        self.set_max_current(ICHG_CURR_300)
        self.en_pin.write(1)
        self.int.enable()                                 
        pass

    def read_reg(self,reg):
        rregdata = self.read_data(reg, 1)

    def set_wdog(self,enable):
        #enable=0 mean disable wdog
        rregdata = self.read_data(WDOG_REG, 1)
        wregdata = (rregdata[0] & WDOG_CLEAR_MASK) | enable
        self.write_data(WDOG_REG, wregdata)

    def set_max_current(self,current):
        #default max prechg current is 180 no need to set
        #set default fastchg current to 420-0x7,480-0x8
        self.set_wdog(WDOG_EN_40S)
        rregdata = self.read_data(ICHG_REG, 1)
        wregdata = (rregdata[0] & ICHG_CLEAR_MASK) | current
        self.write_data(ICHG_REG, wregdata)
        self.set_wdog(WDOG_DISABLE)        

    def intfucn(self):
        #check vbus in
        rregdata = self.read_data(INT_VBUS_REG, 1)
        print('eta6965 int vbus reg=0x%x'%(rregdata[0]))
        if (rregdata[0] & INT_VBUS_MASK) is not 0:
            #maybe need send message to ap
            print('eta6965 int VBUS IN')
        else:
            #maybe need send message to ap
            print('eta6965 int VBUS OUT')
        #check fault   
        rregdata = self.read_data(INT_FAULT_REG, 1)
        print('eta6965 int fault reg=0x%x'%(rregdata[0]))
        if (rregdata[0] & INT_WDOG_MASK) is not 0:
            print('eta6965 int INT_WDOG_MASK')
        if (rregdata[0] & INT_CHG_MASK) is not 0:
            print('eta6965 int INT_CHG_MASK')
        if (rregdata[0] & INT_BOVP_MASK) is not 0:
            print('eta6965 int INT_BOVP_MASK')   
        if (rregdata[0] & INT_NTC_MASK) == NTC_BAT_HOT:
            #maybe need send message to ap
            print('eta6965 int NTC_BAT_HOT')                     
        if (rregdata[0] & INT_NTC_MASK) == NTC_BAT_COLD:
            #maybe need send message to ap            
            print('eta6965 int NTC_BAT_COLD')
        
    def read_data(self, regaddr, datalen, debug=True):
        r_data = [0x00 for _ in range(datalen)]
        r_data = bytearray(r_data)
        reg_addres = bytearray([regaddr])
        self.i2c_dev.read(self.address, reg_addres, 1, r_data, datalen, 1)
        ret_data = list(r_data)
        if debug is True:
            print('eta6965 read_data reg=0x%x value=0x%x'%(regaddr,ret_data[0]))
        return ret_data

    def write_data(self, regaddr, data, debug=True):
        w_data = bytearray([regaddr, data])
        # Temporarily put the address to be transmitted in the data bit
        self.i2c_dev.write(self.address, bytearray(0x00), 0, bytearray(w_data), len(w_data))
        if debug is True:
            print('eta6965 write_data reg=0x%x value=0x%x'%(regaddr,data))

if __name__ == "__main__":
    dev = eta6965()
    dev.init(ETA6965_ADDRESS)
