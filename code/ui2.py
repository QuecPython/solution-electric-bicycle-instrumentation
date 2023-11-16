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

# -*- coding: UTF-8 -*-
from machine import LCD
from machine import Pin
import lvgl as lv
import _thread
import queue
import utime
import osTimer
from usr.const import *
from usr.utils.log import log
from usr.drivers.icn6211 import icn6211

# Common color definitions
red = 0xF800            # gules
green = 0x07E0          # green
blue = 0x001F           # blue
white = 0xFFFF          # white
black = 0x0000          # black
purple = 0xF81F         # purple
colour = white          # Default background color
fc = 0x0000  # The font color black can be modified as required
bc = 0xffff  # Background color white can be modified as required
lvgl_text_main_color = lv.color_make(0x00,0xd2,0xfd)
lvgl_white = lv.color_make(0xff,0xff,0xff)

NAVI_TIMEOUT_MS = 15000 # 15秒内没有收到导航信息就关掉导航显示
TIME_UPDATE_INTERVAL_MS = 60000 # 时间刷新间隔

screen = None
screen_img_bg1 = None
screen_img_bg2 = None
screen_img_bg3 = None
screen_img_bg4 = None
screen_img_bg5 = None
screen_img_bg6 = None
screen_label_speed = None
screen_label_current = None
screen_label_trip = None
screen_label_odo = None
screen_label_left_km = None
screen_label_time = None
screen_label_ready = None
screen_bar_battery = None
screen_bar_battery = None
screen_img_gps = None
screen_img_bt = None
screen_img_light_left = None
screen_img_light_right = None
screen_img_light_far = None
screen_img_light_near = None
screen_img_light_small = None
screen_img_light_auto = None
screen_img_light_double_flash = None
screen_img_warning = None
screen_img_batt_warning = None
screen_img_charging = None
screen_img_left_km = None
screen_img_not_sit = None
screen_img_biancheng = None
screen_img_unbind = None
screen_img_auto_speed = None
screen_img_eco = None
screen_img_bg_gear = None
screen_img_navi_info = None
screen_img_batt_ind = None
screen_label_navi_dist = None
screen_label_navi_info2 = None
screen_label_navi_next_road = None
screen_label_gear_d = None
screen_label_gear_t = None
screen_label_gear_r = None
screen_canvas_qrcode = None
style_screen_main_main_default = None
style_screen_img_bg_main_main_default = None
style_screen_label_speed_main_main_default = None
style_screen_label_current_main_main_default = None
style_screen_label_trip_main_main_default = None
style_screen_label_odo_main_main_default = None
style_screen_label_left_km_main_main_default = None
style_screen_label_time_main_main_default = None
style_screen_label_ready_main_main_default = None
style_screen_bar_battery_main_main_default = None
style_screen_bar_battery_main_indicator_default = None
style_screen_img_gps_main_main_default = None
style_screen_img_bt_main_main_default = None
style_screen_img_light_left_main_main_default = None
style_screen_img_light_right_main_main_default = None
style_screen_img_light_far_main_main_default = None
style_screen_img_light_near_main_main_default = None
style_screen_img_light_small_main_main_default = None
style_screen_img_light_auto_main_main_default = None
style_screen_img_light_double_flash_main_main_default = None
style_screen_img_warning_main_main_default = None
style_screen_img_batt_warning_main_main_default = None
style_screen_img_charging_main_main_default = None
style_screen_img_left_km_main_main_default = None
style_screen_img_not_sit_main_main_default = None
style_screen_img_biancheng_main_main_default = None
style_screen_img_unbind_main_main_default = None
style_screen_img_auto_speed_main_main_default = None
style_screen_img_eco_main_main_default = None
style_screen_img_bg_gear_main_main_default = None
style_screen_img_navi_info_main_main_default = None
style_screen_img_batt_ind_main_main_default = None
style_screen_label_navi_dist_main_main_default = None
style_screen_label_navi_info2_main_main_default = None
style_screen_label_navi_next_road_main_main_default = None
style_screen_label_gear_d_main_main_default = None
style_screen_label_gear_t_main_main_default = None
style_screen_label_gear_r_main_main_default = None
style_screen_canvas_qrcode_main_main_default = None



class UI_lvgl:

    def __init__(self, mmi):
        log.d('ui __init__')
        self.mmi = mmi
        # self.screen_backlight = Pin(Pin.GPIO8, Pin.OUT, Pin.PULL_DISABLE,0)


        
        self.mipilcd = LCD()
        init_480X800_XMT = (0x29,0,0)
        #self.mipilcd.mipi_init(initbuf=bytearray(init_480X800_XMT), width=800,hight=480, DataLane=2, TransMode=1, HSync=128, HFP=88, HBP=0, VSync=128, VFP=13, VBP=45, FrameRate=45)
        #self.mipilcd.mipi_init(initbuf=bytearray(init_480X800_XMT),width=800,hight=480, DataLane=2, TransMode=3, HSync=48, HFP=40, HBP=40, VSync=1, VFP=13, VBP=31, FrameRate=60)
        self.mipilcd.mipi_init(initbuf=bytearray(init_480X800_XMT),width=800,hight=480, DataLane=2, RstPolarity=0, TransMode=3, HSync=48, HFP=40, HBP=40, VSync=1, VFP=13, VBP=31, FrameRate=60)
        #self.mipilcd.lcd_init(width=480,hight=854,type=3)
        #self.mipilcd.lcd_clear(red)
        self.icn6211 = icn6211()
        self.icn6211.init(ICN6211_ADDRESS)
        self.icn6211.lcd_on()
        if USE_DEVBOARD:
            self.sdcard_enable = Pin(Pin.GPIO27, Pin.OUT, Pin.PULL_DISABLE,0)
            self.sdcard_enable.write(1)

        self.lvgl_ui_init()
        self.curSpeed = 0
        self.curCurrent = 0
        self.curBatt = 0

        _thread.stack_size(1024*5)
        _thread.start_new_thread(self.ui_lvgl_thread,(THREAD_ID_UI,))


    def ui_lvgl_thread(self,thread_id):
        global screen
        global screen_img_bg1
        global screen_img_bg2
        global screen_img_bg3
        global screen_img_bg4
        global screen_img_bg5
        global screen_img_bg6
        global screen_label_speed
        global screen_label_current
        global screen_label_trip
        global screen_label_odo
        global screen_label_left_km
        global screen_label_time
        global screen_label_ready
        global screen_bar_battery
        global screen_bar_battery
        global screen_img_gps
        global screen_img_bt
        global screen_img_light_left
        global screen_img_light_right
        global screen_img_light_far
        global screen_img_light_near
        global screen_img_light_small
        global screen_img_light_auto
        global screen_img_light_double_flash
        global screen_img_warning
        global screen_img_batt_warning
        global screen_img_charging
        global screen_img_left_km
        global screen_img_not_sit
        global screen_img_biancheng
        global screen_img_unbind
        global screen_img_auto_speed
        global screen_img_eco
        global screen_img_bg_gear
        global screen_img_navi_info
        global screen_img_batt_ind
        global screen_label_navi_dist
        global screen_label_navi_info2
        global screen_label_navi_next_road
        global screen_label_gear_d
        global screen_label_gear_t
        global screen_label_gear_r
        global screen_canvas_qrcode
        global style_screen_main_main_default
        global style_screen_img_bg_main_main_default
        global style_screen_label_speed_main_main_default
        global style_screen_label_current_main_main_default
        global style_screen_label_trip_main_main_default
        global style_screen_label_odo_main_main_default
        global style_screen_label_left_km_main_main_default
        global style_screen_label_time_main_main_default
        global style_screen_label_ready_main_main_default
        global style_screen_bar_battery_main_main_default
        global style_screen_bar_battery_main_indicator_default
        global style_screen_img_gps_main_main_default
        global style_screen_img_bt_main_main_default
        global style_screen_img_light_left_main_main_default
        global style_screen_img_light_right_main_main_default
        global style_screen_img_light_far_main_main_default
        global style_screen_img_light_near_main_main_default
        global style_screen_img_light_small_main_main_default
        global style_screen_img_light_auto_main_main_default
        global style_screen_img_light_double_flash_main_main_default
        global style_screen_img_warning_main_main_default
        global style_screen_img_batt_warning_main_main_default
        global style_screen_img_charging_main_main_default
        global style_screen_img_left_km_main_main_default
        global style_screen_img_not_sit_main_main_default
        global style_screen_img_biancheng_main_main_default
        global style_screen_img_unbind_main_main_default
        global style_screen_img_auto_speed_main_main_default
        global style_screen_img_eco_main_main_default
        global style_screen_img_bg_gear_main_main_default
        global style_screen_img_navi_info_main_main_default
        global style_screen_img_batt_ind_main_main_default
        global style_screen_label_navi_dist_main_main_default
        global style_screen_label_navi_info2_main_main_default
        global style_screen_label_navi_next_road_main_main_default
        global style_screen_label_gear_d_main_main_default
        global style_screen_label_gear_t_main_main_default
        global style_screen_label_gear_r_main_main_default
        global style_screen_canvas_qrcode_main_main_default


        self.naviTimer = osTimer()
        self.timeTimer = osTimer()
        # self.updateSysTime(0)
        self.timeTimer.start(TIME_UPDATE_INTERVAL_MS, 1, self.updateSysTime)
        log.d("lvgl thread id is:%d" % thread_id)
        global lvgl_queue
        lvgl_queue = queue.Queue(300)
        self.lvgl_handle_list = (
            self.set_speed_noanim, 
            self.set_current_noanim, 
            self.set_battery_noanim,
            self.set_gear,
            self.set_trip,
            self.set_leftkm,
            self.set_time,
            self.set_ready,
            self.set_mobile_signal,
            self.set_gps,
            self.set_bt,
            self.set_light_left,
            self.set_light_right,
            self.set_light_far,
            self.set_light_near,
            self.set_light_auto,
            self.set_light_small,
            self.set_light_doubleflash,
            self.set_auto_speed,
            self.set_warning,
            self.set_batt_warning,
            self.set_eco,
            self.set_charging,
            self.set_not_sit,
            self.set_biancheng,
            self.set_unbind,
            self.set_navi_info,
            self.set_odo,
            self.hide_navi
            )
        
        ################################################################## 以下代码从GUI Guide中复制出来的 ##################################################################

        screen = lv.obj()
        # create style style_screen_main_main_default
        style_screen_main_main_default = lv.style_t()
        style_screen_main_main_default.init()
        style_screen_main_main_default.set_bg_color(lv.color_make(0x02,0x0d,0x1b))
        style_screen_main_main_default.set_bg_opa(255)

        # add style for screen
        screen.add_style(style_screen_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_bg1 = lv.img(screen)
        screen_img_bg1.set_size(400,160)
        screen_img_bg1.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_bg1.set_src('U:/images2/background1.png')
        screen_img_bg1.set_pos(0,0)
        screen_img_bg1.set_angle(0)
        # create style style_screen_img_bg_main_main_default
        style_screen_img_bg_main_main_default = lv.style_t()
        style_screen_img_bg_main_main_default.init()
        style_screen_img_bg_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_bg_main_main_default.set_img_recolor_opa(0)
        style_screen_img_bg_main_main_default.set_img_opa(255)

        # add style for screen_img_bg
        screen_img_bg1.add_style(style_screen_img_bg_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


        screen_img_bg2 = lv.img(screen)
        screen_img_bg2.set_size(400,160)
        screen_img_bg2.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_bg2.set_src('U:/images2/background2.png')
        screen_img_bg2.set_pos(400,0)
        screen_img_bg2.set_angle(0)
        screen_img_bg2.add_style(style_screen_img_bg_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        
        screen_img_bg3 = lv.img(screen)
        screen_img_bg3.set_size(400,160)
        screen_img_bg3.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_bg3.set_src('U:/images2/background3.png')
        screen_img_bg3.set_pos(0,160)
        screen_img_bg3.set_angle(0)
        screen_img_bg3.add_style(style_screen_img_bg_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        
        screen_img_bg4 = lv.img(screen)
        screen_img_bg4.set_size(400,160)
        screen_img_bg4.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_bg4.set_src('U:/images2/background4.png')
        screen_img_bg4.set_pos(400,160)
        screen_img_bg4.set_angle(0)
        screen_img_bg4.add_style(style_screen_img_bg_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        
        screen_img_bg5 = lv.img(screen)
        screen_img_bg5.set_size(400,160)
        screen_img_bg5.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_bg5.set_src('U:/images2/background5.png')
        screen_img_bg5.set_pos(0,320)
        screen_img_bg5.set_angle(0)
        screen_img_bg5.add_style(style_screen_img_bg_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        
        screen_img_bg6 = lv.img(screen)
        screen_img_bg6.set_size(400,160)
        screen_img_bg6.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_bg6.set_src('U:/images2/background6.png')
        screen_img_bg6.set_pos(400,320)
        screen_img_bg6.set_angle(0)
        screen_img_bg6.add_style(style_screen_img_bg_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)


        screen_label_speed = lv.label(screen)
        screen_label_speed.set_pos(158,209)
        screen_label_speed.set_size(120,61)
        screen_label_speed.set_text("100")
        screen_label_speed.set_long_mode(lv.label.LONG.CLIP)
        screen_label_speed.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        # create style style_screen_label_speed_main_main_default
        style_screen_label_speed_main_main_default = lv.style_t()
        style_screen_label_speed_main_main_default.init()
        style_screen_label_speed_main_main_default.set_radius(0)
        style_screen_label_speed_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_speed_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_speed_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_speed_main_main_default.set_bg_opa(0)
        style_screen_label_speed_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
        try:
            style_screen_label_speed_main_main_default.set_text_font(lv.font_HarmonyOS_Bold_60)
        except AttributeError:
            try:
                style_screen_label_speed_main_main_default.set_text_font(lv.font_montserrat_60)
            except AttributeError:
                style_screen_label_speed_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_speed_main_main_default.set_text_letter_space(2)
        style_screen_label_speed_main_main_default.set_pad_left(0)
        style_screen_label_speed_main_main_default.set_pad_right(0)
        style_screen_label_speed_main_main_default.set_pad_top(0)
        style_screen_label_speed_main_main_default.set_pad_bottom(0)

        # add style for screen_label_speed
        screen_label_speed.add_style(style_screen_label_speed_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_current = lv.label(screen)
        screen_label_current.set_pos(526,209)
        screen_label_current.set_size(120,65)
        screen_label_current.set_text("35")
        screen_label_current.set_long_mode(lv.label.LONG.CLIP)
        screen_label_current.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        # create style style_screen_label_current_main_main_default
        style_screen_label_current_main_main_default = lv.style_t()
        style_screen_label_current_main_main_default.init()
        style_screen_label_current_main_main_default.set_radius(0)
        style_screen_label_current_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_current_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_current_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_current_main_main_default.set_bg_opa(0)
        style_screen_label_current_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
        try:
            style_screen_label_current_main_main_default.set_text_font(lv.font_HarmonyOS_Bold_60)
        except AttributeError:
            try:
                style_screen_label_current_main_main_default.set_text_font(lv.font_montserrat_60)
            except AttributeError:
                style_screen_label_current_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_current_main_main_default.set_text_letter_space(2)
        style_screen_label_current_main_main_default.set_pad_left(0)
        style_screen_label_current_main_main_default.set_pad_right(0)
        style_screen_label_current_main_main_default.set_pad_top(0)
        style_screen_label_current_main_main_default.set_pad_bottom(0)

        # add style for screen_label_current
        screen_label_current.add_style(style_screen_label_current_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_trip = lv.label(screen)
        screen_label_trip.set_pos(296,381)
        screen_label_trip.set_size(57,22)
        screen_label_trip.set_text("010")
        screen_label_trip.set_long_mode(lv.label.LONG.WRAP)
        screen_label_trip.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        # create style style_screen_label_trip_main_main_default
        style_screen_label_trip_main_main_default = lv.style_t()
        style_screen_label_trip_main_main_default.init()
        style_screen_label_trip_main_main_default.set_radius(0)
        style_screen_label_trip_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_trip_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_trip_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_trip_main_main_default.set_bg_opa(0)
        style_screen_label_trip_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
        try:
            style_screen_label_trip_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_trip_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_trip_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_trip_main_main_default.set_text_letter_space(2)
        style_screen_label_trip_main_main_default.set_pad_left(0)
        style_screen_label_trip_main_main_default.set_pad_right(0)
        style_screen_label_trip_main_main_default.set_pad_top(0)
        style_screen_label_trip_main_main_default.set_pad_bottom(0)

        # add style for screen_label_trip
        screen_label_trip.add_style(style_screen_label_trip_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_odo = lv.label(screen)
        screen_label_odo.set_pos(439,381)
        screen_label_odo.set_size(75,22)
        screen_label_odo.set_text("01896")
        screen_label_odo.set_long_mode(lv.label.LONG.WRAP)
        screen_label_odo.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        # create style style_screen_label_odo_main_main_default
        style_screen_label_odo_main_main_default = lv.style_t()
        style_screen_label_odo_main_main_default.init()
        style_screen_label_odo_main_main_default.set_radius(0)
        style_screen_label_odo_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_odo_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_odo_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_odo_main_main_default.set_bg_opa(0)
        style_screen_label_odo_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
        try:
            style_screen_label_odo_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_odo_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_odo_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_odo_main_main_default.set_text_letter_space(2)
        style_screen_label_odo_main_main_default.set_pad_left(0)
        style_screen_label_odo_main_main_default.set_pad_right(0)
        style_screen_label_odo_main_main_default.set_pad_top(0)
        style_screen_label_odo_main_main_default.set_pad_bottom(0)

        # add style for screen_label_odo
        screen_label_odo.add_style(style_screen_label_odo_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_left_km = lv.label(screen)
        screen_label_left_km.set_pos(562,414)
        screen_label_left_km.set_size(53,19)
        screen_label_left_km.set_text("189")
        screen_label_left_km.set_long_mode(lv.label.LONG.CLIP)
        screen_label_left_km.set_style_text_align(lv.TEXT_ALIGN.RIGHT, 0)
        # create style style_screen_label_left_km_main_main_default
        style_screen_label_left_km_main_main_default = lv.style_t()
        style_screen_label_left_km_main_main_default.init()
        style_screen_label_left_km_main_main_default.set_radius(0)
        style_screen_label_left_km_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_left_km_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_left_km_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_left_km_main_main_default.set_bg_opa(0)
        style_screen_label_left_km_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
        try:
            style_screen_label_left_km_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_left_km_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_left_km_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_left_km_main_main_default.set_text_letter_space(2)
        style_screen_label_left_km_main_main_default.set_pad_left(0)
        style_screen_label_left_km_main_main_default.set_pad_right(0)
        style_screen_label_left_km_main_main_default.set_pad_top(0)
        style_screen_label_left_km_main_main_default.set_pad_bottom(0)

        # add style for screen_label_left_km
        screen_label_left_km.add_style(style_screen_label_left_km_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_time = lv.label(screen)
        screen_label_time.set_pos(676,12)
        screen_label_time.set_size(69,20)
        screen_label_time.set_text("09:30")
        screen_label_time.set_long_mode(lv.label.LONG.WRAP)
        screen_label_time.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        # create style style_screen_label_time_main_main_default
        style_screen_label_time_main_main_default = lv.style_t()
        style_screen_label_time_main_main_default.init()
        style_screen_label_time_main_main_default.set_radius(0)
        style_screen_label_time_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_time_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_time_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_time_main_main_default.set_bg_opa(0)
        style_screen_label_time_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
        try:
            style_screen_label_time_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_time_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_time_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_time_main_main_default.set_text_letter_space(2)
        style_screen_label_time_main_main_default.set_pad_left(0)
        style_screen_label_time_main_main_default.set_pad_right(0)
        style_screen_label_time_main_main_default.set_pad_top(0)
        style_screen_label_time_main_main_default.set_pad_bottom(0)

        # add style for screen_label_time
        screen_label_time.add_style(style_screen_label_time_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_ready = lv.label(screen)
        screen_label_ready.set_pos(360,15)
        screen_label_ready.set_size(80,28)
        screen_label_ready.set_text("Ready")
        screen_label_ready.set_long_mode(lv.label.LONG.WRAP)
        screen_label_ready.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        # create style style_screen_label_ready_main_main_default
        style_screen_label_ready_main_main_default = lv.style_t()
        style_screen_label_ready_main_main_default.init()
        style_screen_label_ready_main_main_default.set_radius(0)
        style_screen_label_ready_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_ready_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_ready_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_ready_main_main_default.set_bg_opa(0)
        style_screen_label_ready_main_main_default.set_text_color(lv.color_make(0x00,0xff,0x66))
        try:
            style_screen_label_ready_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_ready_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_ready_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_ready_main_main_default.set_text_letter_space(2)
        style_screen_label_ready_main_main_default.set_pad_left(0)
        style_screen_label_ready_main_main_default.set_pad_right(0)
        style_screen_label_ready_main_main_default.set_pad_top(0)
        style_screen_label_ready_main_main_default.set_pad_bottom(0)

        # add style for screen_label_ready
        screen_label_ready.add_style(style_screen_label_ready_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_bar_battery = lv.bar(screen)
        screen_bar_battery.set_pos(306,456)
        screen_bar_battery.set_size(200,4)
        screen_bar_battery.set_style_anim_time(1000, lv.PART.INDICATOR|lv.STATE.DEFAULT)
        screen_bar_battery.set_mode(lv.bar.MODE.NORMAL)
        screen_bar_battery.set_value(50, lv.ANIM.OFF)
        # create style style_screen_bar_battery_main_main_default
        style_screen_bar_battery_main_main_default = lv.style_t()
        style_screen_bar_battery_main_main_default.init()
        style_screen_bar_battery_main_main_default.set_radius(10)
        style_screen_bar_battery_main_main_default.set_bg_color(lv.color_make(0x7f,0x84,0x8b))
        style_screen_bar_battery_main_main_default.set_bg_grad_color(lv.color_make(0x7f,0x84,0x8b))
        style_screen_bar_battery_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_bar_battery_main_main_default.set_bg_opa(255)
        style_screen_bar_battery_main_main_default.set_pad_left(0)
        style_screen_bar_battery_main_main_default.set_pad_right(0)
        style_screen_bar_battery_main_main_default.set_pad_top(0)
        style_screen_bar_battery_main_main_default.set_pad_bottom(0)

        # add style for screen_bar_battery
        screen_bar_battery.add_style(style_screen_bar_battery_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        # create style style_screen_bar_battery_main_indicator_default
        style_screen_bar_battery_main_indicator_default = lv.style_t()
        style_screen_bar_battery_main_indicator_default.init()
        style_screen_bar_battery_main_indicator_default.set_radius(10)
        style_screen_bar_battery_main_indicator_default.set_bg_color(lv.color_make(0x0d,0x2e,0x32))
        style_screen_bar_battery_main_indicator_default.set_bg_grad_color(lv.color_make(0x07,0xf6,0xf3))
        style_screen_bar_battery_main_indicator_default.set_bg_grad_dir(lv.GRAD_DIR.HOR)
        style_screen_bar_battery_main_indicator_default.set_bg_opa(255)

        # add style for screen_bar_battery
        screen_bar_battery.add_style(style_screen_bar_battery_main_indicator_default, lv.PART.INDICATOR|lv.STATE.DEFAULT)

        screen_img_gps = lv.img(screen)
        screen_img_gps.set_pos(82,20)
        screen_img_gps.set_size(20,20)
        screen_img_gps.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_gps.set_src('U:/images2/icon_gps.png')
        screen_img_gps.set_pivot(0,0)
        screen_img_gps.set_angle(0)
        # create style style_screen_img_gps_main_main_default
        style_screen_img_gps_main_main_default = lv.style_t()
        style_screen_img_gps_main_main_default.init()
        style_screen_img_gps_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_gps_main_main_default.set_img_recolor_opa(0)
        style_screen_img_gps_main_main_default.set_img_opa(255)

        # add style for screen_img_gps
        screen_img_gps.add_style(style_screen_img_gps_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_bt = lv.img(screen)
        screen_img_bt.set_pos(108,20)
        screen_img_bt.set_size(20,20)
        screen_img_bt.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_bt.set_src('U:/images2/icon_bt.png')
        screen_img_bt.set_pivot(0,0)
        screen_img_bt.set_angle(0)
        # create style style_screen_img_bt_main_main_default
        style_screen_img_bt_main_main_default = lv.style_t()
        style_screen_img_bt_main_main_default.init()
        style_screen_img_bt_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_bt_main_main_default.set_img_recolor_opa(0)
        style_screen_img_bt_main_main_default.set_img_opa(255)

        # add style for screen_img_bt
        screen_img_bt.add_style(style_screen_img_bt_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_light_left = lv.img(screen)
        screen_img_light_left.set_pos(154,11)
        screen_img_light_left.set_size(36,36)
        screen_img_light_left.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_light_left.set_src('U:/images2/icon_light_left.png')
        screen_img_light_left.set_pivot(0,0)
        screen_img_light_left.set_angle(0)
        # create style style_screen_img_light_left_main_main_default
        style_screen_img_light_left_main_main_default = lv.style_t()
        style_screen_img_light_left_main_main_default.init()
        style_screen_img_light_left_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_light_left_main_main_default.set_img_recolor_opa(0)
        style_screen_img_light_left_main_main_default.set_img_opa(255)

        # add style for screen_img_light_left
        screen_img_light_left.add_style(style_screen_img_light_left_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_light_right = lv.img(screen)
        screen_img_light_right.set_pos(610,11)
        screen_img_light_right.set_size(36,36)
        screen_img_light_right.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_light_right.set_src('U:/images2/icon_light_right.png')
        screen_img_light_right.set_pivot(0,0)
        screen_img_light_right.set_angle(0)
        # create style style_screen_img_light_right_main_main_default
        style_screen_img_light_right_main_main_default = lv.style_t()
        style_screen_img_light_right_main_main_default.init()
        style_screen_img_light_right_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_light_right_main_main_default.set_img_recolor_opa(0)
        style_screen_img_light_right_main_main_default.set_img_opa(255)

        # add style for screen_img_light_right
        screen_img_light_right.add_style(style_screen_img_light_right_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_light_far = lv.img(screen)
        screen_img_light_far.set_pos(210,12)
        screen_img_light_far.set_size(34,34)
        screen_img_light_far.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_light_far.set_src('U:/images2/icon_light_far.png')
        screen_img_light_far.set_pivot(0,0)
        screen_img_light_far.set_angle(0)
        # create style style_screen_img_light_far_main_main_default
        style_screen_img_light_far_main_main_default = lv.style_t()
        style_screen_img_light_far_main_main_default.init()
        style_screen_img_light_far_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_light_far_main_main_default.set_img_recolor_opa(0)
        style_screen_img_light_far_main_main_default.set_img_opa(255)

        # add style for screen_img_light_far
        screen_img_light_far.add_style(style_screen_img_light_far_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_light_near = lv.img(screen)
        screen_img_light_near.set_pos(258,12)
        screen_img_light_near.set_size(34,34)
        screen_img_light_near.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_light_near.set_src('U:/images2/icon_light_near.png')
        screen_img_light_near.set_pivot(0,0)
        screen_img_light_near.set_angle(0)
        # create style style_screen_img_light_near_main_main_default
        style_screen_img_light_near_main_main_default = lv.style_t()
        style_screen_img_light_near_main_main_default.init()
        style_screen_img_light_near_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_light_near_main_main_default.set_img_recolor_opa(0)
        style_screen_img_light_near_main_main_default.set_img_opa(255)

        # add style for screen_img_light_near
        screen_img_light_near.add_style(style_screen_img_light_near_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_light_small = lv.img(screen)
        screen_img_light_small.set_pos(306,12)
        screen_img_light_small.set_size(34,34)
        screen_img_light_small.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_light_small.set_src('U:/images2/icon_light_small.png')
        screen_img_light_small.set_pivot(0,0)
        screen_img_light_small.set_angle(0)
        # create style style_screen_img_light_small_main_main_default
        style_screen_img_light_small_main_main_default = lv.style_t()
        style_screen_img_light_small_main_main_default.init()
        style_screen_img_light_small_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_light_small_main_main_default.set_img_recolor_opa(0)
        style_screen_img_light_small_main_main_default.set_img_opa(255)

        # add style for screen_img_light_small
        screen_img_light_small.add_style(style_screen_img_light_small_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_light_auto = lv.img(screen)
        screen_img_light_auto.set_pos(461,13)
        screen_img_light_auto.set_size(32,32)
        screen_img_light_auto.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_light_auto.set_src('U:/images2/icon_light_auto.png')
        screen_img_light_auto.set_pivot(0,0)
        screen_img_light_auto.set_angle(0)
        # create style style_screen_img_light_auto_main_main_default
        style_screen_img_light_auto_main_main_default = lv.style_t()
        style_screen_img_light_auto_main_main_default.init()
        style_screen_img_light_auto_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_light_auto_main_main_default.set_img_recolor_opa(0)
        style_screen_img_light_auto_main_main_default.set_img_opa(255)

        # add style for screen_img_light_auto
        screen_img_light_auto.add_style(style_screen_img_light_auto_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_light_double_flash = lv.img(screen)
        screen_img_light_double_flash.set_pos(508,12)
        screen_img_light_double_flash.set_size(34,34)
        screen_img_light_double_flash.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_light_double_flash.set_src('U:/images2/icon_light_double_flash.png')
        screen_img_light_double_flash.set_pivot(0,0)
        screen_img_light_double_flash.set_angle(0)
        # create style style_screen_img_light_double_flash_main_main_default
        style_screen_img_light_double_flash_main_main_default = lv.style_t()
        style_screen_img_light_double_flash_main_main_default.init()
        style_screen_img_light_double_flash_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_light_double_flash_main_main_default.set_img_recolor_opa(0)
        style_screen_img_light_double_flash_main_main_default.set_img_opa(255)

        # add style for screen_img_light_double_flash
        screen_img_light_double_flash.add_style(style_screen_img_light_double_flash_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_warning = lv.img(screen)
        screen_img_warning.set_pos(30,407)
        screen_img_warning.set_size(30,30)
        screen_img_warning.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_warning.set_src('U:/images2/icon_warning.png')
        screen_img_warning.set_pivot(0,0)
        screen_img_warning.set_angle(0)
        # create style style_screen_img_warning_main_main_default
        style_screen_img_warning_main_main_default = lv.style_t()
        style_screen_img_warning_main_main_default.init()
        style_screen_img_warning_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_warning_main_main_default.set_img_recolor_opa(0)
        style_screen_img_warning_main_main_default.set_img_opa(255)

        # add style for screen_img_warning
        screen_img_warning.add_style(style_screen_img_warning_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_batt_warning = lv.img(screen)
        screen_img_batt_warning.set_pos(74,407)
        screen_img_batt_warning.set_size(30,30)
        screen_img_batt_warning.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_batt_warning.set_src('U:/images2/icon_batt_warning.png')
        screen_img_batt_warning.set_pivot(0,0)
        screen_img_batt_warning.set_angle(0)
        # create style style_screen_img_batt_warning_main_main_default
        style_screen_img_batt_warning_main_main_default = lv.style_t()
        style_screen_img_batt_warning_main_main_default.init()
        style_screen_img_batt_warning_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_batt_warning_main_main_default.set_img_recolor_opa(0)
        style_screen_img_batt_warning_main_main_default.set_img_opa(255)

        # add style for screen_img_batt_warning
        screen_img_batt_warning.add_style(style_screen_img_batt_warning_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_charging = lv.img(screen)
        screen_img_charging.set_pos(206,407)
        screen_img_charging.set_size(30,30)
        screen_img_charging.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_charging.set_src('U:/images2/icon_charging.png')
        screen_img_charging.set_pivot(0,0)
        screen_img_charging.set_angle(0)
        # create style style_screen_img_charging_main_main_default
        style_screen_img_charging_main_main_default = lv.style_t()
        style_screen_img_charging_main_main_default.init()
        style_screen_img_charging_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_charging_main_main_default.set_img_recolor_opa(0)
        style_screen_img_charging_main_main_default.set_img_opa(255)

        # add style for screen_img_charging
        screen_img_charging.add_style(style_screen_img_charging_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_left_km = lv.img(screen)
        screen_img_left_km.set_pos(541,409)
        screen_img_left_km.set_size(30,30)
        screen_img_left_km.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_left_km.set_src('U:/images2/icon_left_km.png')
        screen_img_left_km.set_pivot(0,0)
        screen_img_left_km.set_angle(0)
        # create style style_screen_img_left_km_main_main_default
        style_screen_img_left_km_main_main_default = lv.style_t()
        style_screen_img_left_km_main_main_default.init()
        style_screen_img_left_km_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_left_km_main_main_default.set_img_recolor_opa(0)
        style_screen_img_left_km_main_main_default.set_img_opa(255)

        # add style for screen_img_left_km
        screen_img_left_km.add_style(style_screen_img_left_km_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_not_sit = lv.img(screen)
        screen_img_not_sit.set_pos(652,407)
        screen_img_not_sit.set_size(30,30)
        screen_img_not_sit.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_not_sit.set_src('U:/images2/icon_no_sit.png')
        screen_img_not_sit.set_pivot(0,0)
        screen_img_not_sit.set_angle(0)
        # create style style_screen_img_not_sit_main_main_default
        style_screen_img_not_sit_main_main_default = lv.style_t()
        style_screen_img_not_sit_main_main_default.init()
        style_screen_img_not_sit_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_not_sit_main_main_default.set_img_recolor_opa(0)
        style_screen_img_not_sit_main_main_default.set_img_opa(255)

        # add style for screen_img_not_sit
        screen_img_not_sit.add_style(style_screen_img_not_sit_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_biancheng = lv.img(screen)
        screen_img_biancheng.set_pos(696,407)
        screen_img_biancheng.set_size(30,30)
        screen_img_biancheng.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_biancheng.set_src('U:/images2/icon_biancheng.png')
        screen_img_biancheng.set_pivot(0,0)
        screen_img_biancheng.set_angle(0)
        # create style style_screen_img_biancheng_main_main_default
        style_screen_img_biancheng_main_main_default = lv.style_t()
        style_screen_img_biancheng_main_main_default.init()
        style_screen_img_biancheng_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_biancheng_main_main_default.set_img_recolor_opa(0)
        style_screen_img_biancheng_main_main_default.set_img_opa(255)

        # add style for screen_img_biancheng
        screen_img_biancheng.add_style(style_screen_img_biancheng_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_unbind = lv.img(screen)
        screen_img_unbind.set_pos(740,407)
        screen_img_unbind.set_size(30,30)
        screen_img_unbind.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_unbind.set_src('U:/images2/icon_unbind.png')
        screen_img_unbind.set_pivot(0,0)
        screen_img_unbind.set_angle(0)
        # create style style_screen_img_unbind_main_main_default
        style_screen_img_unbind_main_main_default = lv.style_t()
        style_screen_img_unbind_main_main_default.init()
        style_screen_img_unbind_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_unbind_main_main_default.set_img_recolor_opa(0)
        style_screen_img_unbind_main_main_default.set_img_opa(255)

        # add style for screen_img_unbind
        screen_img_unbind.add_style(style_screen_img_unbind_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_auto_speed = lv.img(screen)
        screen_img_auto_speed.set_pos(196,176)
        screen_img_auto_speed.set_size(33,32)
        screen_img_auto_speed.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_auto_speed.set_src('U:/images2/icon_auto_speed.png')
        screen_img_auto_speed.set_pivot(0,0)
        screen_img_auto_speed.set_angle(0)
        # create style style_screen_img_auto_speed_main_main_default
        style_screen_img_auto_speed_main_main_default = lv.style_t()
        style_screen_img_auto_speed_main_main_default.init()
        style_screen_img_auto_speed_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_auto_speed_main_main_default.set_img_recolor_opa(0)
        style_screen_img_auto_speed_main_main_default.set_img_opa(255)

        # add style for screen_img_auto_speed
        screen_img_auto_speed.add_style(style_screen_img_auto_speed_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_eco = lv.img(screen)
        screen_img_eco.set_pos(552,179)
        screen_img_eco.set_size(65,29)
        screen_img_eco.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_eco.set_src('U:/images2/icon_eco.png')
        screen_img_eco.set_pivot(0,0)
        screen_img_eco.set_angle(0)
        # create style style_screen_img_eco_main_main_default
        style_screen_img_eco_main_main_default = lv.style_t()
        style_screen_img_eco_main_main_default.init()
        style_screen_img_eco_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_eco_main_main_default.set_img_recolor_opa(0)
        style_screen_img_eco_main_main_default.set_img_opa(255)

        # add style for screen_img_eco
        screen_img_eco.add_style(style_screen_img_eco_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_bg_gear = lv.img(screen)
        screen_img_bg_gear.set_pos(290,102)
        screen_img_bg_gear.set_size(220,40)
        screen_img_bg_gear.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_bg_gear.set_src('U:/images2/bg_gear.png')
        screen_img_bg_gear.set_pivot(0,0)
        screen_img_bg_gear.set_angle(0)
        # create style style_screen_img_bg_gear_main_main_default
        style_screen_img_bg_gear_main_main_default = lv.style_t()
        style_screen_img_bg_gear_main_main_default.init()
        style_screen_img_bg_gear_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_bg_gear_main_main_default.set_img_recolor_opa(0)
        style_screen_img_bg_gear_main_main_default.set_img_opa(255)

        # add style for screen_img_bg_gear
        screen_img_bg_gear.add_style(style_screen_img_bg_gear_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_navi_info = lv.img(screen)
        screen_img_navi_info.set_pos(374,74)
        screen_img_navi_info.set_size(50,50)
        screen_img_navi_info.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_navi_info.set_src('U:/images2/action5.png')
        screen_img_navi_info.set_pivot(0,0)
        screen_img_navi_info.set_angle(0)
        # create style style_screen_img_navi_info_main_main_default
        style_screen_img_navi_info_main_main_default = lv.style_t()
        style_screen_img_navi_info_main_main_default.init()
        style_screen_img_navi_info_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_navi_info_main_main_default.set_img_recolor_opa(0)
        style_screen_img_navi_info_main_main_default.set_img_opa(255)

        # add style for screen_img_navi_info
        screen_img_navi_info.add_style(style_screen_img_navi_info_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_img_batt_ind = lv.img(screen)
        screen_img_batt_ind.set_pos(400,442)
        screen_img_batt_ind.set_size(13,9)
        screen_img_batt_ind.add_flag(lv.obj.FLAG.CLICKABLE)
        screen_img_batt_ind.set_src('U:/images2/icon_batt_indicator.png')
        screen_img_batt_ind.set_pivot(0,0)
        screen_img_batt_ind.set_angle(0)
        # create style style_screen_img_batt_ind_main_main_default
        style_screen_img_batt_ind_main_main_default = lv.style_t()
        style_screen_img_batt_ind_main_main_default.init()
        style_screen_img_batt_ind_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_img_batt_ind_main_main_default.set_img_recolor_opa(0)
        style_screen_img_batt_ind_main_main_default.set_img_opa(255)

        # add style for screen_img_batt_ind
        screen_img_batt_ind.add_style(style_screen_img_batt_ind_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_navi_dist = lv.label(screen)
        screen_label_navi_dist.set_pos(285,133)
        screen_label_navi_dist.set_size(122,49)
        screen_label_navi_dist.set_text("480")
        screen_label_navi_dist.set_long_mode(lv.label.LONG.WRAP)
        screen_label_navi_dist.set_style_text_align(lv.TEXT_ALIGN.RIGHT, 0)
        # create style style_screen_label_navi_dist_main_main_default
        style_screen_label_navi_dist_main_main_default = lv.style_t()
        style_screen_label_navi_dist_main_main_default.init()
        style_screen_label_navi_dist_main_main_default.set_radius(0)
        style_screen_label_navi_dist_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_navi_dist_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_navi_dist_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_navi_dist_main_main_default.set_bg_opa(0)
        style_screen_label_navi_dist_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
        try:
            style_screen_label_navi_dist_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_48)
        except AttributeError:
            try:
                style_screen_label_navi_dist_main_main_default.set_text_font(lv.font_montserrat_48)
            except AttributeError:
                style_screen_label_navi_dist_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_navi_dist_main_main_default.set_text_letter_space(2)
        style_screen_label_navi_dist_main_main_default.set_pad_left(0)
        style_screen_label_navi_dist_main_main_default.set_pad_right(0)
        style_screen_label_navi_dist_main_main_default.set_pad_top(0)
        style_screen_label_navi_dist_main_main_default.set_pad_bottom(0)

        # add style for screen_label_navi_dist
        screen_label_navi_dist.add_style(style_screen_label_navi_dist_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_navi_info2 = lv.label(screen)
        screen_label_navi_info2.set_pos(415,152)
        screen_label_navi_info2.set_size(98,20)
        screen_label_navi_info2.set_text("米 进入")
        screen_label_navi_info2.set_long_mode(lv.label.LONG.WRAP)
        screen_label_navi_info2.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        # create style style_screen_label_navi_info2_main_main_default
        style_screen_label_navi_info2_main_main_default = lv.style_t()
        style_screen_label_navi_info2_main_main_default.init()
        style_screen_label_navi_info2_main_main_default.set_radius(0)
        style_screen_label_navi_info2_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_navi_info2_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_navi_info2_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_navi_info2_main_main_default.set_bg_opa(0)
        style_screen_label_navi_info2_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
        try:
            style_screen_label_navi_info2_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_navi_info2_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_navi_info2_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_navi_info2_main_main_default.set_text_letter_space(2)
        style_screen_label_navi_info2_main_main_default.set_pad_left(0)
        style_screen_label_navi_info2_main_main_default.set_pad_right(0)
        style_screen_label_navi_info2_main_main_default.set_pad_top(0)
        style_screen_label_navi_info2_main_main_default.set_pad_bottom(0)

        # add style for screen_label_navi_info2
        screen_label_navi_info2.add_style(style_screen_label_navi_info2_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_navi_next_road = lv.label(screen)
        screen_label_navi_next_road.set_pos(336,192)
        screen_label_navi_next_road.set_size(154,84)
        screen_label_navi_next_road.set_text("东四环中路辅路")
        screen_label_navi_next_road.set_long_mode(lv.label.LONG.WRAP)
        screen_label_navi_next_road.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)
        # create style style_screen_label_navi_next_road_main_main_default
        style_screen_label_navi_next_road_main_main_default = lv.style_t()
        style_screen_label_navi_next_road_main_main_default.init()
        style_screen_label_navi_next_road_main_main_default.set_radius(0)
        style_screen_label_navi_next_road_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_navi_next_road_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_navi_next_road_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_navi_next_road_main_main_default.set_bg_opa(0)
        style_screen_label_navi_next_road_main_main_default.set_text_color(lv.color_make(0xff,0xff,0xff))
        try:
            style_screen_label_navi_next_road_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_navi_next_road_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_navi_next_road_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_navi_next_road_main_main_default.set_text_letter_space(2)
        style_screen_label_navi_next_road_main_main_default.set_pad_left(0)
        style_screen_label_navi_next_road_main_main_default.set_pad_right(0)
        style_screen_label_navi_next_road_main_main_default.set_pad_top(0)
        style_screen_label_navi_next_road_main_main_default.set_pad_bottom(0)

        # add style for screen_label_navi_next_road
        screen_label_navi_next_road.add_style(style_screen_label_navi_next_road_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_gear_d = lv.label(screen)
        screen_label_gear_d.set_pos(320,112)
        screen_label_gear_d.set_size(32,20)
        screen_label_gear_d.set_text("D")
        screen_label_gear_d.set_long_mode(lv.label.LONG.WRAP)
        screen_label_gear_d.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        # create style style_screen_label_gear_d_main_main_default
        style_screen_label_gear_d_main_main_default = lv.style_t()
        style_screen_label_gear_d_main_main_default.init()
        style_screen_label_gear_d_main_main_default.set_radius(0)
        style_screen_label_gear_d_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_gear_d_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_gear_d_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_gear_d_main_main_default.set_bg_opa(0)
        style_screen_label_gear_d_main_main_default.set_text_color(lv.color_make(0x13,0x8e,0x91))
        try:
            style_screen_label_gear_d_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_gear_d_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_gear_d_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_gear_d_main_main_default.set_text_letter_space(2)
        style_screen_label_gear_d_main_main_default.set_pad_left(0)
        style_screen_label_gear_d_main_main_default.set_pad_right(0)
        style_screen_label_gear_d_main_main_default.set_pad_top(0)
        style_screen_label_gear_d_main_main_default.set_pad_bottom(0)

        # add style for screen_label_gear_d
        screen_label_gear_d.add_style(style_screen_label_gear_d_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_gear_t = lv.label(screen)
        screen_label_gear_t.set_pos(390,112)
        screen_label_gear_t.set_size(32,20)
        screen_label_gear_t.set_text("T")
        screen_label_gear_t.set_long_mode(lv.label.LONG.WRAP)
        screen_label_gear_t.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        # create style style_screen_label_gear_t_main_main_default
        style_screen_label_gear_t_main_main_default = lv.style_t()
        style_screen_label_gear_t_main_main_default.init()
        style_screen_label_gear_t_main_main_default.set_radius(0)
        style_screen_label_gear_t_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_gear_t_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_gear_t_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_gear_t_main_main_default.set_bg_opa(0)
        style_screen_label_gear_t_main_main_default.set_text_color(lv.color_make(0x13,0x8e,0x91))
        try:
            style_screen_label_gear_t_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_gear_t_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_gear_t_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_gear_t_main_main_default.set_text_letter_space(2)
        style_screen_label_gear_t_main_main_default.set_pad_left(0)
        style_screen_label_gear_t_main_main_default.set_pad_right(0)
        style_screen_label_gear_t_main_main_default.set_pad_top(0)
        style_screen_label_gear_t_main_main_default.set_pad_bottom(0)

        # add style for screen_label_gear_t
        screen_label_gear_t.add_style(style_screen_label_gear_t_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_label_gear_r = lv.label(screen)
        screen_label_gear_r.set_pos(460,112)
        screen_label_gear_r.set_size(32,20)
        screen_label_gear_r.set_text("R")
        screen_label_gear_r.set_long_mode(lv.label.LONG.WRAP)
        screen_label_gear_r.set_style_text_align(lv.TEXT_ALIGN.LEFT, 0)
        # create style style_screen_label_gear_r_main_main_default
        style_screen_label_gear_r_main_main_default = lv.style_t()
        style_screen_label_gear_r_main_main_default.init()
        style_screen_label_gear_r_main_main_default.set_radius(0)
        style_screen_label_gear_r_main_main_default.set_bg_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_gear_r_main_main_default.set_bg_grad_color(lv.color_make(0x21,0x95,0xf6))
        style_screen_label_gear_r_main_main_default.set_bg_grad_dir(lv.GRAD_DIR.VER)
        style_screen_label_gear_r_main_main_default.set_bg_opa(0)
        style_screen_label_gear_r_main_main_default.set_text_color(lv.color_make(0x13,0x8e,0x91))
        try:
            style_screen_label_gear_r_main_main_default.set_text_font(lv.font_HarmonyOS_Regular_20)
        except AttributeError:
            try:
                style_screen_label_gear_r_main_main_default.set_text_font(lv.font_montserrat_20)
            except AttributeError:
                style_screen_label_gear_r_main_main_default.set_text_font(lv.font_montserrat_16)
        style_screen_label_gear_r_main_main_default.set_text_letter_space(2)
        style_screen_label_gear_r_main_main_default.set_pad_left(0)
        style_screen_label_gear_r_main_main_default.set_pad_right(0)
        style_screen_label_gear_r_main_main_default.set_pad_top(0)
        style_screen_label_gear_r_main_main_default.set_pad_bottom(0)

        # add style for screen_label_gear_r
        screen_label_gear_r.add_style(style_screen_label_gear_r_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        screen_canvas_qrcode = lv.canvas(screen)
        screen_canvas_qrcode.set_pos(700,380)
        screen_canvas_qrcode.set_size(100,100)
        cbuf_screen_canvas_qrcode = bytearray(100 * 100 * 4)
        screen_canvas_qrcode.set_buffer(cbuf_screen_canvas_qrcode, 100, 100, lv.img.CF.TRUE_COLOR_ALPHA)
        screen_canvas_qrcode.fill_bg(lv.color_make(0xff,0xff,0xff), 255)
        # create style style_screen_canvas_qrcode_main_main_default
        style_screen_canvas_qrcode_main_main_default = lv.style_t()
        style_screen_canvas_qrcode_main_main_default.init()
        style_screen_canvas_qrcode_main_main_default.set_img_recolor(lv.color_make(0xff,0xff,0xff))
        style_screen_canvas_qrcode_main_main_default.set_img_recolor_opa(255)

        # add style for screen_canvas_qrcode
        screen_canvas_qrcode.add_style(style_screen_canvas_qrcode_main_main_default, lv.PART.MAIN|lv.STATE.DEFAULT)

        ################################################################## 以上代码从GUI Guide中复制出来的 ##################################################################

        # content from custom.py
        self.initIcons()
        self.updateSysTime(0)

        # Load the default screen
        lv.scr_load(screen)
        lv.tick_inc(5)
        lv.task_handler()



        log.d('ui init finished')
        while 1:
            lvgl_data = lvgl_queue.get()
            if not lvgl_data:
                continue

            if(lvgl_data[0] >= MSG_UI_MAX):
                log.d("control outsize:",lvgl_data[0])
                continue

            self.lvgl_handle_list[lvgl_data[0]](lvgl_data)
            # log.d('ui queue len : {}'.format(lvgl_queue.size()))
            # utime.sleep_ms(10)

    def lvgl_ui_init(self):
        lv.init()
        self.disp_buf1 = lv.disp_draw_buf_t()
        self.buf1_1 = bytes(480*800*2)
        self.disp_buf1.init(self.buf1_1, None, len(self.buf1_1))
        self.disp_drv = lv.disp_drv_t()
        self.disp_drv.init()
        self.disp_drv.draw_buf = self.disp_buf1
        self.disp_drv.flush_cb = self.mipilcd.lcd_write
        self.disp_drv.hor_res = 800
        self.disp_drv.ver_res = 480
        self.disp_drv.sw_rotate=1
        self.disp_drv.rotated = lv.DISP_ROT.NONE
        self.disp_drv.register()
        # lv.tick_inc(5)
        # lv.task_handler()

    def set_current_internal(self, current):
        global screen_label_current
        screen_label_current.set_text('{}'.format(current))
        # global screen_arc_current
        # max_current = 20
        # min_current = 0
        # max_current_angle = 266
        # min_current_angle = 150
        # screen_arc_current.set_end_angle(int(min_current_angle + (current * (max_current_angle - min_current_angle) / (max_current - min_current))))

    def set_current(self, data):
        current = data[1]
        log.d('set_current {}'.format(current))
        a = lv.anim_t()
        a.init()
        a.set_custom_exec_cb(lambda a,val: self.set_current_internal(val))
        a.set_values(self.curCurrent, current)
        a.set_time(200)
        a.set_repeat_count(1)
        a.start()
        self.curCurrent = current
        
    def set_current_noanim(self, data):
        current = data[1]
        log.d('set_current_noanim {}'.format(current))
        self.curCurrent = current
        self.set_current_internal(current)

    def set_battery_internal(self, batt):
        battPersents = batt
        if batt > 100:
            battPersents = 100
        elif batt < 0:
            battPersents = 0
        global screen_bar_battery
        screen_bar_battery.set_value(battPersents, lv.ANIM.OFF)
        global screen_img_batt_ind
        x = int(300 + battPersents * 2)
        screen_img_batt_ind.set_pos(x,442)

        # global screen_arc_battery
        # global screen_label_battery
        # global screen_label_battery_percent
        # max_batt = 100
        # min_batt = 0
        # max_batt_angle = 280
        # min_batt_angle = 50 + 360
        # screen_label_battery.set_text('{}'.format(batt))
        # if batt > 99:
        #     screen_label_battery_percent.set_pos(700,224)
        # else:
        #     screen_label_battery_percent.set_pos(685,224)
        # screen_arc_battery.set_end_angle(int(min_batt_angle + (batt * (max_batt_angle - min_batt_angle) / (max_batt - min_batt))))

    def set_battery(self, data):
        batt = data[1]
        log.d('set_battery {}'.format(batt))
        a = lv.anim_t()
        a.init()
        a.set_custom_exec_cb(lambda a,val: self.set_battery_internal(val))
        a.set_values(self.curBatt, batt)
        a.set_time(200)
        a.set_repeat_count(1)
        a.start()
        self.curBatt = batt
        
    def set_battery_noanim(self, data):
        batt = data[1]
        log.d('set_battery_noanim {}'.format(batt))
        self.curBatt = batt
        self.set_battery_internal(batt)

    def set_speed_internal(self, speed):
        global screen_label_speed
        screen_label_speed.set_text('{}'.format(speed))
        # global screen_arc_speed
        # max_speed = 120
        # min_speed = 0
        # max_speed_angle = 360
        # min_speed_angle = 100
        # screen_arc_speed.set_end_angle(int(min_speed_angle + (speed * (max_speed_angle - min_speed_angle) / (max_speed - min_speed))))

    def set_speed(self, data):
        speed = data[1]
        log.d('set_speed {}'.format(speed))
        a = lv.anim_t()
        a.init()
        a.set_custom_exec_cb(lambda a,val: self.set_speed_internal(val))
        a.set_values(self.curSpeed, speed)
        a.set_time(200)
        a.set_repeat_count(1)
        a.start()
        self.curSpeed = speed

    def set_speed_noanim(self, data):
        speed = data[1]
        log.d('set_speed_noanim {}'.format(speed))
        self.curSpeed = speed
        self.set_speed_internal(speed)


    def set_gear(self, data):
        global screen_label_gear_d
        global screen_label_gear_t
        global screen_label_gear_r
        screen_label_gear_d.set_style_text_color(lvgl_white, 0)
        screen_label_gear_t.set_style_text_color(lvgl_white, 0)
        screen_label_gear_r.set_style_text_color(lvgl_white, 0)
        if (data[1] == 0):
            #self.set_ready([0, 'P'])
            pass
        elif (data[1] == 1) :
            #self.set_ready([0, 'Ready'])
            screen_label_gear_d.set_style_text_color(lvgl_text_main_color, 0)
        elif (data[1] == 2):
            #self.set_ready([0, 'Ready'])
            screen_label_gear_d.set_style_text_color(lvgl_text_main_color, 0)
        elif (data[1] == 3):
            #self.set_ready([0, 'Ready'])
            screen_label_gear_d.set_style_text_color(lvgl_text_main_color, 0)
        elif (data[1] == 4):
            #self.set_ready([0, 'Ready'])
            screen_label_gear_t.set_style_text_color(lvgl_text_main_color, 0)
        elif (data[1] == 5):
            #self.set_ready([0, 'Ready'])
            screen_label_gear_r.set_style_text_color(lvgl_text_main_color, 0)
        elif (data[1] == 6):
            #self.set_ready([0, 'Ready'])
            screen_label_gear_d.set_style_text_color(lvgl_text_main_color, 0)

    def set_trip(self, data):
        global screen_label_trip
        screen_label_trip.set_text(('{:0>3d}'.format(int(data[1]))))
    
    def set_leftkm(self, data):
        global screen_label_left_km
        screen_label_left_km.set_text(('{:0>3d}'.format(int(data[1]))))

    def set_odo(self, data):
        global screen_label_odo
        screen_label_odo.set_text(('{:0>4d}'.format(int(data[1]))))
    
    def set_time(self, data):
        global screen_label_time
        curTime = utime.localtime()
        timeStr = '{:0>2d}:{:0>2d}'.format(curTime[3], curTime[4])
        screen_label_time.set_text(('{}'.format(timeStr)))

    def hide_navi(self, data):
        self.hideNaviInfo()
    
    def set_ready(self, data):
        global screen_label_ready
        screen_label_ready.set_text(('{}'.format(data[1])))
    
    def set_mobile_signal(self, data):
        #TODO
        pass
    
    def set_gps(self, data):
        global screen_img_gps
        if data[1] == True :
            screen_img_gps.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_gps.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_bt(self, data):
        global screen_img_bt
        if data[1] == True :
            screen_img_bt.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_bt.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_light_left(self, data):
        global screen_img_light_left
        if data[1] == True :
            screen_img_light_left.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_light_left.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_light_right(self, data):
        global screen_img_light_right
        if data[1] == True :
            screen_img_light_right.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_light_right.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_light_far(self, data):
        global screen_img_light_far
        if data[1] == True :
            screen_img_light_far.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_light_far.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_light_near(self, data):
        global screen_img_light_near
        if data[1] == True :
            screen_img_light_near.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_light_near.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_light_auto(self, data):
        global screen_img_light_auto
        if data[1] == True :
            screen_img_light_auto.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_light_auto.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_light_small(self, data):
        global screen_img_light_small
        if data[1] == True :
            screen_img_light_small.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_light_small.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_light_doubleflash(self, data):
        global screen_img_light_double_flash
        if data[1] == True :
            screen_img_light_double_flash.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_light_double_flash.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_auto_speed(self, data):
        global screen_img_auto_speed
        if data[1] == True :
            screen_img_auto_speed.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_auto_speed.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_warning(self, data):
        global screen_img_warning
        if data[1] == True :
            screen_img_warning.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_warning.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_batt_warning(self, data):
        global screen_img_batt_warning
        if data[1] == True :
            screen_img_batt_warning.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_batt_warning.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_eco(self, data):
        global screen_img_eco
        if data[1] == True :
            screen_img_eco.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_eco.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_charging(self, data):
        global screen_img_charging
        if data[1] == True :
            screen_img_charging.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_charging.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_not_sit(self, data):
        global screen_img_not_sit
        if data[1] == True :
            screen_img_not_sit.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_not_sit.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_biancheng(self, data):
        global screen_img_biancheng
        if data[1] == True :
            screen_img_biancheng.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_biancheng.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_unbind(self, data):
        global screen_img_unbind
        if data[1] == True :
            screen_img_unbind.clear_flag(lv.obj.FLAG.HIDDEN)
        else:
            screen_img_unbind.add_flag(lv.obj.FLAG.HIDDEN)
    
    def set_navi_info(self, data):
        global screen_img_navi_info
        global screen_label_navi_info2
        global screen_label_navi_dist
        global screen_label_navi_next_road
        if len(data) < 4:
            return
        icon_type = int(data[1])
        next_dist = int(data[2])
        next_road = data[3]
        if next_dist < 1000 :
            screen_label_navi_dist.set_text('{}'.format(next_dist))
            screen_label_navi_info2.set_text('米 进入')
        else:
            screen_label_navi_dist.set_text('{:.1f} km'.format(next_dist / 1000))
            screen_label_navi_info2.set_text('公里 进入')
        screen_label_navi_next_road.set_text('{}'.format(next_road))
        screen_img_navi_info.set_src('U:/images2/action{}.png'.format(icon_type))
        self.showNaviInfo()
        self.naviTimer.stop()
        self.naviTimer.start(NAVI_TIMEOUT_MS, 0, self.onNaviTimeout)

    def hideNaviInfo(self):
        global screen_img_navi_info
        global screen_label_navi_dist
        global screen_label_navi_next_road
        global screen_label_navi_info2
        global screen_img_bg_gear
        screen_img_navi_info.add_flag(lv.obj.FLAG.HIDDEN)
        screen_label_navi_dist.add_flag(lv.obj.FLAG.HIDDEN)
        screen_label_navi_next_road.add_flag(lv.obj.FLAG.HIDDEN)
        screen_label_navi_info2.add_flag(lv.obj.FLAG.HIDDEN)
        screen_img_bg_gear.clear_flag(lv.obj.FLAG.HIDDEN)
        screen_label_gear_d.clear_flag(lv.obj.FLAG.HIDDEN)
        screen_label_gear_t.clear_flag(lv.obj.FLAG.HIDDEN)
        screen_label_gear_r.clear_flag(lv.obj.FLAG.HIDDEN)

    def onNaviTimeout(self, a):
        print('--callback start-- onNaviTimeout')
        self.lvgl_queue_put([MSG_UI_HIDE_NAVI, ])
        print('--callback end-- onNaviTimeout')

    def showNaviInfo(self):
        global screen_img_navi_info
        global screen_label_navi_dist
        global screen_label_navi_next_road
        global screen_label_navi_info2
        global screen_img_bg_gear
        screen_img_navi_info.clear_flag(lv.obj.FLAG.HIDDEN)
        screen_label_navi_dist.clear_flag(lv.obj.FLAG.HIDDEN)
        screen_label_navi_next_road.clear_flag(lv.obj.FLAG.HIDDEN)
        screen_label_navi_info2.clear_flag(lv.obj.FLAG.HIDDEN)
        screen_img_bg_gear.add_flag(lv.obj.FLAG.HIDDEN)
        screen_label_gear_d.add_flag(lv.obj.FLAG.HIDDEN)
        screen_label_gear_t.add_flag(lv.obj.FLAG.HIDDEN)
        screen_label_gear_r.add_flag(lv.obj.FLAG.HIDDEN)

    def updateSysTime(self,a):
        print('--callback start-- updateSysTime')
        self.lvgl_queue_put([MSG_UI_SET_TIME, ])
        print('--callback end-- updateSysTime')

    def hideQrCode(self):
        global screen_canvas_qrcode
        screen_canvas_qrcode.add_flag(lv.obj.FLAG.HIDDEN)
        
    def drawQrCode(self):
        global screen_canvas_qrcode
        screen_canvas_qrcode.clear_flag(lv.obj.FLAG.HIDDEN)

    def lvgl_queue_put(self,data):
        global lvgl_queue
        if lvgl_queue is not None:
            lvgl_queue.put(data)

    def initIcons(self):
        log.d('start init icons')
        self.set_speed_noanim([0, 0])
        self.set_current_noanim([0, 0])
        self.set_battery_noanim([0, 100])
        self.set_trip([0, 0])
        self.set_odo([0, 0])
        self.set_leftkm([0, 0])
        self.set_light_left([0, False])
        self.set_light_right([0, False])
        self.set_light_far([0, False])
        self.set_light_near([0, False])
        self.set_light_auto([0, False])
        self.set_light_small([0, False])
        self.set_light_doubleflash([0, False])
        self.set_auto_speed([0, False])
        self.set_warning([0, False])
        self.set_batt_warning([0, False])
        self.set_eco([0, False])
        self.set_charging([0, False])
        self.set_not_sit([0, False])
        self.set_biancheng([0, False])
        self.set_unbind([0, False])
        self.set_bt([0, False])
        self.set_gps([0, False])
        self.hideNaviInfo()
        self.hideQrCode()
        utime.sleep_ms(100)
        log.d('init icons finish')

    def turnLcdOn(self):
        self.icn6211.lcd_on()
        # self.screen_backlight.write(1)

    def turnLcdOff(self):
        self.icn6211.lcd_off()
        # self.screen_backlight.write(0)

if __name__ == '__main__':
    ui = UI_lvgl(None)