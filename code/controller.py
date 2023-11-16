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
import osTimer
import ustruct


CONTROLLER_STATE_INIT = 0
CONTROLLER_STATE_RUNNING = 1
CONTROLLER_STATE_OFFLINE = 2
CONTROLLER_STATE_STOPPED = 3

CONTROLLER_INIT_POLL_MS = 1000 # 查询设备信息的时间间隔
CONTROLLER_RUNNING_POLL_MS = 500 # 查询实时信息的时间间隔
CONTROLLER_OFFLINE_POLL_MS = 5000 # 掉线后重新查询的时间间隔

CONTROLLER_TIMEOUT_MS = 10000 # 超时时间


# class ControllerBean:
#     def __init__(self):
#         self.addr = None
#         self.subAddr = None
#         self.bufferLen = 0
#         self.msgLen = 0
#         self.data = None
#         self.sum = None
#         self.isValid = False
#         self.cmd = None
#         self.cmdValue = None
#         self.success = 0

#     def checkAddr(self, buffer):
#         if len(buffer) > 2:
#             if buffer[0] == 0x02 and (buffer[1] == 0x03 or buffer[1] == 0x01): # 控制器地址
#                 return True
#         return False

#     def fromBytes(self, buffer):
#         self.bufferLen = len(buffer)
#         if (self.bufferLen < 6):
#             return
#         self.isValid = True
#         self.addr, = ustruct.unpack('<H', buffer[:2])
#         if (self.addr == 0x0302):
#             mLen, = ustruct.unpack('<H', buffer[2:4])
#             self.msgLen = self.bufferLen - 6
#             if self.msgLen < 0:
#                 return
#             if (mLen != self.msgLen):
#                 self.isValid = False
#                 return
#             self.data = buffer[4:-2]
#             self.sum, = ustruct.unpack('<H', buffer[-2:])
#         elif (self.addr == 0x0102):
#             self.cmd, self.msgLen = ustruct.unpack('<2B', buffer[2:4])
#             self.data = buffer[4:-2]
#         if not self.checkSum():
#             self.isValid = False

#     def toBytes(self):
#         if self.addr == 0x0302:
#             format = '<3H{}sH'.format(self.msgLen)
#             self.calcSum()
#             buffer = ustruct.pack(format, self.addr, self.subAddr, self.msgLen, self.data, self.sum)
#             return buffer
#         elif self.addr == 0x0102:
#             self.calcSum()
#             buffer = ustruct.pack('H3BH', self.addr, self.cmd, self.msgLen, self.cmdValue, self.sum)
#             return buffer

#     def checkSum(self):
#         return True

#     def calcSum(self):
#         self.sum = 0

class Controller:
    def __init__(self, serial, mmi):
        self.mmi = mmi
        self.serial = serial
        self.state = CONTROLLER_STATE_INIT
        self.timeoutCount = 0
        self.timer = osTimer()
        self.timeoutTimer = osTimer()
    
    def start(self):
        print('controller start')
        self.state = CONTROLLER_STATE_INIT
        self.timer.start(CONTROLLER_INIT_POLL_MS, 1, self.onTimer)

    def stop(self):
        self.state = CONTROLLER_STATE_STOPPED
        self.timer.stop()
        self.timeoutTimer.stop()

    def getInfo(self):
        # cb = ControllerBean()
        # cb.addr = 0x0302
        # cb.subAddr = 0xE002
        # cb.msgLen = 0
        # cb.calcSum()
        # dataBuffer = cb.toBytes()
        dataBuffer = bytearray(8)
        dataBuffer[0] = 0x02
        dataBuffer[1] = 0x03
        dataBuffer[2] = 0x02
        dataBuffer[3] = 0xE0
        dataBuffer[4] = 0x00
        dataBuffer[5] = 0x00
        dataBuffer[6] = 0xE7
        dataBuffer[7] = 0x10
        self.timeoutTimer.start(CONTROLLER_TIMEOUT_MS, 0, self.onTimeout)
        self.serial.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_485, dataBuffer])

    def onGotInfo(self, data):
        # cb = ControllerBean()
        # cb.fromBytes(data)
        if len(data) != 35:
            print('on got controller info length error')
            return
        self.state = CONTROLLER_STATE_RUNNING
        self.timer.stop()
        self.timer.start(CONTROLLER_RUNNING_POLL_MS, 1, self.onTimer)
        self.timeoutTimer.stop()
        if self.mmi == None:
            print('no mmi, cannot update info!')
            return
        g_status = self.mmi.getGStatus()
        g_status.motor_status.hw_version = data[4] # 硬件版本序号
        g_status.motor_status.hw_manufacturer = data[5] # 硬件厂商代码
        g_status.motor_status.hw_code = data[7] # 硬件识别码
        g_status.motor_status.sw_sub_version = data[8] # 次软件版本号
        g_status.motor_status.sw_version = data[9] # 主软件版本号
        g_status.motor_status.sw_model = data[10] # 产品型号
        g_status.motor_status.sw_code = data[11] # 软件识别码
        g_status.motor_status.sw_boot_version = data[12] + (data[13] << 8) # BOOT底层软件版本
        g_status.motor_status.sw_boot_upgrade_version = data[14] # BOOT升级协议版本
        g_status.motor_status.protocal_sub_version = data[15] # 次通信协议版本
        g_status.motor_status.protocal_version = data[16] # 主通信协议版本
        g_status.motor_status.custom_code = data[21] + (data[22] << 8) # 客户代码
        g_status.motor_status.manufacturer = data[23] + (data[24] << 8) # 设计厂家
        g_status.motor_status.spec = data[25] + (data[26] << 8) # 产品规格
        g_status.motor_status.controller_manufacturer = data[27] + (data[28] << 8) # 控制器生产厂家

    def getRealtimeInfo(self):
        # cb = ControllerBean()
        # cb.addr = 0x0302
        # cb.subAddr = 0xE003
        # cb.msgLen = 0
        # cb.calcSum()
        # dataBuffer = cb.toBytes()
        dataBuffer = bytearray(8)
        dataBuffer[0] = 0x02
        dataBuffer[1] = 0x03
        dataBuffer[2] = 0x03
        dataBuffer[3] = 0xE0
        dataBuffer[4] = 0x00
        dataBuffer[5] = 0x00
        dataBuffer[6] = 0xE8
        dataBuffer[7] = 0x10
        self.timeoutTimer.start(CONTROLLER_TIMEOUT_MS, 0, self.onTimeout)
        self.serial.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_485, dataBuffer])

    def onGotRealtimeInfo(self, data):
        if len(data) != 29:
            print('on got controller real time info length error')
            return
        self.timeoutTimer.stop()
        i = 4
        if self.mmi == None:
            print('no mmi, cannot update ui!')
            return
        g_status = self.mmi.getGStatus()
        g_status.motor_status.gear = data[i] & 0x0F # 档位 0x0:P 档 0x1:低速档（D1） 0x2:中速档（D2） 0x3:高速档（D3） 0x4:助力推行档（T） 0x5:倒车辅助档（R） 0x6：D 档（电自） 0x7～F:Reserved
        g_status.motor_status.auto_pilot = (data[i] >> 4) & 0x03 # 定时巡航状态 0-禁用; 1-启动; 2-未启动
        g_status.motor_status.voltage_mode = (data[i] >> 6) & 0x03 # 当前电压模式 0-48V; 1-60V; 2-72V; 
        i += 1
        g_status.motor_status.zhuanba_status = ((data[i] & 0x01) != 0) # 转把状态 0-空闲; 1-工作;
        g_status.motor_status.motor_lock_status = ((data[i] & 0x02) != 0) # 0-解锁; 1-上锁;
        g_status.motor_status.biancheng_status = (data[i] >> 2) & 0x03 # 0- 边撑感应禁用; 1-边撑打开; 2-边撑收起;
        g_status.motor_status.sitdown_status = (data[i] >> 4) & 0x03 # 0- 坐垫感应禁用; 1-没坐人; 2- 坐人
        g_status.motor_status.charging = ((data[i] & 0x40) != 0) # 是否在整车充电
        g_status.motor_status.speed_limit = ((data[i] & 0x80) != 0) # 是否限速
        i += 1
        g_status.motor_status.eco = ((data[i] & 0x01) != 0) # 是否最佳能耗
        g_status.motor_status.wheel_move = ((data[i] & 0x02) != 0) # 轮动信号, 轮子是否在动
        g_status.motor_status.motor_move = (data[i] >> 2) & 0x03 # 0-电机停止; 1-正转; 2-反转
        g_status.motor_status.p_mode = ((data[i] & 0x10) != 0) # 是否启用驻车模式
        g_status.motor_status.controller_error = ((data[i] & 0x20) != 0) # 控制器是否故障
        g_status.motor_status.break_mode = ((data[i] & 0x40) != 0) # 是否正在刹车
        g_status.motor_status.speed_limit_enable = ((data[i] & 0x80) != 0) # 是否启用限速功能
        i += 1
        g_status.motor_status.accelerator = data[i] # 油门开度 0 - 未开; 0x00-0xFE-开度程度; 0xFF-满开
        i += 1
        i += 1
        g_status.motor_status.r_speed = data[i] # 0x00:辅助倒车功能禁用 0x01～0x0F:倒车最高设 定速度（当设置为0x0F 时， 转把可控制的速度为全速 的 15%） 出厂默认值：10%
        i += 1
        g_status.motor_status.t_speed = data[i] # 0x00:助力推行功能禁用 0x01～0x0F:助力推行最 高设定速度（当设置为 0x0F 时，转把可控制的速 度为全速的 15%） 出厂默认值：13%
        i += 1
        g_status.motor_status.d1_speed = data[i] # 0x05～0x64:速度上限阈值 (当设置为 0x10 时，转 把可控制的速度为全速的 16%)
        i += 1
        g_status.motor_status.d2_speed = data[i] # 0x05～0x64:速度上限阈值 (当设置为 0x10 时，转 把可控制的速度为全速的 16%)
        i += 1
        g_status.motor_status.d3_speed = data[i] # 0x05～0x64:速度上限阈值 (当设置为 0x10 时，转 把可控制的速度为全速的 16%)
        i += 1
        g_status.motor_status.motor_temp = data[i] # 电机温度
        i += 1
        g_status.motor_status.controller_temp = data[i] # 控制器温度
        i += 1
        g_status.motor_status.voltage = data[i] + (data[i+1] << 8) # 直流电压 0.1v
        i += 2
        g_status.motor_status.current = data[i] + (data[i+1] << 8) # 电机电流 0.1A
        i += 2
        g_status.motor_status.wheel_r = data[i] # 轮半径
        i += 1
        i += 2
        g_status.motor_status.hall_error = ((data[i] & 0x01) != 0) # 是否有霍尔故障
        g_status.motor_status.biancheng_error = ((data[i] & 0x02) != 0) # 是否有边撑故障
        g_status.motor_status.sitdown_error = ((data[i] & 0x04) != 0) # 是否有坐垫感应故障
        g_status.motor_status.zhuanba_error = ((data[i] & 0x08) != 0) # 是否有转把故障
        g_status.motor_status.phase_current_error = ((data[i] & 0x10) != 0) # 是否有相电流过流故障
        g_status.motor_status.voltage_error = ((data[i] & 0x20) != 0) # 是否有电压故障
        g_status.motor_status.motor_overtemp = ((data[i] & 0x40) != 0) # 是否电机过温
        g_status.motor_status.controller_overtemp = ((data[i] & 0x80) != 0) # 是否控制器过温
        i += 1
        g_status.motor_status.phase_current_overflow = ((data[i] & 0x01) != 0) # 是否相电流溢出
        g_status.motor_status.phase_current_zero_error = ((data[i] & 0x02) != 0) # 是否相电流零点故障
        g_status.motor_status.phase_current_short_error = ((data[i] & 0x04) != 0) # 是否相电流短路故障
        g_status.motor_status.line_current_zero_error = ((data[i] & 0x08) != 0) # 是否线电流零点故障
        g_status.motor_status.mosfet_up_error = ((data[i] & 0x10) != 0) # 是否上桥故障
        g_status.motor_status.mosfet_down_error = ((data[i] & 0x20) != 0) # 是否下桥故障
        g_status.motor_status.max_current_error = ((data[i] & 0x40) != 0) # 是否峰值电流保护故障
        g_status.motor_status.rest_flag = ((data[i] & 0x80) != 0) # 0x0:收到中控批量设置命 令后置 0 0x1:表示ACC 重新上电 或电控重启，收到批量设 置命令后，将此标志位置 0
        i += 1
        g_status.motor_status.hall = data[i] + (data[i+1] << 8) # 用于计算转速 转速（m/s）=（500Ms 霍 尔个数*2）/（6*极对数）* 周长（米）
        self.mmi.mmi_queue_put([MSG_MMI_UPDATE_UI, UI_TYPE_CONTROLLER])

    def onGotData(self, data):
        self.timeoutCount = 0
        if not self.isValid(data):
            print('on got not valid controller data')
            return
        if data[0] == 0x02 and data[1] == 0x03:
            if (self.state == CONTROLLER_STATE_INIT or self.state == CONTROLLER_STATE_OFFLINE):
                self.onGotInfo(data)
            elif (self.state == CONTROLLER_STATE_RUNNING):
                self.onGotRealtimeInfo(data)
        elif data[0] == 0x02 and data[1] == 0x01:
            pass # 写参数的返回

    def onTimer(self, a):
        print('STATE : {}'.format(self.state))
        if (self.state == CONTROLLER_STATE_INIT or self.state == CONTROLLER_STATE_OFFLINE):
            self.getInfo()
        elif (self.state == CONTROLLER_STATE_RUNNING):
            self.getRealtimeInfo()
            
    def onTimeout(self, a):
        self.timeoutCount = self.timeoutCount + 1
        if (self.timeoutCount >= 3) :
            self.state = CONTROLLER_STATE_OFFLINE
            self.timeoutCount = 0
            self.timer.stop()
            self.timer.start(CONTROLLER_OFFLINE_POLL_MS, 1, self.onTimer)


    def checksum(self, data): #TODO
        return True

    def isValid(self, data):
        # if self.buffer[0] != 0x02:
        #     return False
        if not self.checksum(data):
            return False
        return True

    def checkAddr(self, buffer):
        if len(buffer) > 2:
            if buffer[0] == 0x02 and (buffer[1] == 0x03 or buffer[1] == 0x01): # 控制器地址
                return True
        return False




if __name__ == '__main__':
    controller = Controller(None)