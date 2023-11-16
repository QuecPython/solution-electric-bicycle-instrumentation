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
import ustruct
import _thread
from ucollections import deque
import queue
from machine import UART
from usr.controller import Controller
from usr.bms import BMS
from usr.utils.log import log


UART_HEAD_LEN = 8
UART_TAIL_LEN = 2
UART_SUM_LEN = 2

class SerialBean:
    def __init__(self):
        self.buffer_len = 0
        self.data_len = 0
        self.is_valid = False
        self.cmd_id = None
        self.data = None
        self.sum = 0

    def calcSum(self):
        sumCalc = 0
        for i in range(0, UART_HEAD_LEN - 1):
            sumCalc += self.cmd_id[i]
        sumCalc += ord(':')
        for i in range(0, self.data_len):
            sumCalc += self.data[i]
        return sumCalc & 0xff


    def checkSum(self):
        if (self.calcSum() == self.sum):
            return True
        else:
            return False

    def updateSum(self):
        self.sum = self.calcSum()


    def fromBytes(self, buffer):
        self.buffer_len = len(buffer)
        self.data_len = self.buffer_len - UART_HEAD_LEN - UART_TAIL_LEN - UART_SUM_LEN
        if not self.isValid():
            self.is_valid = False
            return
        else:
            self.is_valid = True
        self.cmd_id = buffer[:UART_HEAD_LEN - 1]
        self.data = buffer[UART_HEAD_LEN:-UART_TAIL_LEN-UART_SUM_LEN]
        self.sum = buffer[UART_HEAD_LEN + self.data_len]
        if not self.checkSum():
            self.is_valid = False

        # a= bytes()
        # a.replace
        
        # for i in range(0, self.data_len - 1):
        #     if self.data[i] == 0x0d and self.data[i+1] == 0x01:


    def toBytes(self):
        self.updateSum()
        convertedDataLen = self.data_len
        convertedData = bytearray()
        for i in self.data:
            convertedData.append(i)
            if i == 0x0D:
                convertedData.append(0x01)
                convertedDataLen += 1
        convertedData.append(self.sum)
        convertedDataLen += 1
        if self.sum == 0x0D:
            convertedData.append(0x01)
            convertedDataLen += 1

        formatStr = '{}sB{}s2B'.format(UART_HEAD_LEN - 1, convertedDataLen)
        buffer = ustruct.pack(formatStr, self.cmd_id, ord(':'), convertedData, 0x0D,0x0A)
        return buffer

    def isValid(self):
        if (self.data_len < 0):
            return False
        return True


class SERIAL:
    def __init__(self, mmi):
        self.isOrder = False
        self.mmi = mmi
        self.uart = UART(UART.UART2, 115200, 8, 0, 1, 0)
        self.uart.set_callback(self.serial_recv_data_cb) #test
        self.controller = Controller(self, self.mmi)
        self.bms = BMS(self, self.mmi)

        # 双向队列buffer, 接收缓冲区, 从右侧添加数据, 最大256字节, 超过256字节从队列左侧删除
        self.data_buffer = deque((), 256)

        # 存放一包数据的数组, 该包数据拼包完成后, 解码并清空
        self.single_buffer = bytearray()

        _thread.start_new_thread(self.serial_task,(THREAD_ID_SERIAL,))
        # _thread.start_new_thread(self.serial_read_task,(THREAD_ID_SERIAL_READ, ))

    # 读数据线程loop
    def serial_read_task(self, thread_id):
        while 1:
            msgLen = self.uart.any()
            # 当有数据时进行读取
            if msgLen:
                msg = self.uart.read(msgLen)
                # 读取msgLen个字节, 放入data_buffer
                for i in msg:
                    self.data_buffer.append(i)
                # self.data_buffer.extend(serial_data)
                self.decode_data()

    # 收到串口数据的中断回调
    def serial_recv_data_cb(self, para):
        print('--callback start-- serial_recv_data_cb')
        # global serialQueue
        # print(para)
        # toRead 是可以读取的字节数, 把这个字节数发给消息队列处理线程读取数据
        toRead = para[2]
        log.d('uart data callback! toRead : {}'.format(toRead))
        # if toRead > 0:
        self.serial_queue_put([MSG_SERIAL_READ, toRead])
        print('--callback end-- serial_recv_data_cb')

    # 从串口读数据
    def read_data(self, data):
        # len = data[1]
        len = self.uart.any()
        log.d('read len : {}'.format(len))
        if (len > 0):
            serial_data = self.uart.read(len)
            # serial_data = self.uart.read()
            self.hexShow('<<<<< raw <<<<<', serial_data)
            # 读取len个字节, 放入data_buffer
            for i in serial_data:
                self.data_buffer.append(i)
            # self.data_buffer.extend(serial_data)
            self.decode_mcu_data()

    # 封包后写数据
    def write_data(self, data):
        sd = SerialBean()
        sd.cmd_id = data[1]
        sd.data = data[2]
        sd.data_len = len(sd.data)
        sd.buffer_len = sd.data_len + UART_HEAD_LEN + UART_TAIL_LEN
        self.write_raw_data([0, sd.toBytes()])
    
    # 写原始数据
    def write_raw_data(self, data):
        buffer = data[1]
        # self.hexShow('>>>>>>>>>>', buffer)
        log.i('>>>>>>>>>>', buffer)
        self.uart.write(buffer)

    # 解析并处理数据
    def decode_mcu_data(self):
        while len(self.data_buffer) > 0:
            b = self.data_buffer.popleft()
            bufferlen = len(self.single_buffer)
            if bufferlen > 0 and self.single_buffer[-1] == 0x0d and b == 0x01: # 0d 01 转义, 跳过0x01
                pass
            elif bufferlen > 0 and self.single_buffer[-1] == 0x0d and b == 0x0a: # 收到结束符
                if bufferlen < UART_HEAD_LEN + UART_TAIL_LEN - 1:
                    self.single_buffer = bytearray() # 丢弃不完整数据，重新开始接收
                elif bufferlen >= UART_HEAD_LEN + UART_TAIL_LEN - 1 and self.single_buffer[UART_HEAD_LEN - 1] == ord(':'): # 数据有效
                    self.single_buffer.append(b)
                    log.i('<<<<<<<<<<', self.single_buffer)
                    sd = SerialBean() # 解析串口报文
                    sd.fromBytes(self.single_buffer)
                    self.process_mcu_cmd(sd) # 处理串口报文命令
                    self.single_buffer = bytearray()
                else:
                    self.single_buffer = bytearray() # 数据无效，丢弃当前数据，重新接收
            else:
                self.single_buffer.append(b)


            # self.single_buffer.append(b)
            # bufferlen = len(self.single_buffer)
            # if bufferlen == 1:
            #     pass
            # elif 1 < bufferlen and bufferlen < UART_HEAD_LEN + UART_TAIL_LEN:
            #     if self.single_buffer[-2] == 0x0D and self.single_buffer[-1] == 0x0A:
            #         self.single_buffer = bytearray() # 发现结束符，丢弃不完整数据，重新开始接收
            # elif bufferlen >= UART_HEAD_LEN + UART_TAIL_LEN:
            #     if self.single_buffer[-2] == 0x0D and self.single_buffer[-1] == 0x0A: # 发现结束符
            #         if self.single_buffer[UART_HEAD_LEN - 1] == ord(':'): # 数据有效
            #             print('<<<<<<<<<<', self.single_buffer)
            #             sd = SerialBean() # 解析串口报文
            #             sd.fromBytes(self.single_buffer)
            #             self.process_mcu_cmd(sd) # 处理串口报文命令
            #             self.single_buffer = bytearray()
            #         else:
            #             self.single_buffer = bytearray()

    def decode_485_data(self, data):
        if self.controller.checkAddr(data): # 控制器地址
            self.controller.onGotData(data)
        elif self.bms.checkAddr(data): # BMS地址
            self.bms.onGotData(data)

    def processMcuData(self, data):
        g_status = self.mmi.getGStatus()
        self.mmi.get
        

    # 处理串口命令
    def process_mcu_cmd(self, sd):
        if not sd.is_valid:
            print('not valid serial data')
            return
        else:
            if sd.cmd_id == CMD_TYPE_M_C_INFO:
                self.processMcuInfo(sd.data)
            # elif sd.cmd_id == CMD_TYPE_M_C_485: # 485
            #     self.decode_485_data(sd.data)
            

    def serial_task(self, thread_id):
        print("serial_task id %d" % thread_id)
        global serialQueue
        serialQueue = queue.Queue(50)
        self.msg_type_handle_func = (self.read_data, self.write_data)
        if not DEMO_MODE:
            self.controller.start()
        #self.bms.start()
        self.write_data([MSG_SERIAL_WRITE, CMD_TYPE_C_M_BACKLIGHT, b'\x01'])
        while 1:
            msg_data = serialQueue.get()
            # print('got serialQueue msg')
            if (msg_data[0] >= MSG_SERIAL_MAX):
                continue
            self.msg_type_handle_func[msg_data[0]](msg_data)
            print('uart queue len : {}'.format(serialQueue.size()))
            utime.sleep_ms(10)

    def serial_queue_put(self, data):
        global serialQueue
        serialQueue.put(data)
        
    # 十六进制显示
    def hexShow(self, info, argv):
        print(info, argv)
        # try:
        #     result = ''
        #     hLen = len(argv)
        #     for i in range(hLen):
        #         hvol = argv[i]
        #         hhex = '%02x' % hvol
        #         result += hhex+' '

        #     print(info, result)
        # except Exception as e:
        #     print("---异常---:", e)

    def turnBackLightOn(self):
        log.i('turnBackLightOn')
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_BACKLIGHT, b'\x01\x01'])
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_BACKLIGHT, b'\x01'])

    def turnBackLightOff(self):
        log.i('turnBackLightOff')
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_BACKLIGHT, b'\x01\x00'])
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_BACKLIGHT, b'\x00'])

    def lockAll(self):
        log.i('lockAll')
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x01\x00'])
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x02\x00'])
        
    def unLockAll(self):
        log.i('lockAll')
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x01\x01'])
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x02\x01'])

    def study433(self):
        log.i('study433')
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_433, b'\x01\x01'])
        
    def erase433(self):
        log.i('erase433')
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_433, b'\x01\x00'])

    def enable433(self):
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x04\x01'])

    def disable433(self):
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x04\x00'])

    def acc1On(self):
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x05\x01'])

    def acc1Off(self):
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x05\x00'])

    def acc2On(self):
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x06\x01'])
        
    def acc2Off(self):
        self.serial_queue_put([MSG_SERIAL_WRITE, CMD_TYPE_C_M_CCTLOCK, b'\x06\x00'])

if __name__ == '__main__':
    serial = SERIAL(None)