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
import osTimer
import sys_bus
from machine import Pin
from machine import ExtInt
from usr.drivers.LB2209conf import *
#irqtype: 0-rising   1-falling
KEY_EVENT_SHORT  = 0
KEY_EVENT_LONG   = 1
KEY_EVENT_DOUBLE = 2
KEY_LONG_PRESS_TIME = 1000
KEY_DOUBLE_MAX_TIME = 400
KEY_DEBOUNCE_TIME = 20

class gpio_key(object):
    def double_timer_cb(self, args):
        if self.up_before_double_timer == 1:
            #self.up_before_double_timer = 0
            self.long_timer.stop()
            self.ts_prev = self.ts_down
            self.tms_prev = self.tms_down
            self.event = KEY_EVENT_SHORT
            print('key=%s event=%d'%(self.name,self.event)) 
            sys_bus.publish('MKEY_EVENT', self.event)

    def long_timer_cb(self, args):
        self.ts_prev = self.ts_down
        self.tms_prev = self.tms_down
        self.event = KEY_EVENT_LONG
        print('key=%s event=%d'%(self.name,self.event))  
        sys_bus.publish('MKEY_EVENT', self.event)

    def intfucn(self, args):
        gpionum=args[0]
        irqtype=args[1]
        
        # down report double hit
        if irqtype == 1:
            self.ts_down = utime.time()
            self.tms_down = utime.ticks_ms()
            self.up_before_double_timer = 0
            #if 60s no key press down, clear tms_prev no double hit
            if self.ts_down-self.ts_prev > 60:
                self.tms_prev = 0
            #double hit  tms_down - tms_prev < 300 report double hit       
            if utime.ticks_diff(self.tms_down,self.tms_prev) < KEY_DOUBLE_MAX_TIME:
                #do not update 2rd down time or three hit will report 2 double hit
                self.double_timer.stop()
                self.long_timer.stop()  
                self.event = KEY_EVENT_DOUBLE
                print('key=%s down=%d event=%d'%(self.name,irqtype,self.event))
                sys_bus.publish('MKEY_EVENT', self.event)
            else:
                self.double_timer.start(KEY_DOUBLE_MAX_TIME, 0, self.double_timer_cb)
                self.long_timer.start(KEY_LONG_PRESS_TIME, 0, self.long_timer_cb)
                #print('key=%s down=%d no event'%(self.name,irqtype))
 
        #up report short hit
        if irqtype == 0:
            tms_up = utime.ticks_ms()
            #wrong key up<20ms 
            if utime.ticks_diff(tms_up,self.tms_down) < KEY_DEBOUNCE_TIME:
                print('press time lower than 20 wrong key')                  
            #long press up>1000 send event in timer cb
            elif utime.ticks_diff(tms_up,self.tms_down) > KEY_LONG_PRESS_TIME:
                #print('key=%s long press up no event'%(self.name))
                pass
            #short hit type1 300<up<1000 report
            elif utime.ticks_diff(tms_up,self.tms_down) > KEY_DOUBLE_MAX_TIME:
                self.long_timer.stop()
                self.ts_prev = self.ts_down
                self.tms_prev = self.tms_down
                self.event = KEY_EVENT_SHORT
                print('key=%s down=%d event=%d'%(self.name,irqtype,self.event)) 
                sys_bus.publish('MKEY_EVENT', self.event)
            #short hit type2 20<up<300 wait timer report in timer cb
            else:
                self.ts_prev = self.ts_down
                self.tms_prev = self.tms_down
                self.up_before_double_timer = 1

    def __init__(self, pin, int, name):
        #prev time update when reort key state, if no state report drop this time
        self.ts_prev = 0
        self.tms_prev = 0
        self.tms_down = 0
        self.ts_down = 0
        self.event = KEY_EVENT_SHORT
        self.double_timer = osTimer()
        self.long_timer = osTimer()
        self.up_before_double_timer = 0        
        self.name = name
        self.pin = Pin(pin, Pin.IN, Pin.PULL_PU, 0)
        self.int = ExtInt(int, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, self.intfucn)
        self.int.enable()
        pass

if __name__ == "__main__":
    key10 = gpio_key(Pin.GPIO10, ExtInt.GPIO10, "key10")
    key13 = gpio_key(Pin.GPIO13, ExtInt.GPIO13, "key13")
    #mkey = gpio_key(MKEY_PIN, MKEY_INT, "mkey")
