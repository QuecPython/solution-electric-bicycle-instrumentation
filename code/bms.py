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

BMS_STATE_INIT = 0
BMS_STATE_READING_SN = 1
BMS_STATE_RUNNING = 2
BMS_STATE_OFFLINE = 3
BMS_STATE_STOPPED = 4

BMS_INIT_POLL_MS = 500 # 查询设备信息的时间间隔
BMS_READING_SN_POLL_MS = 500 # 查询设备信息的时间间隔
BMS_RUNNING_POLL_MS = 500 # 查询实时信息的时间间隔
BMS_OFFLINE_POLL_MS = 2000 # 掉线后重新查询的时间间隔

BMS_TIMEOUT_MS = 300 # 超时时间



class BMS:
    def __init__(self, serial, mmi):
        self.mmi = mmi
        self.serial = serial
        self.state = BMS_STATE_INIT
        self.timeoutCount = 0
        self.timer = osTimer()
        self.timeoutTimer = osTimer()

    

        # #self.buffer = buffer
        # self.is_valid = False
        # self.cmd_id = None
        # self.body = None
        # self.fromBytes()
    
    def start(self):
        self.state = BMS_STATE_INIT
        self.timer.start(BMS_INIT_POLL_MS, 1, self.onTimer)

    def stop(self):
        self.state = BMS_STATE_STOPPED
        self.timer.stop()
        self.timeoutTimer.stop()

    def getInfo(self):
        dataBuffer = bytearray(8)
        dataBuffer[0] = 0x03
        dataBuffer[1] = 0x03
        dataBuffer[2] = 0x00
        dataBuffer[3] = 0xE0
        dataBuffer[4] = 0x00
        dataBuffer[5] = 0x00
        dataBuffer[6] = 0xE6
        dataBuffer[7] = 0x00
        self.timeoutTimer.start(BMS_TIMEOUT_MS, 0, self.onTimeout)
        self.serial.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_485, dataBuffer])

    def onGotInfo(self, data):
        if len(data) != 36:
            print('on got bms info length error')
            return
        self.state = BMS_STATE_READING_SN
        self.timer.stop()
        self.timer.start(BMS_READING_SN_POLL_MS, 1, self.onTimer)
        self.timeoutTimer.stop()
        global g_status
        g_status.bms_status.hw_version = data[4] # 硬件版本序号
        g_status.bms_status.hw_manufacturer = data[5] # 硬件厂商代码
        g_status.bms_status.hw_code = data[7] # 硬件识别码
        g_status.bms_status.sw_sub_version = data[8] # 次软件版本号
        g_status.bms_status.sw_version = data[9] # 主软件版本号
        g_status.bms_status.sw_model = data[10] # 产品型号
        g_status.bms_status.sw_code = data[11] # 软件识别码
        g_status.bms_status.sw_boot_version = data[12] # BOOT底层软件版本
        g_status.bms_status.sw_boot_upgrade_version = data[13] # BOOT升级协议版本
        g_status.bms_status.protocal_sub_version = data[14] # 次通信协议版本
        g_status.bms_status.protocal_version = data[15] # 主通信协议版本
        g_status.bms_status.custom_code = data[20] + (data[21] << 8) # 客户代码
        g_status.bms_status.manufacturer = data[22] + (data[23] << 8) # 设计厂家
        g_status.bms_status.spec = data[24] + (data[25] << 8) # 产品规格
        g_status.bms_status.controller_manufacturer = data[26] + (data[27] << 8) # 控制器生产厂家
        
        g_status.bms_status.rated_voltage = data[28] + (data[29] << 8) # 电池额定电压 V
        g_status.bms_status.rated_ah = data[30] # 电池额定容量 AH
        g_status.bms_status.batt_cell_s_num = data[31] # 电池电芯串联级数
        g_status.bms_status.batt_cell_p_num = data[32] # 电池电芯并联级数
        g_status.bms_status.batt_cell_temp_sensor_num = data[33] & 0x0F # 电池电芯温度传感器数量



    def getRealtimeInfo(self):
        dataBuffer = bytearray(8)
        dataBuffer[0] = 0x03
        dataBuffer[1] = 0x03
        dataBuffer[2] = 0x01
        dataBuffer[3] = 0xE0
        dataBuffer[4] = 0x00
        dataBuffer[5] = 0x00
        dataBuffer[6] = 0xE7
        dataBuffer[7] = 0x00
        self.timeoutTimer.start(BMS_TIMEOUT_MS, 0, self.onTimeout)
        self.serial.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_485, dataBuffer])

    def onGotRealtimeInfo(self, data):
        if len(data) != 36:
            print('on got bms real time info length error')
            return
        g_status.motor_status.timeoutTimer.stop()
        i = 4
        g_status.motor_status.batt_status = data[i] & 0x0F # 电池工作状态 0x0:电池单独放电 0x1:电池单独充电 0x2:电池单独回馈 0x3～E:Reserved 0xF:void
        i += 1
        g_status.motor_status.batt_charge_phase = data[i] & 0x0F # 电池充电阶段 0x0:未充电 0x1:握手阶段 0x2:配置阶段 0x3:恒流充电 0x4:恒压充电 0x5:涓流充电 0x6:充电完成 0x7:充电保护 0x8～E:Reserved 0xF:Void
        g_status.motor_status.batt_charge_status = (data[i] >> 4) & 0x0F # 电池充电状态 0x0:充电器未连接未充电 0x1:充电器已连接 未开始充电 0x2:充电器已连接 充电器充电中 0x3:充电器已连接 充电器充电完成 0x4～0x6:Reserved 0x7:void
        i += 1
        i += 1
        g_status.motor_status.batt_charge_finish_status = data[i] & 0x0F # 充电结束状态 充电结束状态为 0x00， 代表正常充电完成，电量 为 100%; 充电结束状态 为非 0，代表充电异常截 止。0x0:充电完成 正常截止 0x1:充电未完成 故障保护 0x2:握手阶段 CHG 反馈信息超时 0x3:握手阶段 CHG 反馈 信息不匹配 0x4:配置阶段 CHG 反馈信息超时 0x5:配置阶段 CHG 反馈信息不匹配 0x6:充电阶段 CHG 反馈信息超时 0x7:充电阶段 CHG 反馈信息不匹配 0x8:充电器移除 0x9：充电器交流无输入 0xF:Void 充电过程中发送无效值， 充电结束发送当前充电结状态值
        g_status.motor_status.acc_valid = ((data[i] & 0x10) != 0) # ACC 信号状态
        g_status.motor_status.on_valid = ((data[i] & 0x20) != 0) # ON 信号状态
        g_status.motor_status.crg_valid = ((data[i] & 0x40) != 0) # CRG 信号状态
        i += 1
        g_status.motor_status.batt_max_charge_voltage = data[i] + (data[i+1] << 8) # 电池最大允许充电电压 0.1V
        i += 2
        g_status.motor_status.batt_max_charge_current = data[i] + (data[i+1] << 8) # 电池最大允许充电电流 0.1A
        i += 2
        g_status.motor_status.batt_soc = data[i] # 电池剩余电量SOC 0.5%
        i += 1
        g_status.motor_status.batt_max_feedback_current = data[i] + (data[i+1] << 8) # 电池最大允许回馈电流 0.1A
        i += 2
        g_status.motor_status.batt_max_current = data[i] + (data[i+1] << 8) # 电池最大允许放电电流 0.1A
        i += 2
        g_status.motor_status.batt_max_instant_current = data[i] + (data[i+1] << 8) # 总电池最大瞬时放电电流 0.1A
        i += 2
        g_status.motor_status.batt_max_instant_current_time = data[i] # 总电池最大瞬时放电电流时间 0.5s
        i += 1
        g_status.motor_status.batt_charge_remain_time = data[i] + (data[i+1] << 8) # 电池电量剩余满充时间 0.1min
        i += 2
        g_status.motor_status.batt_voltage = data[i] + (data[i+1] << 8) # 电池总电压 0.1V
        i += 2
        g_status.motor_status.batt_current = data[i] + (data[i+1] << 8) # 电池总电流 0.1A
        i += 2
        g_status.motor_status.batt_discharge_mos = data[i] & 0x03 # 电池放电 MOS 状态 0x0:DSG OFF 0x1:DSG ON 0x2:Reserved 0x3:void
        g_status.motor_status.batt_charge_mos = (data[i] >> 2) & 0x03 # 电池充电 MOS 状态 0x0:CHG OFF 0x1:CHG ON 0x2:Reserved 0x3:void
        g_status.motor_status.batt_pre_discharge_mos = (data[i] >> 4) & 0x03 # 电池预放电 MOS 状态 0x0:PDSG OFF 0x1:PDSG ON 0x2:Reserved
        i += 1
        g_status.motor_status.batt_remain_soe = data[i] + (data[i+1] << 8) # 电池剩余能量 SOE Wh
        i += 2
        g_status.motor_status.batt_loop_count = data[i] + (data[i+1] << 8) # 电池循环次数
        i += 2
        g_status.motor_status.batt_soh = data[i] # 电池健康度 SOH 1%
        i += 1
        g_status.motor_status.batt_single_max_temp = data[i] # 电池单体最高温度 
        i += 1
        g_status.motor_status.batt_single_min_temp = data[i] # 电池单体最低温度 
        i += 1
        g_status.motor_status.batt_mos_max_temp = data[i] # 电池MOS最高温度 
        i += 1
        g_status.motor_status.batt_single_max_voltage = data[i] + (data[i+1] << 8) # 电池单体最高电压 mV
        i += 2
        g_status.motor_status.batt_single_min_voltage = data[i] + (data[i+1] << 8) # 电池单体最低电压 mV
        i += 2
        g_status.motor_status.batt_errors = data[i:i + 10] # 10个字节故障码

    def getSN(self):
        dataBuffer = bytes(8)
        dataBuffer[0] = 0x03
        dataBuffer[1] = 0x03
        dataBuffer[2] = 0x02
        dataBuffer[3] = 0xE0
        dataBuffer[4] = 0x00
        dataBuffer[5] = 0x00
        dataBuffer[6] = 0xE8
        dataBuffer[7] = 0x00
        self.timeoutTimer.start(BMS_TIMEOUT_MS, 0, self.onTimeout)
        self.serial.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_485, dataBuffer])

    def onGotSN(self, data):
        if len(data) != 38:
            print('on got bms sn info length error')
            return
        self.state = BMS_STATE_RUNNING
        self.timer.stop()
        self.timer.start(BMS_RUNNING_POLL_MS, 1, self.onTimer)
        self.timeoutTimer.stop()
        g_status.bms_status.sn = bytes(data[4:20]).decode()

    def onGotData(self, data):
        self.timeoutCount = 0
        if not self.isValid(data):
            print('on got not valid bms data')
            return
        if data[0] == 0x02 and data[1] == 0x03:
            if (self.state == BMS_STATE_INIT):
                self.onGotInfo(data)
            elif (self.state == BMS_STATE_READING_SN):
                self.onGotSN(data)
            elif (self.state == BMS_STATE_RUNNING):
                self.onGotRealtimeInfo(data)
        elif data[0] == 0x02 and data[1] == 0x01:
            pass # 写参数的返回

    def onTimer(self, a):
        # print('bms onTimer')
        if (self.state == BMS_STATE_INIT or self.state == BMS_STATE_OFFLINE):
            self.getInfo()
        elif (self.state == BMS_STATE_RUNNING):
            self.getRealtimeInfo()
            
    def onTimeout(self, a):
        self.timeoutCount = self.timeoutCount + 1
        if (self.timeoutCount >= 3) :
            self.state = BMS_STATE_OFFLINE
            self.timeoutCount = 0
            self.timer.stop()
            self.timer.start(BMS_OFFLINE_POLL_MS, 1, self.onTimer)


    def checksum(self): #TODO
        return True

    def isValid(self):
        # if self.buffer[0] != 0x02:
        #     return False
        if not self.checksum():
            return False
        return True


if __name__ == '__main__':
    bms = BMS(None)