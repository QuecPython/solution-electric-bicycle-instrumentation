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
from usr.const import *
import utime
import _thread
import queue
import sys_bus
from machine import UART
from gnss import GnssGetData
from usr.drivers.enpin import gpio_en
from usr.utils.log import log

GPS_UPDATE_INTERVAL_WHILE_LOCK_SEC = 60
GPS_UPDATE_INTERVAL_WHILE_UNLOCK_SEC = 5

class GPS:
    def __init__(self, mmi):
        self.mmi = mmi
        self.interval = GPS_UPDATE_INTERVAL_WHILE_UNLOCK_SEC
        _thread.start_new_thread(self.gps_task,(THREAD_ID_GPS,))

    def gps_task(self, thread_id):
        log.d("gps_task id %d" % thread_id)
        sys_bus.subscribe('LOCK_MODE', self.onBusMsg)

        self.gps_en = gpio_en(GPS_EN_PIN, 0, "gps_en")
        self.gps_en.enable()
        self.gnss = GnssGetData(UART.UART1, 9600, 8, 0, 1, 0)
        self.gnss.read_gnss_data(max_retry=1, debug=0)
        data = self.gnss.getOriginalData()
        log.i('---GPS----', data)
        # global gpsQueue
        # gpsQueue = queue.Queue(30)
        # self.msg_type_handle_func = (self.xxx,)
        while 1:
            self.gnss.read_gnss_data(max_retry=1, debug=0)
            # data = self.gnss.getOriginalData()
            # log.d(data)
            sat_count_v = self.gnss.getViewedSateCnt()
            sat_count_u = self.gnss.getUsedSateCnt()
            loc = self.gnss.getLocation()
            height = self.gnss.getGeodeticHeight()
            speed = self.gnss.getSpeed()
            log.i('经纬度：{}  海拔：{} 速度：{} 可见卫星数量：{} 使用卫星数量：{}'.format(loc, height, speed, sat_count_v, sat_count_u))
            utime.sleep(self.interval)
            g_status = self.mmi.getGStatus()
            g_status.latlng = loc
            # gps_data = gpsQueue.get()
            # if (gps_data[0] >= GPS_MSG_MAX):
            #     continue
            # self.msg_type_handle_func[gps_data[0]](gps_data)

    def onBusMsg(self, topic, msg):
        if topic == 'LOCK_MODE':
            if msg == MODE_LOCK or msg == MODE_READY_TO_LOCK:
                self.interval = GPS_UPDATE_INTERVAL_WHILE_UNLOCK_SEC
            elif msg == MODE_UNLOCK or msg == MODE_READY_TO_UNLOCK:
                self.interval = GPS_UPDATE_INTERVAL_WHILE_LOCK_SEC

if __name__ == '__main__':
    gps = GPS(None)