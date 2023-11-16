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

import checkNet
import utime
import _thread
from usr.const import *


class NETWORK:
    def __init__(self, mmi):
        self.mmi = mmi
        _thread.stack_size(1024)
        _thread.start_new_thread(self.net_work_env_check_task,(THREAD_ID_NETWORK,))

    def net_work_env_check_task(self, thread_id):
        print(thread_id)
        while 1:
            stagecode, subcode = checkNet.wait_network_connected(30)
            print('stagecode = {}, subcode = {}'.format(stagecode, subcode))
            if stagecode == 1:
                # 如果 subcode = 0，说明没插卡，或者卡槽松动，需要用户去检查确认；
                # 如果是其他值，请参考官方wiki文档中关于sim卡状态值的描述，确认sim卡当前状态，然后做相应处理
                print('no sim card!')
                data = [MSG_MMI_NET_EVENT, NETWORK_EVENT_NO_SIM]
                if self.mmi:
                    self.mmi.mmi_queue_put(data)
                utime.sleep(60)
            elif stagecode == 2:
                print('network register fail!')
                data = [MSG_MMI_NET_EVENT, NETWORK_EVENT_NETWORK_REG_FAIL]
                if self.mmi:
                    self.mmi.mmi_queue_put(data)
                utime.sleep(30)
                # if subcode == -1:
                #     # 这种情况说明在超时时间内，获取注网状态API一直执行失败，在确认SIM卡可正常使用且能正常被模块识
                #     # 别的前提下，可联系我们的FAE反馈问题；
                # elif subcode == 0:
                #     # 这种情况说明在超时时间内，模块一直没有注网成功，这时请按如下步骤排查问题：
                #     # （1）首先确认SIM卡状态是正常的，通过 sim 模块的 sim.getState() 接口获取，为1说明正常；
                #     # （2）如果SIM卡状态正常，确认当前信号强度，通过 net模块的 net.csqQueryPoll() 接口获取，
                #     #     如果信号强度比较弱，那么可能是因为当前信号强度较弱导致短时间内注网不成功，可以增加超时
                #     #      时间或者换个信号比较好的位置再试试；
                #     # （3）如果SIM卡状态正常，信号强度也较好，但就是注不上网，请联系我们的FAE反馈问题；最好将相应
                #     #     SIM卡信息，比如哪个运营商的卡、什么类型的卡、卡的IMSI等信息也一并提供，必要时可以将
                #     #     SIM卡寄给我们来排查问题。
                # else:
                #     # 请参考官方Wiki文档中 net.getState() 接口的返回值说明，确认注网失败原因
            elif stagecode == 3:
                if subcode == 1:
                    # 这是正常返回情况，说明网络已就绪，即注网成功，拨号成功
                    print('data connected!')
                    data = [MSG_MMI_NET_EVENT, NETWORK_EVENT_DATA_CONNECTED]
                    if self.mmi:
                        self.mmi.mmi_queue_put(data)
                    utime.sleep(120)
                else:
                    print('data connected!')
                    data = [MSG_MMI_NET_EVENT, NETWORK_EVENT_DATA_FAIL]
                    if self.mmi:
                        self.mmi.mmi_queue_put(data)
                    utime.sleep(30)
                    # 这种情况说明在超时时间内，拨号一直没有成功，请按如下步骤尝试：
                    # （1）通过 sim 模块的 sim.getState() 接口获取sim卡状态，为1表示正常；
                    # （2）通过 net 模块的 net.getState() 接口获取注网状态，为1表示正常；
                    # （3）手动调用拨号接口尝试拨号，看看能否拨号成功，可参考官方Wiki文档中的 dataCall 模块
                    #     的拨号接口和获取拨号结果接口；
                    # （4）如果手动拨号成功了，但是开机拨号失败，那么可能是默认的apn配置表中没有与当前SIM卡匹配
                    #     的apn，用户可通过 sim 模块的 sim.getImsi() 来获取 IMSI 码，确认IMSI的第四和第五              
                    #     位字符组成的数字是否在 01 ~ 13 的范围内，如果不在，说明当前默认apn配置表中无此类SIM卡对
                    #     应的apn 信息，这种情况下，用户如果希望开机拨号成功，可以使用 dataCall.setApn(...)
                    #     接口来设置保存用户自己的apn信息，然后开机重启，就会使用用户设置的apn来进行开机拨号；
                    # （5）如果手动拨号也失败，那么请联系我们的FAE反馈问题，最好将相应SIM卡信息，比如哪个运营商
                    #     的卡、什么类型的卡、卡的IMSI等信息也一并提供，必要时可以将SIM卡寄给我们来排查问题。
        


if __name__ == '__main__':
    net_set = NETWORK(None)


    