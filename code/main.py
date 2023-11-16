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

from usr.drivers.key import KEY_EVENT_DOUBLE, KEY_EVENT_LONG
from usr.mcudata import McuData
import utime
import _thread
import queue
import sys_bus
import audio
from misc import Power
from machine import ExtInt
from usr.const import *
utime.sleep_ms(50)
from usr.ui2 import UI_lvgl
utime.sleep_ms(50)
from usr.gps import GPS
from usr.classicbt import BT
from usr.serial import SERIAL
from usr.network import NETWORK
from usr.uidemo import UI_DEMO
from usr.utils.log import log
# from usr.drivers.eta6965 import eta6965
# from usr.drivers.enpin import gpio_en
from usr.drivers.driverinit import driver_init
from usr.drivers.key import *
from usr.mcudata import *

# The following two global variables are mandatory, and users can modify the values of the following two global variables according to their actual projects.
# The values of these two variables are printed before the user code is executed.
PROJECT_NAME = "VC2Pro"
PROJECT_VERSION = "1.0.1"

class MotorStatus:
    def __init__(self):
        # self.max_current = 0 # 最大电流
        # self.sn = bytes(20)  # sn
        # self.speed_mode = None # 速度模式
        # self.biancheng_down = None
        # self.sitdown = None
        
        self.hw_version = None # 硬件版本序号
        self.hw_manufacturer = None # 硬件厂商代码
        self.hw_code = None # 硬件识别码
        self.sw_sub_version = None # 次软件版本号
        self.sw_version = None # 主软件版本号
        self.sw_model = None # 产品型号
        self.sw_code = None # 软件识别码
        self.sw_boot_version = None # BOOT底层软件版本
        self.sw_boot_upgrade_version = None # BOOT升级协议版本
        self.protocal_sub_version = None # 次通信协议版本
        self.protocal_version = None # 主通信协议版本
        self.custom_code = None # 客户代码
        self.manufacturer = None # 设计厂家
        self.spec = None # 产品规格
        self.controller_manufacturer = None # 控制器生产厂家

        self.gear = None # 档位 0x0:P 档 0x1:低速档（D1） 0x2:中速档（D2） 0x3:高速档（D3） 0x4:助力推行档（T） 0x5:倒车辅助档（R） 0x6：D 档（电自） 0x7～F:Reserved
        self.auto_pilot = None # 定时巡航状态 0-禁用; 1-启动; 2-未启动
        self.voltage_mode = None # 当前电压模式 0-48V; 1-60V; 2-72V; 
        self.zhuanba_status = None # 转把状态 0-空闲; 1-工作;
        self.motor_lock_status = None # 0-解锁; 1-上锁;
        self.biancheng_status = 1 # 0- 边撑感应禁用; 1-边撑打开; 2-边撑收起;
        self.sitdown_status = 1 # 0- 坐垫感应禁用; 1-没坐人; 2- 坐人
        self.charging = None # 是否在整车充电
        self.speed_limit = None # 是否限速
        self.eco = None # 是否最佳能耗
        self.wheel_move = False # 轮动信号, 轮子是否在动
        self.motor_move = None # 0-电机停止; 1-正转; 2-反转
        self.p_mode = None # 是否启用驻车模式
        self.controller_error = None # 控制器是否故障
        self.break_mode = None # 是否正在刹车
        self.speed_limit_enable = None # 是否启用限速功能
        self.accelerator = None # 油门开度 0 - 未开; 0x00-0xFE-开度程度; 0xFF-满开
        self.r_speed = None # 0x00:辅助倒车功能禁用 0x01～0x0F:倒车最高设 定速度（当设置为0x0F 时， 转把可控制的速度为全速 的 15%） 出厂默认值：10%
        self.t_speed = None # 0x00:助力推行功能禁用 0x01～0x0F:助力推行最 高设定速度（当设置为 0x0F 时，转把可控制的速 度为全速的 15%） 出厂默认值：13%
        self.d1_speed = None # 0x05～0x64:速度上限阈值 (当设置为 0x10 时，转 把可控制的速度为全速的 16%)
        self.d2_speed = None # 0x05～0x64:速度上限阈值 (当设置为 0x10 时，转 把可控制的速度为全速的 16%)
        self.d3_speed = None # 0x05～0x64:速度上限阈值 (当设置为 0x10 时，转 把可控制的速度为全速的 16%)
        self.motor_temp = None # 电机温度
        self.controller_temp = None # 控制器温度
        self.voltage = None # 直流电压 0.1v
        self.current = None # 电机电流 0.1A
        self.wheel_r = None # 轮半径
        self.hall_error = None # 是否有霍尔故障
        self.biancheng_error = None # 是否有边撑故障
        self.sitdown_error = None # 是否有坐垫感应故障
        self.zhuanba_error = None # 是否有转把故障
        self.phase_current_error = None # 是否有相电流过流故障
        self.voltage_error = None # 是否有电压故障
        self.motor_overtemp = None # 是否电机过温
        self.controller_overtemp = None # 是否控制器过温
        self.phase_current_overflow = None # 是否相电流溢出
        self.phase_current_zero_error = None # 是否相电流零点故障
        self.phase_current_short_error = None # 是否相电流短路故障
        self.line_current_zero_error = None # 是否线电流零点故障
        self.mosfet_up_error = None # 是否上桥故障
        self.mosfet_down_error = None # 是否下桥故障
        self.max_current_error = None # 是否峰值电流保护故障
        self.rest_flag = None # 0x0:收到中控批量设置命 令后置 0 0x1:表示ACC 重新上电 或电控重启，收到批量设 置命令后，将此标志位置 0
        self.hall = None # 用于计算转速 转速（m/s）=（500Ms 霍 尔个数*2）/（6*极对数）* 周长（米）
        

class BmsStatus:
    def __init__(self):
        self.hw_version = None # 硬件版本序号
        self.hw_manufacturer = None # 硬件厂商代码
        self.hw_code = None # 硬件识别码
        self.sw_sub_version = None # 次软件版本号
        self.sw_version = None # 主软件版本号
        self.sw_model = None # 产品型号
        self.sw_code = None # 软件识别码
        self.sw_boot_version = None # BOOT底层软件版本
        self.sw_boot_upgrade_version = None # BOOT升级协议版本
        self.protocal_sub_version = None # 次通信协议版本
        self.protocal_version = None # 主通信协议版本
        self.custom_code = None # 客户代码
        self.manufacturer = None # 设计厂家
        self.spec = None # 产品规格
        self.bms_manufacturer = None # BMS生产厂家

        self.rated_voltage = None # 电池额定电压 V
        self.rated_ah = None # 电池额定容量 AH
        self.batt_cell_s_num = None # 电池电芯串联级数
        self.batt_cell_p_num = None # 电池电芯并联级数
        self.batt_cell_temp_sensor_num = None # 电池电芯温度传感器数量

        self.sn = None # SN号, 16字节字符串

        self.batt_status = None # 电池工作状态 0x0:电池单独放电 0x1:电池单独充电 0x2:电池单独回馈 0x3～E:Reserved 0xF:void
        self.batt_charge_phase = None # 电池充电阶段 0x0:未充电 0x1:握手阶段 0x2:配置阶段 0x3:恒流充电 0x4:恒压充电 0x5:涓流充电 0x6:充电完成 0x7:充电保护 0x8～E:Reserved 0xF:Void
        self.batt_charge_status = None # 电池充电状态 0x0:充电器未连接未充电 0x1:充电器已连接 未开始充电 0x2:充电器已连接 充电器充电中 0x3:充电器已连接 充电器充电完成 0x4～0x6:Reserved 0x7:void
        self.batt_charge_finish_status = None # 充电结束状态 充电结束状态为 0x00， 代表正常充电完成，电量 为 100%; 充电结束状态 为非 0，代表充电异常截 止。0x0:充电完成 正常截止 0x1:充电未完成 故障保护 0x2:握手阶段 CHG 反馈信息超时 0x3:握手阶段 CHG 反馈 信息不匹配 0x4:配置阶段 CHG 反馈信息超时 0x5:配置阶段 CHG 反馈信息不匹配 0x6:充电阶段 CHG 反馈信息超时 0x7:充电阶段 CHG 反馈信息不匹配 0x8:充电器移除 0x9：充电器交流无输入 0xF:Void 充电过程中发送无效值， 充电结束发送当前充电结状态值
        self.acc_valid = None # ACC 信号状态
        self.on_valid = None # ON 信号状态
        self.crg_valid = None # CRG 信号状态
        self.batt_max_charge_voltage = None # 电池最大允许充电电压 0.1V
        self.batt_max_charge_current = None # 电池最大允许充电电流 0.1A
        self.batt_soc = None # 电池剩余电量SOC 0.5%
        self.batt_max_feedback_current = None # 电池最大允许回馈电流 0.1A
        self.batt_max_current = None # 电池最大允许放电电流 0.1A
        self.batt_max_instant_current = None # 总电池最大瞬时放电电流 0.1A
        self.batt_max_instant_current_time = None # 总电池最大瞬时放电电流时间 0.5s
        self.batt_charge_remain_time = None # 电池电量剩余满充时间 0.1min
        self.batt_voltage = None # 电池总电压 0.1V
        self.batt_current = None # 电池总电流 0.1A
        self.batt_discharge_mos = None # 电池放电 MOS 状态 0x0:DSG OFF 0x1:DSG ON 0x2:Reserved 0x3:void
        self.batt_charge_mos = None # 电池充电 MOS 状态 0x0:CHG OFF 0x1:CHG ON 0x2:Reserved 0x3:void
        self.batt_pre_discharge_mos = None # 电池预放电 MOS 状态 0x0:PDSG OFF 0x1:PDSG ON 0x2:Reserved
        self.batt_remain_soe = None # 电池剩余能量 SOE Wh
        self.batt_loop_count = None # 电池循环次数
        self.batt_soh = None # 电池健康度 SOH 1%
        self.batt_single_max_temp = None # 电池单体最高温度 
        self.batt_single_min_temp = None # 电池单体最低温度 
        self.batt_mos_max_temp = None # 电池MOS最高温度 
        self.batt_single_max_voltage = None # 电池单体最高电压 mV
        self.batt_single_min_voltage = None # 电池单体最低电压 mV
        self.batt_errors = None # 10个字节故障码

class Settings():
    def __init__(self):
        self.no_feeling_lock = True # 蓝牙无感解锁/上锁
        self.timeout_lock = False # 超时上锁
        # self.unlock_bt_mac_whitelist = ['8c:5a:c1:87:4d:9f',] # 蓝牙解锁白名单
        self.unlock_bt_mac_whitelist = [] # 蓝牙解锁白名单

class GlobalStatus():
    def __init__(self):
        self.poweron_starttime = None
        self.lock_mode = None # 解锁/锁车状态
        self.latlng = None # 经纬度
        self.bt_status = BT_STATUS_OFF # 蓝牙开关状态
        self.mcu_data = McuData()
        self.settings = Settings()

class MMI():
    def __init__(self):
        log.d("mmi start")
        # 读取配置文件数据
        self.config_json = self.read_config_json()
        driver_init()
        # self.mKey = None
        # self.init_mkey()
        # self.breakKey = None
        # self.init_breakKey()
        # self.init_eta6965()
        # self.init_boot_5v()
        _thread.start_new_thread(self.mmi_main_task,(THREAD_ID_MAIN,))

    # def init_mkey(self):
    #     self.mKey = ExtInt(MKEY_INT, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, self.onMKeyClick)
    #     self.mKey.enable()

    # def init_breakKey(self):
    #     self.breakKey = ExtInt(BRAKE_INT, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, self.onBreakKeyClick)
    #     self.breakKey.enable()

    # def init_eta6965(self):
    #     dev = eta6965()
    #     dev.init(ETA6965_ADDRESS)

    # def init_boot_5v(self):
    #     boot_5v_en = gpio_en(BOOST_5V_EN_PIN, 0, "boot_5v_en")
    #     boot_5v_en.enable()


    def mmi_main_task(self, thread_id):
        log.d("mmi_main_task id %d" % thread_id)
        sys_bus.subscribe('LOCK_MODE', self.onBusMsg)
        sys_bus.subscribe('MKEY_EVENT', self.onBusMsg)
        sys_bus.subscribe('LED_EVENT', self.onBusMsg)
        global mmiQueue
        mmiQueue = queue.Queue(30)
        self.msg_type_handle_func = (self.mmi_update_ui,
            self.mmi_set_navi_info,
            self.mmi_handle_network_event
            )
        while 1:
            mmi_data = mmiQueue.get()
            if (mmi_data[0] >= MSG_MMI_MAX):
                continue
            self.msg_type_handle_func[mmi_data[0]](mmi_data)

    def onBusMsg(self, topic, msg):
        if topic == 'LOCK_MODE':
            if msg == MODE_LOCK:
                self.enablebackLight(False)
                self.enableLCD(False)
                self.pauseDemo()
                self.clearDemoSpeed()
                self.setReady('P')
                # self.playSound('U:/audio/yishangsuo.mp3')
                # self.mmi_lock()
            elif msg == MODE_UNLOCK:
                self.enablebackLight(True)
                self.enableLCD(True)
                self.resumeDemo()
                self.setReady('Ready')
                # self.playSound('U:/audio/yijiesuo.mp3')
                # self.mmi_unlock()
            elif msg == MODE_READY_TO_LOCK:
                self.enablebackLight(True)
                self.enableLCD(True)
                self.pauseDemo()
                self.clearDemoSpeed()
                self.setReady('P')
                # self.playSound('U:/audio/zhunbeisuoche.mp3')
            elif msg == MODE_READY_TO_UNLOCK:
                self.enablebackLight(True)
                self.enableLCD(False)
                self.pauseDemo()
                self.clearDemoSpeed()
                self.setReady('P')
                # self.playSound('U:/audio/yonghukaojin.mp3')
                # self.mmi_unlock()
        elif topic == 'MKEY_EVENT':
            if msg == KEY_EVENT_SHORT:
                log.i('短按 M-Key')
                self.onMKeyClick()
            elif msg == KEY_EVENT_LONG:
                log.i('长按 M-Key')
            elif msg == KEY_EVENT_DOUBLE:
                log.i('双击 M-Key')
        elif topic == 'LED_EVENT':
            if msg[0] == 'l_led':
                ui.lvgl_queue_put([MSG_UI_SET_LIGHT_LEFT, msg[1]])
            elif msg[0] == 'r_led':
                ui.lvgl_queue_put([MSG_UI_SET_LIGHT_RIGHT, msg[1]])
            elif msg[0] == 'n_led':
                ui.lvgl_queue_put([MSG_UI_SET_LIGHT_NEAR, msg[1]])
            elif msg[0] == 'f_led':
                ui.lvgl_queue_put([MSG_UI_SET_LIGHT_FAR, msg[1]])
            elif msg[0] == 'a_led':
                ui.lvgl_queue_put([MSG_UI_SET_LIGHT_SMALL, msg[1]])

    def mmi_update_ui(self, data):
        #log.d('mmi_update_ui')
        if data[1] == UI_TYPE_CONTROLLER:
            #log.d('mmi_update_ui UI_TYPE_CONTROLLER')
            ui.lvgl_queue_put([MSG_UI_SET_SPEED, int(g_status.mcu_data.getData(hole_num) * 2 / (6 * 30) * 2 * 3.14159 * g_status.mcu_data.getData(curr_round) * 3600 / 1000 / 1000)])
            ui.lvgl_queue_put([MSG_UI_SET_CURRENT, int(g_status.mcu_data.getData(bat_all_curr) * 0.1)])
            ui.lvgl_queue_put([MSG_UI_SET_AUTO_SPEED, g_status.mcu_data.getData(cruising_status) == 1])
            ui.lvgl_queue_put([MSG_UI_SET_GEAR, g_status.mcu_data.getData(now_parking)])
            ui.lvgl_queue_put([MSG_UI_SET_BIANCHENG, g_status.mcu_data.getData(hold_func) == 1])
            ui.lvgl_queue_put([MSG_UI_SET_NOT_SIT, g_status.mcu_data.getData(seat_sensor) == 1])
            ui.lvgl_queue_put([MSG_UI_SET_ECO, g_status.mcu_data.getData(eco_sig) == 1])

    def enableLCD(self, lcdEnable):
        log.d('enableLCD {}'.format(lcdEnable))
        if ui is not None:
            if lcdEnable:
                ui.turnLcdOn()
            else:
                ui.turnLcdOff()

    def enablebackLight(self, backLightEnable):
        log.d('enablebackLight {} '.format(backLightEnable))
        try:
            if backLightEnable:
                serial.turnBackLightOn()
            else:
                serial.turnBackLightOff()
        except:
            log.e('turnBackLight error')

    def mmi_set_speed(self, data):
        data1 = [MSG_UI_SET_SPEED, data[1]]
        log.d('mmi_set_speed')
        ui.lvgl_queue_put(data1)

    def setReady(self, str):
        ui.lvgl_queue_put([MSG_UI_SET_READY, str])


    def mmi_set_navi_info(self, data):
        data[0] = MSG_UI_SET_NAVI_INFO
        ui.lvgl_queue_put(data)

    def mmi_handle_network_event(self, data):
        if data[1] == NETWORK_EVENT_DATA_CONNECTED:
            log.d('network ready, start mqtt')
            # data_service = DataService()

    # 读取json文件内容
    def read_config_json(self, file_path='usr/system_config.json'):
        with open(file_path, 'r') as f:
            config_json = ujson.load(f)
        return config_json

    def mmi_queue_put(self, data):
        global mmiQueue
        mmiQueue.put(data)

    def getGStatus(self):
        global g_status
        return g_status

    def setLockMode(self, mode):
        global g_status
        g_status.lock_mode = mode
        if mode == MODE_LOCK:
            log.i('---------- MODE_LOCK ----------')
        elif mode == MODE_UNLOCK:
            log.i('---------- MODE_UNLOCK ----------')
        elif mode == MODE_READY_TO_UNLOCK:
            log.i('---------- MODE_READY_TO_UNLOCK ----------')
        elif mode == MODE_READY_TO_LOCK:
            log.i('---------- MODE_READY_TO_LOCK ----------')
        sys_bus.publish('LOCK_MODE', mode)

    def setBtStatus(self, status):
        global g_status
        g_status.bt_status = status
        if status == BT_STATUS_CONNECTED:
            if g_status.settings.unlock_bt_mac_whitelist == None or len(g_status.settings.unlock_bt_mac_whitelist) == 0:
                self.checkIfNeedReadyToLock()
        if ui is not None:
            ui.lvgl_queue_put([MSG_UI_SET_BT, status == BT_STATUS_CONNECTED])

    # Mkey 按键处理
    def onMKeyClick(self):
        log.i('M-Key clicked!')
        if g_status.lock_mode == MODE_READY_TO_UNLOCK:
            self.setLockMode(MODE_UNLOCK)
        elif g_status.lock_mode == MODE_UNLOCK:
            if DEMO_MODE:
                self.setLockMode(MODE_READY_TO_LOCK)
        elif g_status.lock_mode == MODE_READY_TO_LOCK:
            if DEMO_MODE:
                self.setLockMode(MODE_LOCK)
        elif g_status.lock_mode == MODE_LOCK:
            if DEMO_MODE:
                self.setLockMode(MODE_UNLOCK)
        self.checkIfNeedReadyToLock()

    # def onBreakKeyClick(self, args):
    #     # Power.powerRestart()
    #     if DEMO_MODE:
    #         try:
    #             if uiDemo.isPause:
    #                 uiDemo.resume()
    #             else:
    #                 uiDemo.pause()
    #         except:
    #             log.e('uidemo pause error')
    #     pass

    def checkIfNeedReadyToLock(self):
        log.i('checkIfNeedReadyToLock')
        if g_status.lock_mode == MODE_UNLOCK \
                and g_status.mcu_data.getData(hold_func) == 1 \
                and g_status.mcu_data.getData(seat_sensor) == 1 \
                and g_status.mcu_data.getData(vechel_move_sig) == 0 \
                and (g_status.settings.no_feeling_lock or g_status.settings.timeout_lock):
            if not DEMO_MODE:
                self.setLockMode(MODE_READY_TO_LOCK)

    def resumeDemo(self):
        pass
        # try:
        #     uiDemo.resume()
        # except:
        #     log.w('resumeDemo error')

    def pauseDemo(self):
        try:
            uiDemo.pause()
        except:
            log.w('pauseDemo error')

    def clearDemoSpeed(self):
        try:
            uiDemo.clearSpeed()
        except:
            log.w('clearDemoSpeed error')

    def playSound(self, filename):
        # pass
        aud = audio.Audio(2)
        aud.set_pa(AUDIO_PA_EN_PIN)
        aud.play(1,0,filename)


def main():
    global ui
    global mmi
    global gps
    global btSlave
    global serial
    global network
    global uiDemo
    global g_status

    g_status = GlobalStatus()
    g_status.lock_mode = MODE_UNLOCK
    g_status.poweron_starttime = utime.time()

    log.d("main init")

    # 初始化主线程
    mmi = MMI()

    # 网络检查
    utime.sleep_ms(100)
    network = NETWORK(mmi)

    # 初始化UI
    # ui = None
    utime.sleep_ms(100)
    ui = UI_lvgl(mmi)

    # 初始化蓝牙
    utime.sleep_ms(500)
    btSlave = BT(mmi)
    # utime.sleep_ms(2000)
    # ble = BLE(mmi)
    # ble.init()

    # 初始化GPS
    utime.sleep_ms(1000)
    gps = GPS(mmi)

    # 初始化串口
    utime.sleep_ms(500)
    serial = SERIAL(mmi)

    # 初始化UI演示
    if DEMO_MODE:
        utime.sleep_ms(1000)
        uiDemo = UI_DEMO(ui, mmi)
        uiDemo.start()


    log.d('------- start -------')

if __name__ == '__main__':
    utime.sleep_ms(500)
    log.d('------- start main -------')
    main()