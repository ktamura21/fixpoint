# %%
# 設問２
# ネットワークの状態によっては、一時的にpingがタイムアウトしても、一定期間するとpingの応答が復活することがあり、
# そのような場合はサーバの故障とみなさないようにしたい。
# N回以上連続してタイムアウトした場合にのみ故障とみなすように、設問1のプログラムを拡張せよ。
# Nはプログラムのパラメータとして与えられるようにすること。

import re
from datetime import datetime
import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

with open('./sample.txt') as f:
    logs=f.readlines()

N=2

pattern=re.compile('(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2}),(.+/\d+),(.+)')
status=dict()  # {(ipアドレス):(連続タイムアウト回数)}のdict
timeout_start=dict()  # {(ipアドレス):(timeout開始時刻または0)}のdict
failure_ids=dict()  # {(ipアドレス):(故障idまたは0)}のdict
result=dict()  # {故障id:{ip:ipアドレス, start:故障開始時間, end:故障復旧時間}}のdict
counter=10001

for log in logs:
    matches=pattern.match(log).groups()
    ip,resp_time=matches[6:]
    year,month,day,hour,min,sec=[int(s) for s in matches[:6]]
    time=datetime(year,month,day,hour,min,sec)

    # 故障の場合
    if resp_time=='-': 
        status[ip]=status.get(ip,0)+1
        # 新たに故障した場合
        if status.get(ip,0)==N:
            failure_ids[ip]=counter
            result[failure_ids[ip]]={'ip':ip,'start':timeout_start[ip],'end':None}
            counter+=1
        # 新たにタイムアウトし出した場合
        elif status.get(ip,0)==1:
            timeout_start[ip]=time

    # 故障していない場合
    elif int(resp_time)>=0:
        # 故障から復旧した場合
        if status.get(ip,0)>=N:
            result[failure_ids[ip]]['end']=time
        status[ip]=0
        timeout_start[ip]=0
        failure_ids[ip]=0

    else:
         raise ValueError()

data=pd.DataFrame.from_dict(result,orient='index')
data.to_csv('./output.tsv',sep='\t')

    

# %%
