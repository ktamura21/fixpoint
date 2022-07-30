# %%
# 設問4
# ネットワーク経路にあるスイッチに障害が発生した場合、そのスイッチの配下にあるサーバの応答がすべてタイムアウトすると想定される。
# そこで、あるサブネット内のサーバが全て故障（ping応答がすべてN回以上連続でタイムアウト）している場合は、
# そのサブネット（のスイッチ）の故障とみなそう。
# 設問2または3のプログラムを拡張して、各サブネット毎にネットワークの故障期間を出力できるようにせよ。

import re
from datetime import datetime
import pandas as pd
from collections import defaultdict
import os

os.chdir(os.path.dirname(__file__))

with open('./sample.txt') as f:
    logs=f.readlines()

N=2
M=3
T=100

pattern=re.compile('(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2}),(.+)/(\d+),(.+)')
pattern2=re.compile('(\d+)\.(\d+)\.(\d+)\.(\d+)')

status=defaultdict(lambda: {'timeout':0, 'timeover':0})  # {(ipアドレス):{timeout:(連続タイムアウト回数),timeover:(連続timeover回数)}のdict
timeout_start=dict()  # {(ipアドレス):(timeout開始時刻または0)}のdict
timeover_start=dict()  # {(ipアドレス):(timeover開始時刻または0)}のdict
failure_ids=dict()  # {(ipアドレス):(故障idまたは0)}のdict
overload_ids=dict()  # {(ipアドレス):(過負荷idまたは0)}のdict
result=dict()  # {故障id:{status:('failure'または'overload'),ip:(ipアドレス),start:(故障開始時間), end:(故障復旧時間)}}のdict
counter=10001

# ipアドレスとネットワークプレフィックス長からネットワークアドレスを返す関数
def get_network_ip(ip,subnet_len):
    ip_list=[int(i) for i in pattern2.match(ip).groups()]

    ip_num=0
    for n in ip_list:
        ip_num=(ip_num<<8)+n

    subnet_num=0
    for i in range(32):
        subnet_num+=int(i<subnet)
        subnet_num=subnet_num<<1

    temp=ip_num & subnet_num
    network_ip=[]
    for _ in range(4):
        network_ip.append(temp%256)
        temp=temp>>8

    return(f'{str(network_ip[3])}.{str(network_ip[2])}.{str(network_ip[1])}.{str(network_ip[0])}')


for log in logs:
    matches=pattern.match(log).groups()
    ip,subnet_len,resp_time=matches[6:]
    subnet_len=int(subnet_len)
    subnet=get_network_ip(ip,subnet_len) # ipアドレスのネットワーク部
    year,month,day,hour,min,sec=[int(s) for s in matches[:6]]
    time=datetime(year,month,day,hour,min,sec)

    # timeoutの場合
    if resp_time=='-': 
        status[ip]['timeout']+=1
        status[ip]['timeover']=0
        # 連続timeoutがN回に達した場合
        if status[ip]['timeout']==N:
            failure_ids[ip]=counter
            result[failure_ids[ip]]={'ip':ip,'status':'failure','start':timeout_start[ip],'end':None}
            counter+=1
        # 新たにtimeoutし出した場合
        elif status[ip]['timeout']==1:
            timeout_start[ip]=time

    #timeoverの場合
    elif int(resp_time)>=T:
        status[ip]['timeout']=0
        status[ip]['timeover']+=1
        # 連続timeoverがM回に達した場合
        if status[ip]['timeover']==M:
            overload_ids[ip]=counter
            result[overload_ids[ip]]={'ip':ip,'status':'overload','start':timeout_start[ip],'end':None}
            counter+=1
        # 新たにtimeoverし出した場合
        elif status[ip]['timeover']==1:
            timeover_start[ip]=time

    # 正常な場合
    elif int(resp_time)>=0:
        # 故障から復旧した場合
        if status[ip]['timeout']>=N:
            result[failure_ids[ip]]['end']=time
        # 過負荷から復旧した場合
        if status[ip]['timeover']>=M:
            result[overload_ids[ip]]['end']=time
        status.pop(ip,None)
        timeout_start[ip]=0
        timeover_start[ip]=0
        failure_ids[ip]=0
        overload_ids[ip]=0

    else:
         raise ValueError()

data=pd.DataFrame.from_dict(result,orient='index')
data.to_csv('./output4.tsv',sep='\t')

    

# %%
