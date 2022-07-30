# %%
# 設問4
# ネットワーク経路にあるスイッチに障害が発生した場合、そのスイッチの配下にあるサーバの応答がすべてタイムアウトすると想定される。
# そこで、あるサブネット内のサーバが全て故障（ping応答がすべてN回以上連続でタイムアウト）している場合は、
# そのサブネット（のスイッチ）の故障とみなそう。
# 設問2または3のプログラムを拡張して、各サブネット毎にネットワークの故障期間を出力できるようにせよ。

from ipaddress import ip_address
import re
from datetime import datetime
import pandas as pd
from collections import defaultdict
import os
import sys

os.chdir(os.path.dirname(__file__))

with open('./sample.txt') as f:
    logs=f.readlines()

N=sys.stdin[1]
# N=4

pattern=re.compile('(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2}),(.+)/(\d+),(.+)')
pattern2=re.compile('(\d+)\.(\d+)\.(\d+)\.(\d+)')

status=defaultdict(lambda: {'timeout':0, 'timeover':0})  # {(ipアドレス):{timeout:(連続タイムアウト回数),timeover:(連続timeover回数)}のdict
timeout_start=dict()  # {(ipアドレス):(timeout開始時刻または0)}のdict
failure_ids=dict()  # {(ipアドレス):(故障idまたは0)}のdict
result=dict()  # {故障id:{status:('failure'または'overload'),ip:(ipアドレス),start:(故障開始時間), end:(故障復旧時間)}}のdict

network_ip_dict=defaultdict(lambda: set()) # {(ネットワークアドレス):(属するipアドレスのset)}のdict
nwfailure_ids=dict() # {(ネットワークアドレス):(故障idまたは0)}のdict
result_nw=dict()  # {故障id:{ip:(ネットワークアドレス),start:(故障開始時間), end:(故障復旧時間)}}のdict

counter=10001

# ipアドレスとネットワークプレフィックス長からネットワークアドレスを返す関数
def get_network_ip(ip,subnet_len):
    ip_list=[int(i) for i in pattern2.match(ip).groups()]

    ip_num=0
    for n in ip_list:
        ip_num=(ip_num<<8)+n

    subnet_num=0
    for i in range(32):
        subnet_num+=int(i<subnet_len)
        subnet_num=subnet_num<<1

    temp=ip_num & subnet_num
    network_ip=[]
    for _ in range(4):
        network_ip.append(temp%256)
        temp=temp>>8

    return(f'{str(network_ip[3])}.{str(network_ip[2])}.{str(network_ip[1])}.{str(network_ip[0])}')

# ipアドレスの一覧の作成
for log in logs:
    matches=pattern.match(log).groups()
    ip,subnet_len,resp_time=matches[6:]
    subnet_len=int(subnet_len)
    subnet=get_network_ip(ip,subnet_len) # ipアドレスのネットワーク部

    network_ip_dict[subnet].add(ip)

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
            # ネットワーク全体が故障しているかの判定
            flag=0
            for address in network_ip_dict[subnet]:
                if failure_ids.get(address,0)==0: flag=1
            if flag==0:
                nwfailure_ids[subnet]=failure_ids[ip]
                result_nw[failure_ids[ip]]={'ip':subnet,'start':time,'end':None}
        # 新たにtimeoutし出した場合
        elif status[ip]['timeout']==1:
            timeout_start[ip]=time

    # 正常な場合
    elif int(resp_time)>=0:
        # 故障から復旧した場合
        if status[ip]['timeout']>=N:
            result[failure_ids[ip]]['end']=time
            # ネットワーク全体の故障の場合の処理
            if nwfailure_ids.get(subnet,0)!=0:
                result_nw[nwfailure_ids[subnet]]['end']=time
                nwfailure_ids[subnet]=0

    else:
         raise ValueError()

data=pd.DataFrame.from_dict(result_nw,orient='index')
data.to_csv('./output4.tsv',sep='\t')


    

# %%
