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

import misc
from usr.drivers.LB2209conf import *
from usr.drivers.eta6965 import *
from usr.drivers.led import *
from usr.drivers.key import *
from usr.drivers.exint import *
from usr.drivers.enpin import *
from usr.drivers.pulse import *
from usr.drivers.ltr308 import *
from usr.drivers.mc3416 import *
from usr.drivers.icn6211 import *

def driver_init():
    global dev_eta6965
    global l_led
    global a_led
    global n_led
    global f_led
    global r_led
    global mkey
    global brake
    global mcu2ap
    global boot_5v_en
    global audio_pa_en
    global gps_en
    global ap2mcu
    global dev_ltr308
    global dev_icn6211

    #charger init en and set current 420
    dev_eta6965 = eta6965()
    dev_eta6965.init(ETA6965_ADDRESS)

    #led init init gpio in pull up
    l_led = gpio_in_led(L_LED_PIN, L_LED_INT, "l_led")    
    a_led = gpio_in_led(A_LED_PIN, A_LED_INT, "a_led")
    n_led = gpio_in_led(N_LED_PIN, N_LED_INT, "n_led")
    f_led = gpio_in_led(F_LED_PIN, F_LED_INT, "f_led")
    r_led = gpio_in_led(R_LED_PIN, R_LED_INT, "r_led")

    #key init init gpio in pull up
    mkey = gpio_key(MKEY_PIN, MKEY_INT, "mkey")

    #int init brake and mcu2ap init gpio in pull up
    brake = gpio_exint(BRAKE_PIN, BRAKE_INT, "brake")
    mcu2ap = gpio_exint(MCU2AP_PIN, MCU2AP_INT, "mcu2ap")

    #pin init init gpio out 0
    boot_5v_en = gpio_en(BOOST_5V_EN_PIN, 0, "boot_5v_en")
    audio_pa_en = gpio_en(AUDIO_PA_EN_PIN, 0, "audio_pa_en")
    gps_en = gpio_en(GPS_EN_PIN, 0, "gps_en")

    #pulse pin: ap2mcu wake up mcu init gpio out 0
    ap2mcu = gpio_pulse(AP2MCU_PIN, 1, "ap2mcu")

    #light sensor init will config pin and start sensor
    dev_ltr308 = ltr308()
    dev_ltr308.init(LTR308_ADDRESS)

    #accel sensor init will config pin and start sensor
    dev_mc3416 = mc3416()
    dev_mc3416.init(MC3416_ADDRESS)

    #lcd init
    # dev_icn6211 = icn6211()
    # dev_icn6211.init(ICN6211_ADDRESS)

    #set netmode always off
    misc.net_light(0)
