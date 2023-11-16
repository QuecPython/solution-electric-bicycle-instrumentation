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
import utime
import _thread
import gc
import log
from usr.const import *
from usr.utils.log import log

class UI_DEMO:
    def __init__(self, ui, mmi):
        self.ui = ui
        self.mmi = mmi
        self.speed = 0
        self.current = 0

    def start(self):
        self.isRunning = True
        self.isPause = False
        _thread.start_new_thread(self.ui_demo_thread,(THREAD_ID_UI_DEMO,))

    def resume(self):
        if not self.isRunning:
            return
        self.isPause = False

    def pause(self):
        if not self.isRunning:
            return
        self.isPause = True

    def stop(self):
        self.isRunning = False
        _thread.stop_thread(THREAD_ID_UI_DEMO)

    def clearSpeed(self):
        self.speed = 0
        self.ui.lvgl_queue_put([MSG_UI_SET_SPEED, self.speed])
        self.current = 0
        self.ui.lvgl_queue_put([MSG_UI_SET_CURRENT, int(self.current)])

    def ui_demo_thread(self, thread_id):
        for i in range(5):
            self.ui.lvgl_queue_put([MSG_UI_SET_LIGHT_LEFT, True])
            self.ui.lvgl_queue_put([MSG_UI_SET_LIGHT_RIGHT, True])
            utime.sleep_ms(500)
            self.ui.lvgl_queue_put([MSG_UI_SET_LIGHT_LEFT, False])
            self.ui.lvgl_queue_put([MSG_UI_SET_LIGHT_RIGHT, False])
            utime.sleep_ms(500)
        self.ui.lvgl_queue_put([MSG_UI_SET_LIGHT_SMALL, True])
        self.ui.lvgl_queue_put([MSG_UI_SET_LIGHT_NEAR, True])

        self.speed = 0
        speed_step = 1

        self.current = 0.0
        current_step = 0.2

        trip = 0.0
        trip_step = 0.1

        leftkm = 100.0
        leftkm_step = -0.1

        battery = 100.0
        battery_step = -0.1

        while self.isRunning:
            g_status = self.mmi.getGStatus()
            # if self.isPause or g_status.lock_mode != MODE_UNLOCK:
            if g_status.lock_mode != MODE_UNLOCK:
                utime.sleep_ms(500)
                continue
            # 速度演示
            self.speed = self.speed + speed_step
            if self.speed > 96 :
                speed_step = -1
            elif self.speed < 40 :
                speed_step = 1
            self.ui.lvgl_queue_put([MSG_UI_SET_SPEED, self.speed])
            # self.ui.set_speed_noanim([MSG_UI_SET_SPEED, self.speed])

            # 电流演示
            self.current = self.current + current_step
            if self.current > 20 :
                current_step = -0.2
            elif self.current < 5 :
                current_step = 0.2
            self.ui.lvgl_queue_put([MSG_UI_SET_CURRENT, int(self.current)])
            # self.ui.set_current_noanim([MSG_UI_SET_CURRENT, int(self.current)])

            # 里程演示
            trip = trip + trip_step
            self.ui.lvgl_queue_put([MSG_UI_SET_TRIP, int(trip)])
            # self.ui.set_trip([MSG_UI_SET_TRIP, int(trip)])
            self.ui.lvgl_queue_put([MSG_UI_SET_ODO, int(trip + 1000)])

            # 电量演示
            battery = battery + battery_step
            if battery < 0 :
                battery = 0
            self.ui.lvgl_queue_put([MSG_UI_SET_BATTERY, int(battery)])
            # self.ui.set_battery_noanim([MSG_UI_SET_BATTERY, int(battery)])
            
            # 剩余里程演示
            leftkm = leftkm + leftkm_step
            if leftkm < 0 :
                leftkm = 0
            self.ui.lvgl_queue_put([MSG_UI_SET_LEFTKM, int(leftkm)])
            # self.ui.set_leftkm([MSG_UI_SET_LEFTKM, int(leftkm)])

            utime.sleep_ms(300)
            #mem = gc.mem_free()
            #log.d('free RAM: -------------------  {}  KB'.format(int(mem / 1024)))



if __name__ == '__main__':
    demo = UI_DEMO(ui)
    demo.start()
