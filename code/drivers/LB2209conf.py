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
from misc import ADC
from machine import I2C
#pin define
#int define
AP2MCU_PIN      = Pin.GPIO8
BRAKE_PIN       = Pin.GPIO9
BRAKE_INT           = ExtInt.GPIO9
MKEY_PIN        = Pin.GPIO10
MKEY_INT            = ExtInt.GPIO10
BOOST_5V_EN_PIN = Pin.GPIO11
AUDIO_PA_EN_PIN = Pin.GPIO12
ICN6211_EN_PIN  = Pin.GPIO13
GPS_EN_PIN      = Pin.GPIO14
#CAM_RST    = Pin.GPIO18
#CAM_PWDN   = Pin.GPIO19
ACCL_PIN        = Pin.GPIO20
ACCL_INT            = ExtInt.GPIO20
ALS_PIN         = Pin.GPIO21
ALS_INT             = ExtInt.GPIO21
L_LED_PIN       = Pin.GPIO22
L_LED_INT           = ExtInt.GPIO22
CHARGER_PIN     = Pin.GPIO23
CHARGER_INT         = ExtInt.GPIO23
A_LED_PIN       = Pin.GPIO24
A_LED_INT           = ExtInt.GPIO24
MCU2AP_PIN      = Pin.GPIO25
MCU2AP_INT          = ExtInt.GPIO25
N_LED_PIN       = Pin.GPIO26
N_LED_INT           = ExtInt.GPIO26
F_LED_PIN       = Pin.GPIO27
F_LED_INT           = ExtInt.GPIO27
CHARGER_EN_PIN  = Pin.GPIO28
R_LED_PIN       = Pin.GPIO29
R_LED_INT           = ExtInt.GPIO29
#adc define
LIGHT_ADC       = ADC.ADC0
LCD_ADC = ADC.ADC2
#i2c define
ETA6959_I2C_DEV= I2C.I2C1
ICN6211_I2C_DEV= I2C.I2C1
LTR308_I2C_DEV = I2C.I2C1
MC3416_I2C_DEV = I2C.I2C1
#i2c addr
ETA6965_ADDRESS = 0x6b
ICN6211_ADDRESS = 0x2c
LTR308_ADDRESS = 0x53
MC3416_ADDRESS = 0x4c

