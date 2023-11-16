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

from machine import I2C
from machine import Pin
from misc import ADC
from usr.drivers.LB2209conf import *

#icn6211 self test color bar mode add to init list before 09 reg
#[0x14, 0x43],[0x2a, 0x49],
#weihui
LCD0_ADC  = 1000
LCD0_INIT = [[0x20, 0x20],[0x21, 0xE0],[0x22, 0x13],[0x23, 0x28],[0x24, 0x30],
             [0x25, 0x28],[0x26, 0x00],[0x27, 0x0d],[0x28, 0x01],[0x29, 0x1f],
             [0x34, 0x80],[0x36, 0x28],[0x86, 0x29],[0xB5, 0xA0],[0x5C, 0xFF],             
             [0x2A, 0x01],[0x56, 0x90],[0x6B, 0x71],[0x69, 0x24],[0x10, 0x20],             
             [0x11, 0x88],[0xB6, 0x20],[0x51, 0x20],[0x1c, 0x44],[0x1d, 0x44],[0x09, 0x10]]
#lcd1 default=lcd0
LCD1_ADC  = 1000
LCD1_INIT = [[0x20, 0x20],[0x21, 0xE0],[0x22, 0x13],[0x23, 0x28],[0x24, 0x30],
             [0x25, 0x28],[0x26, 0x00],[0x27, 0x0d],[0x28, 0x01],[0x29, 0x1f],
             [0x34, 0x80],[0x36, 0x28],[0x86, 0x29],[0xB5, 0xA0],[0x5C, 0xFF],             
             [0x2A, 0x01],[0x56, 0x90],[0x6B, 0x71],[0x69, 0x24],[0x10, 0x20],             
             [0x11, 0x88],[0xB6, 0x20],[0x51, 0x20],[0x1c, 0x44],[0x1d, 0x44],[0x09, 0x10]]
#lcd2 default=lcd0
LCD2_ADC  = 1000
LCD2_INIT = [[0x20, 0x20],[0x21, 0xE0],[0x22, 0x13],[0x23, 0x28],[0x24, 0x30],
             [0x25, 0x28],[0x26, 0x00],[0x27, 0x0d],[0x28, 0x01],[0x29, 0x1f],
             [0x34, 0x80],[0x36, 0x28],[0x86, 0x29],[0xB5, 0xA0],[0x5C, 0xFF],             
             [0x2A, 0x01],[0x56, 0x90],[0x6B, 0x71],[0x69, 0x24],[0x10, 0x20],             
             [0x11, 0x88],[0xB6, 0x20],[0x51, 0x20],[0x1c, 0x44],[0x1d, 0x44],[0x09, 0x10]]

#adc center value +-delta means this lcd param
LCD_ADC2INIT = [[LCD0_ADC,LCD0_INIT],[LCD1_ADC,LCD1_INIT],[LCD2_ADC,LCD2_INIT]]
ADC_DELTA = 50
#id reg
DEVICE_ID_REG = 0x0
VENDOR_ID_REG = 0x1

# Bind it to the external interrupt pin。
class icn6211(object):
    i2c_dev = None
    address = None
    int_pin = None

    def init(self, slave_address):
        self.address = slave_address
        self.i2c_dev =  I2C(ICN6211_I2C_DEV, I2C.STANDARD_MODE)
        self.en_pin = Pin(ICN6211_EN_PIN, Pin.OUT, Pin.PULL_DISABLE, 0)         
        pass

    def read_data(self, regaddr, datalen, debug=False):
        r_data = [0x00 for _ in range(datalen)]
        r_data = bytearray(r_data)
        reg_addres = bytearray([regaddr])
        self.i2c_dev.read(self.address, reg_addres, 1, r_data, datalen, 1)
        ret_data = list(r_data)
        if debug is True:
            print('eta6965 read_data reg=0x%x value=0x%x'%(regaddr,ret_data[0]))
        return ret_data

    def write_data(self, regaddr, data, debug=False):
        w_data = bytearray([regaddr, data])
        # Temporarily put the address to be transmitted in the data bit
        self.i2c_dev.write(self.address, bytearray(0x00), 0, bytearray(w_data), len(w_data))
        if debug is True:
            print('eta6965 write_data reg=0x%x value=0x%x'%(regaddr,data))

    def get_id(self):
        deviceid = self.read_data(DEVICE_ID_REG, 1)
        vendorid = self.read_data(VENDOR_ID_REG, 1)
        print('eta6965 device=0x%x vendor=0x%x'%(deviceid[0],vendorid[0]))        
        pass

    def lcd_on(self):
        self.en_pin.write(1)
        self.lcd_select()
        self.get_id()        
        self.init_cmd()   
        #self.lcd_test()
        pass

    def lcd_off(self):
        self.en_pin.write(0)
        pass

    def lcd_test(self):
        self.write_data(0x88, 0x80)
        reg80 = self.read_data(0x80, 1)
        reg81 = self.read_data(0x81, 1)
        print('eta6965 reg80=0x%x reg81=0x%x'%(reg80[0],reg81[0]))       
        pass

    def init_cmd(self):
        cmdlen = len(self.real_init)
        i = 0
        while i < cmdlen:
            self.write_data(self.real_init[i][0], self.real_init[i][1])
            i = i + 1

    def lcd_select(self):
        AdcDevice = ADC()
        vadc = AdcDevice.read(LCD_ADC)
        lcdnum = len(LCD_ADC2INIT)
        print('lcd_select lcd init is 0')
        self.real_init = LCD0_INIT
        i=0
        while i < lcdnum:
            if vadc - LCD_ADC2INIT[i][0] > -50 and vadc - LCD_ADC2INIT[i][0] < 50:
               self.real_init =  LCD_ADC2INIT[i][1]
               print('lcd_select lcd change to %d'%(i))
            i = i+1

if __name__ == "__main__":
    dev = icn6211()
    dev.init(ICN6211_ADDRESS)
    dev.lcd_on()
    #dev.lcd_off()