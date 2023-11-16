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

import bt
import utime
import _thread
import queue
import sys_bus
import osTimer
from machine import Pin
from usr.const import *
from usr.drivers.enpin import gpio_en
from usr.utils.log import log

BT_NAME = 'VC2Pro'
UNLOCK_RSSI = 170
LOCK_RSSI = 160
BT_SCAN_INTERVAL_MS = 3000
WAITING_TO_LOCK_WITHOUT_PHONE_MS = 15000

BT_EVENT = {
    'BT_START_STATUS_IND': 0, # bt/ble start
    'BT_STOP_STATUS_IND': 1, # bt/ble stop
    'BT_SPP_INQUIRY_IND': 6, # bt spp inquiry ind
    'BT_SPP_INQUIRY_END_IND': 7, # bt spp inquiry end ind
    'BT_SPP_RECV_DATA_IND': 14, # bt spp recv data ind
    'BT_HFP_CONNECT_IND': 40, # bt hfp connected
    'BT_HFP_DISCONNECT_IND': 41, # bt hfp disconnected 
    'BT_HFP_CALL_IND': 42, # bt hfp call state 
    'BT_HFP_CALL_SETUP_IND': 43, # bt hfp call setup state 
    'BT_HFP_NETWORK_IND': 44, # bt hfp network state 
    'BT_HFP_NETWORK_SIGNAL_IND': 45, # bt hfp network signal 
    'BT_HFP_BATTERY_IND': 46, # bt hfp battery level 
    'BT_HFP_CALLHELD_IND': 47, # bt hfp callheld state 
    'BT_HFP_AUDIO_IND': 48, # bt hfp audio state 
    'BT_HFP_VOLUME_IND': 49, # bt hfp volume type 
    'BT_HFP_NETWORK_TYPE': 50, # bt hfp network type 
    'BT_HFP_RING_IND': 51, # bt hfp ring indication 
    'BT_HFP_CODEC_IND': 52, # bt hfp codec type
    'BT_SPP_CONNECT_IND': 61, # bt spp connect ind
    'BT_SPP_DISCONNECT_IND': 62, # bt spp disconnect ind
}

HFP_CONN_STATUS = 0

HFP_CONN_STATUS_DICT = {
    'HFP_DISCONNECTED': 0,
    'HFP_CONNECTING': 1,
    'HFP_CONNECTED': 2,
    'HFP_DISCONNECTING': 3,
    }

HFP_CALL_STATUS = 0

HFP_CALL_STATUS_DICT = {
    'HFP_NO_CALL_IN_PROGRESS': 0,
    'HFP_CALL_IN_PROGRESS': 1,
    }

A2DP_AVRCP_CONNECT_STATUS = {
    'DISCONNECTED': 0,
    'CONNECTING': 1,
    'CONNECTED': 2,
    'DISCONNECTING': 3
    }

# DST_DEVICE_INFO = {
#     'dev_name': 'xxx', # 要连接设备的蓝牙名称
#     'bt_addr': None
# }

BT_IS_RUN = 0

def get_key_by_value(val, d):
    for key, value in d.items():
        if val == value:
            return key
    return None


def bt_callback(args):
    print('--callback start-- bt_callback')
    global bt_queue
    bt_queue.put(args) 
    print('--callback end-- bt_callback')

class BT:
    def bt_event_proc_task(self, thread_id):
        global bt_queue
        global BT_IS_RUN
        global BT_NAME
        global BT_EVENT
        global HFP_CONN_STATUS
        global HFP_CONN_STATUS_DICT
        global HFP_CALL_STATUS
        global HFP_CALL_STATUS_DICT
        g_status = self.mmi.getGStatus()
        sys_bus.subscribe('LOCK_MODE', self.onBusMsg)
        # if DEMO_MODE:
        #     self.onBusMsg('LOCK把它从_MODE', MODE_READY_TO_UNLOCK)
        log.d('bt_event_proc_task')
        self.init()
        while True:
            # log.d('wait msg...')
            msg = bt_queue.get() # 没有消息时会阻塞在这
            event_id = msg[0]
            status = msg[1]
            # log.d('get a msg {}'.format(event_id))
            if event_id == BT_EVENT['BT_START_STATUS_IND']:
                self.onBtStart()
                log.d('event: BT_START_STATUS_IND')
                if status == 0:
                    log.i('BT start successfully.')
                    BT_IS_RUN = 1
                    log.d('Set BT name to {}'.format(BT_NAME))
                    retval = bt.setLocalName(0, BT_NAME)
                    if retval != -1:
                        log.d('BT name set successfully.')
                    else:
                        log.e('BT name set failed.')
                        # bt.stop()
                        continue
                    retval = bt.setVisibleMode(3)
                    if retval == 0:
                        mode = bt.getVisibleMode()
                        if mode == 3:
                            log.d('BT visible mode set successfully.')
                        else:
                            log.e('BT visible mode set failed.')
                            # bt.stop()
                            continue
                    else:
                        log.e('BT visible mode set failed.')
                        # bt.stop()
                        continue
                    # if (self.bt_mode == BT_MODE_SCAN_TO_LOCK or self.bt_mode == BT_MODE_SCAN_TO_UNLOCK):
                    #     self.timer.stop()
                    #     self.timer.start(BT_SCAN_INTERVAL_MS, 1, self.onTimerInquiry)
                else:
                    log.e('BT start failed.')
                    # bt.stop()
                    continue
            elif event_id == BT_EVENT['BT_STOP_STATUS_IND']:
                log.d('event: BT_STOP_STATUS_IND')
                if status == 0:
                    BT_IS_RUN = 0
                    log.i('BT stop successfully.')
                else:
                    log.e('BT stop failed.')
                # retval = bt.sppRelease()
                # if retval == 0:
                #     log.d('SPP release successfully.')
                # else:
                #     log.e('SPP release failed.')
                # retval = bt.release()
                # if retval == 0:
                #     log.d('BT release successfully.')
                # else:
                #     log.e('BT release failed.')
                # break
            elif event_id == BT_EVENT['BT_SPP_INQUIRY_IND']:
                log.d('event: BT_SPP_INQUIRY_IND')
                if status == 0:
                    rssi = msg[2]
                    name = msg[4]
                    addr = msg[5]
                    mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
                    log.d('name: {}, addr: {}, rssi: {}'.format(name, mac, rssi))
                    if mac in g_status.settings.unlock_bt_mac_whitelist:
                        log.i('-----Found----- {} {} -----------{}------------'.format(name, mac, rssi))
                        self.phone_nearby = True
                        if rssi > UNLOCK_RSSI and g_status.lock_mode == MODE_LOCK and g_status.settings.no_feeling_lock and self.bt_mode == BT_MODE_SCAN_TO_UNLOCK:
                            self.mmi.setLockMode(MODE_READY_TO_UNLOCK)
                        elif rssi < LOCK_RSSI and (g_status.lock_mode == MODE_READY_TO_LOCK or g_status.lock_mode == MODE_READY_TO_UNLOCK) and g_status.settings.no_feeling_lock and self.bt_mode == BT_MODE_SCAN_TO_LOCK:
                            self.mmi.setLockMode(MODE_LOCK)
                    # if name == DST_DEVICE_INFO['dev_name']:
                    #     log.d('The target device is found, device name {}'.format(name))
                    #     DST_DEVICE_INFO['bt_addr'] = addr
                    #     retval = bt.cancelInquiry()
                    #     if retval != 0:
                    #         log.e('cancel inquiry failed.')
                    #         continue
                else:
                    log.e('BT inquiry failed.')
                    # bt.stop()
                    continue
            elif event_id == BT_EVENT['BT_SPP_INQUIRY_END_IND']:
                log.i('event: BT_SPP_INQUIRY_END_IND')
                # if not self.phone_nearby and g_status.lock_mode == MODE_READY_TO_LOCK and g_status.settings.no_feeling_lock and self.bt_mode == BT_MODE_SCAN_TO_LOCK:
                #     self.mmi.setLockMode(MODE_LOCK)
                # if self.bt_mode == BT_MODE_SCAN_TO_LOCK or self.bt_mode == BT_MODE_SCAN_TO_UNLOCK:
                #     pass
                # if status == 0:
                #     # log.d('BT inquiry has ended.')
                #     inquiry_sta = msg[2]
                #     if inquiry_sta == 0:
                #         if DST_DEVICE_INFO['bt_addr'] is not None:
                #             log.i('Ready to connect to the target device : {}'.format(DST_DEVICE_INFO['dev_name']))
                #             retval = bt.sppConnect(DST_DEVICE_INFO['bt_addr'])
                #             if retval != 0:
                #                 log.e('SPP connect failed.')
                #                 # bt.stop()
                #                 continue
                #         else:
                #             # log.e('Not found device [{}], continue to inquiry.'.format(DST_DEVICE_INFO['dev_name']))
                #             bt.cancelInquiry()
                #             bt.startInquiry(15)
                # else:
                #     log.e('Inquiry end failed.')
                #     # bt.stop()
                #     continue
            elif event_id == BT_EVENT['BT_SPP_RECV_DATA_IND']:
                log.d('event: BT_SPP_RECV_DATA_IND')
                if status == 0:
                    datalen = msg[2]
                    data = msg[3]
                    navi_info = bytes(data).decode()
                    navi_data = navi_info.split(",", 3)
                    if len(navi_data) >= 4:
                        navi_data[0] = MSG_MMI_SET_NAVI_INFO
                        self.mmi.mmi_queue_put(navi_data)
                        log.i('recv {} bytes data: {}'.format(datalen, navi_data))
                    #send_data = 'I have received the data you sent.'
                    #log.d('send data: {}'.format(send_data))
                    #retval = bt.sppSend(send_data)
                    #if retval != 0:
                    #    log.e('send data faied.')
                else:
                    log.e('Recv data failed.')
                    # bt.stop()
                    continue
            elif event_id == BT_EVENT['BT_SPP_CONNECT_IND']:
                log.i('event: BT_SPP_CONNECT_IND')
                if status == 0:
                    conn_sta = msg[2]
                    addr = msg[3]
                    self.connected_mac_addr = addr
                    mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}: {:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
                    log.d('SPP connect successful, conn_sta = {}, addr {}'.format(conn_sta, mac))
                    self.isSppConnected = True
                    self.onBtConnected(mac)
                else:
                    log.e('Connect failed.')
                    # bt.stop()
                    continue
            elif event_id == BT_EVENT['BT_SPP_DISCONNECT_IND']:
                log.i('event: BT_SPP_DISCONNECT_IND')
                conn_sta = msg[2]
                addr = msg[3]
                self.connected_mac_addr = None
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0])
                log.d('SPP disconnect successful, conn_sta = {}, addr {}'.format(conn_sta, mac))
                # bt.stop()
                self.isSppConnected = False
                if not self.isHfpConnected:
                    self.onBtDisconnected()
                continue
            elif event_id == BT_EVENT['BT_HFP_CONNECT_IND']: 
                HFP_CONN_STATUS = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                self.connected_mac_addr = addr
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_CONNECT_IND, {}, hfp_conn_status:{}, mac: {}'.format(status, get_key_by_value(msg[2], HFP_CONN_STATUS_DICT), mac)) 
                if status != 0: 
                    log.e('BT HFP connect failed.') 
                    # bt.stop() 
                    continue 
                self.isHfpConnected = True
                self.onBtConnected(mac)
            elif event_id == BT_EVENT['BT_HFP_DISCONNECT_IND']: 
                HFP_CONN_STATUS = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                self.connected_mac_addr = None
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_DISCONNECT_IND, {}, hfp_conn_status:{}, mac: {}'.format(status, get_key_by_value(msg[2], HFP_CONN_STATUS_DICT), mac)) 
                if status != 0: 
                    log.e('BT HFP disconnect failed.')
                self.isHfpConnected = False
                if not self.isSppConnected:
                    self.onBtDisconnected()
                continue
                # bt.stop() 
            elif event_id == BT_EVENT['BT_HFP_CALL_IND']: 
                call_sta = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_CALL_IND, {}, hfp_call_status:{}, mac: {}'.format(status, get_key_by_value(msg[2], HFP_CALL_STATUS_DICT), mac)) 
                if status != 0: 
                    log.e('BT HFP call failed.') 
                    # bt.stop() 
                    continue 
                if call_sta == HFP_CALL_STATUS_DICT['HFP_NO_CALL_IN_PROGRESS']: 
                    if HFP_CALL_STATUS == HFP_CALL_STATUS_DICT['HFP_CALL_IN_PROGRESS']: 
                        HFP_CALL_STATUS = call_sta 
                        # if HFP_CONN_STATUS == HFP_CONN_STATUS_DICT['HFP_CONNECTED']: 
                        #     log.i('call ended, ready to disconnect hfp.') 
                        #     retval = bt.hfpDisconnect(addr) 
                        #     if retval == 0: 
                        #         HFP_CONN_STATUS = HFP_CONN_STATUS_DICT['HFP_DISCONNECTING'] 
                        #     else:
                        #         log.e('Failed to disconnect hfp connection.') 
                        #         # bt.stop() 
                        #         continue 
                else:
                    if HFP_CALL_STATUS == HFP_CALL_STATUS_DICT['HFP_NO_CALL_IN_PROGRESS']: 
                        HFP_CALL_STATUS = call_sta 
                        log.i('set audio output channel to 2.')
                        bt.setChannel(2) 
                        log.d('set volume to 7.') 
                        retval = bt.hfpSetVolume(addr, 7) 
                        if retval != 0: 
                            log.e('set volume failed.') 
            elif event_id == BT_EVENT['BT_HFP_CALL_SETUP_IND']: 
                call_setup_status = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_CALL_SETUP_IND, {}, hfp_call_setup_status:{}, mac: {}'.format(status, call_setup_status, mac)) 
                if status != 0: 
                    log.e('BT HFP call setup failed.') 
                    # bt.stop() 
                    continue 
            elif event_id == BT_EVENT['BT_HFP_CALLHELD_IND']: 
                callheld_status = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_CALLHELD_IND, {}, callheld_status:{}, mac: {}'.format(status, callheld_status, mac)) 
                if status != 0: 
                    log.e('BT HFP callheld failed.') 
                    # bt.stop() 
                    continue 
            elif event_id == BT_EVENT['BT_HFP_NETWORK_IND']: 
                network_status = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_NETWORK_IND, {}, network_status:{}, mac: {}'.format(status, network_status, mac)) 
                if status != 0: 
                    log.e('BT HFP network status failed.') 
                    # bt.stop() 
                    continue 
            elif event_id == BT_EVENT['BT_HFP_NETWORK_SIGNAL_IND']: 
                network_signal = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_NETWORK_SIGNAL_IND, {}, signal:{}, mac: {}'.format(status, network_signal, mac)) 
                if status != 0: 
                    log.e('BT HFP network signal failed.') 
                    # bt.stop() 
                    continue 
            elif event_id == BT_EVENT['BT_HFP_BATTERY_IND']: 
                battery_level = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_BATTERY_IND, {}, battery_level:{}, mac: {}'.format(status, battery_level, mac)) 
                if status != 0: 
                    log.e('BT HFP battery level failed.')
                    # bt.stop() 
                    continue 
            elif event_id == BT_EVENT['BT_HFP_AUDIO_IND']: 
                audio_status = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.d('BT_HFP_AUDIO_IND, {}, audio_status:{}, mac:{}'.format(status, audio_status, mac)) 
                if status != 0: 
                    log.e('BT HFP audio failed.') 
                    # bt.stop() 
                    continue 
            elif event_id == BT_EVENT['BT_HFP_VOLUME_IND']: 
                volume_type = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_VOLUME_IND, {}, volume_type:{}, mac:{}'.format(status, volume_type, mac)) 
                if status != 0: 
                    log.e('BT HFP volume failed.') 
                    # bt.stop() 
                    continue 
            elif event_id == BT_EVENT['BT_HFP_NETWORK_TYPE']: 
                service_type = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_NETWORK_TYPE, {}, service_type:{}, mac: {}'.format(status, service_type, mac)) 
                if status != 0: 
                    log.e('BT HFP network service type failed.') 
                    # bt.stop() 
                    continue 
            elif event_id == BT_EVENT['BT_HFP_RING_IND']: 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_RING_IND, {}, mac:{}'.format(status, mac)) 
                if status != 0: 
                    log.e('BT HFP ring failed.') 
                    # bt.stop() 
                    continue 
                # retval = bt.hfpAnswerCall(addr) 
                # if retval == 0: 
                #     log.i('The call was answered successfully.') 
                # else:
                #     log.e('Failed to answer the call.') 
                #     # bt.stop() 
                #     continue 
            elif event_id == BT_EVENT['BT_HFP_CODEC_IND']: 
                codec_type = msg[2] 
                addr = msg[3] # BT 主机端mac地址 
                mac = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]) 
                log.i('BT_HFP_CODEC_IND, {}, codec_type:{}, mac:{}'.format(status, codec_type, mac))
                if status != 0: 
                    log.e('BT HFP codec failed.') 
                    # bt.stop() 
                    continue 

    def init(self):
        global BT_NAME
        log.d('BT init start.')
        retval = bt.init(bt_callback)
        if retval == 0:
            log.d('BT init successful.')
        else:
            log.e('BT init failed.')
            return -1
        retval = bt.a2dpavrcpInit()
        if retval == 0:
            log.d('a2dp init successful.')
        else:
            log.e('a2dp init failed.')
            return -1
        retval = bt.hfpInit()
        if retval == 0:
            log.d('HFP init successful.')
        else:
            log.e('HFP init failed.')
            return -1
        retval = bt.sppInit()
        if retval == 0:
            log.d('SPP init successful.')
        else:
            log.e('SPP init failed.')
            return -1
        retval = bt.start()
        if retval == 0:
            log.d('BT start successful.')
        else:
            log.e('BT start failed.')
            # retval = bt.sppRelease()
            # if retval == 0:
            #     log.d('SPP release successful.')
            # else:
            #     log.e('SPP release failed.')
            return -1
        log.d('set audio output channel to 2.')
        bt.setChannel(2)
        local_addr = bt.getLocalAddr()
        log.d(local_addr)
        BT_NAME += '-{:02X}{:02X}'.format(local_addr[1], local_addr[0])

    def onBusMsg(self, topic, msg):
        g_status = self.mmi.getGStatus()
        if topic == 'LOCK_MODE':
            if msg == MODE_LOCK:
                if g_status.settings.no_feeling_lock:
                    self.setBTMode(BT_MODE_SCAN_TO_UNLOCK)
                else:
                    self.setBTMode(BT_MODE_STOP)
            elif msg == MODE_READY_TO_LOCK: # 关电放边撑坐垫无人以后的状态
                if g_status.settings.no_feeling_lock:
                    self.setBTMode(BT_MODE_SCAN_TO_LOCK)
            elif msg == MODE_UNLOCK:
                self.setBTMode(BT_MODE_NORMAL)
            elif msg == MODE_READY_TO_UNLOCK:
                # self.setBTMode(BT_MODE_NORMAL)
                self.setBTMode(BT_MODE_SCAN_TO_LOCK)

    def onTimerInquiry(self, a):
        retval = bt.cancelInquiry()
        if retval is not 0:
            log.e('failed to stop inquiry')
        retval = bt.startInquiry(15)
        if retval is not 0:
            log.e('failed to start inquiry')
            
    def onTimerLock(self, a):
        if self.phone_nearby:
            log.i('onTimerLock there is whitelist phone nearby, restart timer to scan')
            self.phone_nearby = False
            self.lock_timer.start(WAITING_TO_LOCK_WITHOUT_PHONE_MS, 0, self.onTimerLock)
        else:
            g_status = self.mmi.getGStatus()
            if g_status.settings.unlock_bt_mac_whitelist != None and len(g_status.settings.unlock_bt_mac_whitelist) > 0:
                self.mmi.setLockMode(MODE_LOCK)

    def setBTMode(self, mode):
        self.bt_mode = mode
        if mode == BT_MODE_SCAN_TO_UNLOCK:
            log.i('BT MODE :  ---------- BT_MODE_SCAN_TO_UNLOCK ----------')
            self.disconnectBT()
            bt.start()
            self.timer.stop()
            self.timer.start(BT_SCAN_INTERVAL_MS, 1, self.onTimerInquiry)
            self.lock_timer.stop()
        elif mode == BT_MODE_SCAN_TO_LOCK:
            log.i('BT MODE :  ---------- BT_MODE_SCAN_TO_LOCK ----------')
            self.disconnectBT()
            self.phone_nearby = False
            bt.start()
            self.timer.stop()
            self.timer.start(BT_SCAN_INTERVAL_MS, 1, self.onTimerInquiry)
            self.lock_timer.stop()
            self.lock_timer.start(WAITING_TO_LOCK_WITHOUT_PHONE_MS, 0, self.onTimerLock)
        elif mode == BT_MODE_NORMAL:
            log.i('BT MODE :  ---------- BT_MODE_NORMAL ----------')
            # bt.stop()
            # utime.sleep_ms(2000)
            bt.start()
            self.timer.stop()
            self.lock_timer.stop()
        elif mode == BT_MODE_STOP:
            log.i('BT MODE :  ---------- BT_MODE_STOP ----------')
            self.timer.stop()
            self.lock_timer.stop()
            bt.stop()

    def disconnectBT(self):
        if self.connected_mac_addr is not None:
            try:
                bt.a2dpDisconnect(self.connected_mac_addr)
                bt.hfpDisconnect(self.connected_mac_addr)
                bt.sppDisconnect()
            except:
                log.e('disconnect BT fail')


    def onBtConnected(self, mac):
        self.mmi.setBtStatus(BT_STATUS_CONNECTED)
        if DEMO_MODE:
            g_status = self.mmi.getGStatus()
            g_status.settings.unlock_bt_mac_whitelist.append(mac)
            self.mmi.pauseDemo()

    def onBtDisconnected(self):
        self.mmi.setBtStatus(BT_STATUS_NOT_CONNECTED)
        if DEMO_MODE:
            self.mmi.resumeDemo()
        
    def onBtStart(self):
        self.mmi.setBtStatus(BT_STATUS_NOT_CONNECTED)

    def __init__(self, mmi):
        global bt_queue
        self.mmi = mmi
        self.bt_mode = BT_MODE_NORMAL
        self.phone_nearby = False
        self.timer = osTimer()
        self.lock_timer = osTimer()
        self.connected_mac_addr = None # 当前连接的蓝牙mac地址
        self.isSppConnected = False
        self.isHfpConnected = False
        bt_queue = queue.Queue(30)
        self.audio_en = gpio_en(AUDIO_PA_EN_PIN, 0, "audio_en")
        self.audio_en.enable()
        _thread.start_new_thread(self.bt_event_proc_task, (THREAD_ID_BT,))


if __name__ == '__main__':
    classicbt = BT(None)