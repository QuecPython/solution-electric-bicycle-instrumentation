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
from usr.utils.log import log

index=0
sta_car=index;index+=1
sta_alarm=index;index+=1
main_bat_status=index;index+=1
index+=1
n_led_status=index;index+=1
f_led_status=index;index+=1
a_led_status=index;index+=1
turn_led_status=index;index+=1
headlock_status=index;index+=1
seatlock_status=index;index+=1
bt_no_feel_unlock_status=index;index+=1
remote_433_status=index;index+=1
acc_status=index;index+=1
look_car_status=index;index+=1
car_no_fell_unlock_length=index;index+=1
alarm_status=index;index+=1
nfc_status=index;index+=1
index+=1
mcu_version=index;index+=1
index+=1
ctrl_driver_comm_status=index;index+=1
ctrl_driver_fault_status=index;index+=1
index+=1
now_parking=index;index+=1
cruising_status=index;index+=1
now_volt_mode=index;index+=1
twister_idle=index;index+=1
motor_lock=index;index+=1
hold_func=index;index+=1
seat_sensor=index;index+=1
charger_status=index;index+=1
ctrl_speed=index;index+=1
eco_sig=index;index+=1
vechel_move_sig=index;index+=1
motor_run=index;index+=1
stop_car_mode=index;index+=1
ctrl_status=index;index+=1
brake_car_status=index;index+=1
remove_limit_speed=index;index+=1
iol_open=index;index+=1
index+=1
ass_back_car_speed=index;index+=1
ass_push_speed=index;index+=1
low_speed_parking=index;index+=1
middle_speed_parking=index;index+=1
high_speed_parking=index;index+=1
curr_round=index;index+=1
hore_fault_flag=index;index+=1
hold_fault_flag=index;index+=1
seat_fault_flag=index;index+=1
twist_fault_flag=index;index+=1
phase_cuur_fault_flag=index;index+=1
volt_fault_flag=index;index+=1
motor_outtemp_fault_flag=index;index+=1
ctrl_out_temp=index;index+=1
phase_cuur_outflow_fault=index;index+=1
phase_cuur_zero_dot_fault=index;index+=1
phase_cuur_short_fault=index;index+=1
line_cuur_zero_dot_fault=index;index+=1
mos_upbradge_fault_fault=index;index+=1
mos_downbradge_fault_fault=index;index+=1
peak_line_cuur_protect_fault=index;index+=1
acc_again_electly=index;index+=1
hole_num=index;index+=1
index+=1
bsm_comm_status=index;index+=1
bms_fault=index;index+=1
index+=1
bat_work_status=index;index+=1
index+=1
charger_stage=index;index+=1
charger_status=index;index+=1
charger_over_status=index;index+=1
acc_sig=index;index+=1
on_sig=index;index+=1
org_sig=index;index+=1
index+=1
bat_power_remain_charger_full_time=index;index+=1
bat_all_volt=index;index+=1
bat_all_curr=index;index+=1
remain_batt_soe=index;index+=1
bat_cyc_num=index;index+=1
bat_health=index;index+=1
bat_sig_max_high_temp=index;index+=1
bat_sig_min_low_temp=index;index+=1
bat_sig_over_volt_fault=index;index+=1
bat_sig_under_volt_fault=index;index+=1
bat_sig_volt_diff_too_max_fault=index;index+=1
bat_zero_charge_self_lock_fault=index;index+=1
bat_all_over_volt_fault=index;index+=1
bat_all_under_volt_fault=index;index+=1
bat_feedback_over_volt_fault=index;index+=1
bat_charger_curr_fault=index;index+=1
bat_feedback_over_curr_fault=index;index+=1
bat_discharger_over_cuur_fault=index;index+=1
bat_discharger_instan_over_curr_fault=index;index+=1
bat_prelimily_discharger_curr_fault=index;index+=1
bat_charger_high_temp_fault=index;index+=1
bat_charger_low_temp_fault=index;index+=1
bat_discharger_high_temp_fault=index;index+=1
bat_discharger_low_temp_fault=index;index+=1
bat_temp_diff_big_fault=index;index+=1
bat_balana_temp_over_high_fault=index;index+=1
bat_mos_temp_over_high_fault=index;index+=1
bat_discharger_resis_temp_overhigh_fault=index;index+=1
bat_afe_charge_low_temp_fault=index;index+=1
bat_afe_discharge_low_cuur_fault=index;index+=1
bat_afe_charge_over_cuur_fault=index;index+=1
bat_short_circuit_fault=index;index+=1
bat_discharger_mos_fault=index;index+=1
bat_pre_discharger_fault=index;index+=1
bat_charger_mos_fault=index;index+=1
bat_save_time_fault=index;index+=1
bat_material=index;index+=1
bat_volt_level=index;index+=1
bat_ver=index;index+=1
bat_manufa=index;index+=1
bat_production_time_yy=index;index+=1
bat_production_time_mm=index;index+=1
bat_production_time_dd=index;index+=1
serial=index;index+=1
index+=1



class McuData:
    def __init__(self):
        self.totalMcuDataLen = 70 # 字节长度
        self.dataList = [
            [0,4,0x0,0xF], # sta_car 车辆状态: 0x0:设防 0x1:解防上锁（关闭） 0x2:解锁（启动） 0x3：解防上锁唤醒（等待启动） 0x4:异常 0x4～F:Reserved
            [0,4,0x0,0xF], # sta_alarm 报警状态(无音灯效): 0x00 无报警情况 Bit4 0正常  1 温度报警 Bit5  0正常  1 断电报警 Bit6 0 正常 1 电压报警 Bit7 0 正常 1 充电器异常
            [0,1,0x0,0x1], # main_bat_status 大电池状态: 0x0:大电池不在位 0x1:大电池在位
            [0,2,0,0], # res1 预留: 
            [0,1,0x0,0x1], # n_led_status 近光灯状态: 0x0:近光灯关闭状态 0x1:近光灯打开状态
            [0,1,0x0,0x1], # f_led_status 远光灯状态: 0x0:远光灯关闭状态 0x1:远光灯打开状态
            [0,1,0x0,0x1], # a_led_status 示廓灯状态: 0x0:示廓灯关闭状态 0x1:示廓灯打开状态
            [0,2,0x0,0x3], # turn_led_status 转向灯状态: 0x0:左右全灭 0x1:左转灯亮 0x2:右转灯亮 0x3:双闪灯亮
            [0,1,0x0,0x1], # headlock_status 龙头锁状态: 0x0:龙头锁解锁 0x1:龙头锁上锁
            [0,1,0x0,0x1], # seatlock_status 坐桶锁状态: 0x0:坐桶锁解锁 0x1:坐桶锁上锁
            [0,1,0x0,0x1], # bt_no_feel_unlock_status 蓝牙无感解锁状态: 0x0:蓝牙无感解锁已禁用 0x1:启用蓝牙无感已启用
            [0,1,0x0,0x1], # remote_433_status 433遥控状态: 0x0:433遥控功能已禁用 0x1:433遥控功能已启用
            [0,1,0x0,0x1], # acc_status ACC上电状态: 0x0:ACC断电 0x1:ACC上电
            [0,1,0x0,0x1], # look_car_status 寻车状态: 0x0:未触发寻车（默认） 0x1:触发寻车
            [0,2,0x0,0x2], # car_no_fell_unlock_length 车辆无感解锁距离读取: 0x00近距离 0x01中距离 0x02远距离
            [0,3,0x0,0x7], # alarm_status 报警状态（有音灯效）: 0x00 无报警情况 1防盗报警 2移报警 3倾倒报警
            [0,2,0x0,0x3], # nfc_status NFC状态: 0x00 无NFC刷卡 0x01 NFC短刷 0x02 NFC长刷
            [0,3,0,0], # res2 预留: 
            [0,8,0x0,0xFF], # mcu_version MCU版本号: bit0—bit3为版本号小数点前面的数字 bit4—bit7为版本号小数点后面的数字
            [0,8,0,0], # res3 预留: NA 
            [0,1,0x0,0x1], # ctrl_driver_comm_status 控制器通讯状态: 0x0:控制器通讯失败 0x1:控制器通讯正常
            [0,1,0x0,0x1], # ctrl_driver_fault_status 控制器故障状态: 0x0:无故障  0x1:控制器存在故障（只要控制器存在故障该字段设为1）
            [0,6,0,0], # res4 预留: 
            [0,4,0x0,0xF], # now_parking 当前档位: 0x0:P 档 0x1:低速档（D1） 0x2:中速档（D2） 0x3:高速档（D3） 0x4:助力推行档（T） 0x5:倒车辅助档（R） 0x6：D 档（电自） 0x7～F:Reserved
            [0,2,0x0,0x3], # cruising_status 巡航状态: 0x0:定速巡航功能禁用 0x1:定速巡航启动 0x2:定速巡航未启动0x3:Reserved
            [0,2,0x0,0x2], # now_volt_mode 当前电压模式: 0x0:48V 0x1:60V 0x2:72V 0x3:Reserved
            [0,1,0x0,0x1], # twister_idle 转把状态: 0x0:转把空闲 0x1:转把工作
            [0,1,0x0,0x1], # motor_lock 电机锁状态: 0x0:电机解锁 0x1:电机上锁
            [0,2,0x0,0x3], # hold_func 边撑状态: 0x0:边撑感应功能禁用 0x1:边撑打开 0x2:边撑收起0x3:Reserved
            [0,2,0x0,0x3], # seat_sensor 坐垫感应状态: 0x0:坐垫感应功能禁用 0x1:未检测到坐垫坐人 0x2:检测到坐垫坐人0x3:Reserved
            [0,1,0x0,0x1], # charger_status 充电状态: 0x0:未整车充电 0x1:正在整车充电
            [0,1,0x0,0x1], # ctrl_speed 限速状态: 0x0:限速状态 0x1:不限速状态
            [0,1,0x0,0x1], # eco_sig ECO 信号: 0x0:非最佳能耗 0x1:最佳能耗
            [0,1,0x0,0x1], # vechel_move_sig 轮动信号: 0x0:无轮动 0x1:轮动
            [0,2,0x0,0x3], # motor_run 电机转动: 0x0:电机停止 0x1:正转 0x2:反转0x3:Reserved
            [0,1,0x0,0x1], # stop_car_mode 驻车模式: 0x0:未启用驻车模式 0x1:启用驻车模式
            [0,1,0x0,0x1], # ctrl_status 控制器状态: 0x0:控制器正常 0x1:控制器错误
            [0,1,0x0,0x1], # brake_car_status 刹车状态: 0x0:未刹车 0x1:刹车中
            [0,1,0x0,0x1], # remove_limit_speed 解除限速状态: 0x0:解除限速功能禁用 0x1:解除限速功能启用 (功能开启后，最高速度不受限制)
            [0,8,0x00,0xFF], # iol_open 油门开度: 0x00:未开 0x00～0xFE:开度程度 0xFF:满开
            [0,8,0x00,0xFF], # res5 预留: NA
            [0,8,0x00,0x0F], # ass_back_car_speed 辅助倒车速度: 0x00:辅助倒车功能禁用 0x01～0x0F:倒车最高设 定速度（当设置为0x0F 时， 转把可控制的速度为全速的 15%） 出厂默认值：10%
            [0,8,0x00,0x0F], # ass_push_speed 助力推行速度: 0x00:助力推行功能禁用 0x01～0x0F:助力推行最高设定速度（当设置为0x0F 时，转把可控制的速度为全速的 15%） 出厂默认值：13%
            [0,8,0x05,0x64], # low_speed_parking 低速档: 0x05～0x64:速度上限阈值 (当设置为 0x10 时，转把可控制的速度为全速的16%)
            [0,8,0x05,0x64], # middle_speed_parking 中速档: 0x05～0x64:速度上限阈值 (当设置为 0x10 时，转把可控制的速度为全速的16%)
            [0,8,0x05,0x6E], # high_speed_parking 高速档上限阈值: 0x05～0x6E:速度上限阈值 (当设置为 0x10 时，转把可控制的速度为全速的16%)
            [0,8,0x00,0xFF], # curr_round 轮半径: NA
            [0,1,0x0,0x1], # hore_fault_flag 电机霍尔故障: 0x0:电机霍尔正常 0x1:电机霍尔故障
            [0,1,0x0,0x1], # hold_fault_flag 边撑故障: 0x0:边撑正常 0x1:边撑故障
            [0,1,0x0,0x1], # seat_fault_flag 坐垫故障: 0x0:坐垫正常 0x1:坐垫故障
            [0,1,0x0,0x1], # twist_fault_flag 转把故障: 0x0:转把正常 0x1:转把故障
            [0,1,0x0,0x1], # phase_cuur_fault_flag 相电流过流故障: 0x0:相电流过流正常 0x1:相电流过流故障
            [0,1,0x0,0x1], # volt_fault_flag 电压故障: 0x0:电压正常 0x1:电压故障
            [0,1,0x0,0x1], # motor_outtemp_fault_flag 电机过热故障: 
            [0,1,0x0,0x1], # ctrl_out_temp 控制器过热故障: 
            [0,1,0x0,0x1], # phase_cuur_outflow_fault 相电流溢出: 0x0:相电流正常 0x1:相电流溢出故障
            [0,1,0x0,0x1], # phase_cuur_zero_dot_fault 相电流零点故障: 0x0:相电流正常 0x1:相电流零点故障
            [0,1,0x0,0x1], # phase_cuur_short_fault 相线短路故障: 0x0:相电流正常 0x1:相线短路故障
            [0,1,0x0,0x1], # line_cuur_zero_dot_fault 线电流零点故障: 0x0:线电流零点正常 0x1:线电流零点故障
            [0,1,0x0,0x1], # mos_upbradge_fault_fault MOSFET上桥故障: 0x0:MOSFET 上桥正常 0x1:MOSFET 上桥故障
            [0,1,0x0,0x1], # mos_downbradge_fault_fault MOSFET下桥故障: 0x0:MOSFET 下桥正常 0x1:MOSFET 下桥故障
            [0,1,0x0,0x1], # peak_line_cuur_protect_fault 峰值线电流保护: 0x0:峰值线电流保护正常 0x1 峰值线电流保护故障
            [0,1,0x0,0x1], # acc_again_electly ACC 重新上电或电控重启标志位: 0x0:收到中控批量设置命令后置 0 0x1:表示ACC 重新上电或电控重启，收到批量设置命令后，将此标志位置
            [0,16,0x0,0xFFFF], # hole_num 500Ms霍尔个数: 用于计算转速 转速（m/s）=（500Ms霍尔个数*2）/（6*极对数）* 周长（米）
            [0,16,0,0], # res6 保留: NA  
            [0,1,0x0,0x1], # bsm_comm_status BMS通讯状态: 0x0:BMS通讯失败 0x1:BMS通讯正常
            [0,1,0x0,0x1], # bms_fault BMS故障状态: 0x0:BMS无故障 0x1:BMS存在故障（只要BMS存在故障该字段设为1）
            [0,6,0,0], # res7 预留: NA
            [0,4,0x0,0xF], # bat_work_status 电池工作状态: 0x0:电池单独放电 0x1:电池单独充电 0x2:电池单独回馈 0x3～E:Reserved  0xF: Void
            [0,4,0,0], # res8 预留: NA
            [0,4,0x0,0xF], # charger_stage 电池充电阶段: 0x0:未充电  0x1:握手阶段  0x2:配置阶段  0x3:恒流充电  0x4:恒压充电  0x5:涓流充电  0x6:充电完成  0x7:充电保护  0x8～E:Reserved  0xF:Void 
            [0,4,0x0,0xF], # charger_status 电池充电状态: 0x0:充电器未连接  未充电  0x1:充电器已连接  未开始充电  0x2:充电器已连接  充电器充电中  0x3:充电器已连接  充电器充电完成  0x4～0x6:Reserved  0x7:void 
            [0,4,0x0,0xE], # charger_over_status 充电结束状态: 充电结束状态为 0x00，代表正常充电完成，电量为 100%; 充电结束状态为非 0，代表充电异常截止。  0x0:充电完成 正常截止  0x1:充电未完成 故障保护  0x2:握手阶段 CHG 反馈信息超时  0x3:握手阶段 CHG 反馈信息不匹配  0x4:配置阶段 CHG 反馈信息超时  0x5:配置阶段 CHG 反馈信息不匹配  0x6:充电阶段 CHG 反馈信息超时  0x7:充电阶段 CHG 反馈信息不匹配  0x8:充电器移除  0x9：充电器交流无输入  0xF:Void  充电过程中发送无效值，充  电结束发送当前充电结状  态值
            [0,1,0x0,0x1], # acc_sig ACC信号状态: 0x0:Invalid  0x1:Valid 
            [0,1,0x0,0x1], # on_sig ON信号状态: 0x0:Invalid  0x1:Valid 
            [0,1,0x0,0x1], # org_sig CRG信号状态: 0x0:Invalid  0x1:Valid 
            [0,1,0,0], # res9 预留: NA
            [0,16,0x0000,0x07D0], # bat_power_remain_charger_full_time 电池电量剩余满充时间: NA
            [0,16,0x0000,0x2710], # bat_all_volt 电池总电压: NA
            [0,16,0x0000,0x2710], # bat_all_curr 电池总电流: NA
            [0,16,0x0000,0xFFFF], # remain_batt_soe 电池剩余能量SOE: NA
            [0,16,0x0000,0x07D0], # bat_cyc_num 电池循环次数: NA
            [0,8,0x00,0xC8], # bat_health 电池健康度SOH: NA
            [0,8,0x00,0xBE], # bat_sig_max_high_temp 电池单体最高温度: -40℃ - 150℃
            [0,8,0x00,0xBE], # bat_sig_min_low_temp 电池单体最低温度: -40℃ - 150℃ 
            [0,2,0x0,0x3], # bat_sig_over_volt_fault 电池单体过压故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_sig_under_volt_fault 电池单体欠压故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_sig_volt_diff_too_max_fault 电池单体压差过大故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_zero_charge_self_lock_fault 0V禁充软件锁故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_all_over_volt_fault 电池总压过压故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_all_under_volt_fault 电池总压欠压故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_feedback_over_volt_fault 电池回馈过压故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_charger_curr_fault 电池充电过流故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_feedback_over_curr_fault 电池回馈过流故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_discharger_over_cuur_fault 电池放电过流故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_discharger_instan_over_curr_fault 电池放电瞬时过流故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_prelimily_discharger_curr_fault 电池预放过流故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_charger_high_temp_fault 电池充电高温故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_charger_low_temp_fault 电池充电低温故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_discharger_high_temp_fault 电池放电高温故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_discharger_low_temp_fault 电池放电低温故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_temp_diff_big_fault 电池温差过大故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_balana_temp_over_high_fault 电池均衡温度过高故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_mos_temp_over_high_fault 电池MOS温度过高故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_discharger_resis_temp_overhigh_fault 电池预放电阻温度过高故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_afe_charge_low_temp_fault 电池AFE充电低温故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_afe_discharge_low_cuur_fault 电池AFE放电过流故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_afe_charge_over_cuur_fault 电池AFE充电过流故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_short_circuit_fault 电池短路: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_discharger_mos_fault 放电MOS故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_pre_discharger_fault 预放电MOS 故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_charger_mos_fault 充电MOS故障: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void
            [0,2,0x0,0x3], # bat_save_time_fault 电池寿命终止故障EOL: 0x0:Normal  0x1:Reserved  0x2:Protect  0x3:void 
            [0,4,0x0,0xF], # bat_material 电池材料体系: 0x0:未知 0x1:磷酸铁锂材料 0x2:三元锂 0x3:锰酸锂 0x4:钛酸锂
            [0,4,0x0,0xF], # bat_volt_level 电池电压等级: 0x0:未知 0x1:电池额定电压为48V 0x2:电池额定电压为72V
            [0,4,0x0,0xF], # bat_ver 电池额定规格: 0x0:未知 0x1:规格A 0x2:规格B 0x3:规格B 0x4:规格C 0x5:规格D Note:表示电池的一种规格，规格中包含额定容量、循环次数等信息
            [0,4,0x0,0xF], # bat_manufa 生产厂家代码: 0x0:未知 0x1:生产厂家A 0x2:生产厂家B 0x3:生产厂家B 0x4:生产厂家C 0x5:生产厂家D
            [0,8,0x0,0x63], # bat_production_time_yy 生产时间(yy): Note:年份后两位
            [0,8,0x1,0xC], # bat_production_time_mm 生产时间(mm): 
            [0,8,0x1,0x1F], # bat_production_time_dd 生产时间(dd): 
            [0,16,0x0000,0xFFFF], # serial 生产线流水号: 0x0:未知 0x1--0xFFFF第X组 
            [0,120,0,0], # res10 预留: NA
        ]

    def decode(self, buffer):
        if len(buffer) != self.totalMcuDataLen:
            log.e('mcu数据长度错误。实际长度为{} 期望值为{}'.format(len(buffer), self.totalMcuDataLen))
            return
        iBit = 0
        itemCount = len(self.dataList)
        for i in range(0, itemCount):
            if self.dataList[i][2] == 0 and self.dataList[i][3] == 0: # 预留字段
                iBit += self.dataList[i][1]
            elif self.dataList[i][1] % 8 == 0 and self.dataList[i][1] > 0 and self.dataList[i][1] <= 32: # 8位，16位，24位，32位数据
                j = int(iBit / 8)
                byteCount = self.dataList[i][1] / 8
                data = 0
                for k in range(0, byteCount):
                    data += (buffer[j + k] << (k * 8))
                self.setData(i, data)
                iBit += self.dataList[i][1]
            elif self.dataList[i][1] < 8 and self.dataList[i][1] > 0: # 8位以内的数据
                j = int(iBit / 8)
                offset = iBit % 8
                mask = 0
                for k in range(0, self.dataList[i][1]):
                    mask += (0x1 << (offset + k))
                self.setData(i, ((buffer[j] & mask) >> offset))
                iBit += self.dataList[i][1]
            else: # 无法解析的没对齐的数据
                iBit += self.dataList[i][1]

    def getData(self, index):
        return self.dataList[index][0]

    def setData(self, index, data):
        if data >= self.dataList[index][2] and data <= self.dataList[index][3]:
            self.dataList[index][0] = data
            return True
        else:
            log.w('写入非法值 index:{} data:{}'.format(index, data))
            return False

    


if __name__ == '__main__':
    mcuData = McuData()