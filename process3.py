# %%
# 設問３
# サーバが返すpingの応答時間が長くなる場合、サーバが過負荷状態になっていると考えられる。
# そこで、直近m回の平均応答時間がtミリ秒を超えた場合は、サーバが過負荷状態になっているとみなそう。
# 設問2のプログラムを拡張して、各サーバの過負荷状態となっている期間を出力できるようにせよ。mとtはプログラムのパラメータとして与えられるようにすること。

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

pattern=re.compile('(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2}),(.+/\d+),(.+)')


status=defaultdict(lambda: {'timeout':0, 'timeover':0})  # {(ipアドレス):{timeout:(連続タイムアウト回数),timeover:(連続timeover回数)}のdict
timeout_start=dict()  # {(ipアドレス):(timeout開始時刻または0)}のdict
timeover_start=dict()  # {(ipアドレス):(timeover開始時刻または0)}のdict
failure_ids=dict()  # {(ipアドレス):(故障idまたは0)}のdict
overload_ids=dict()  # {(ipアドレス):(過負荷idまたは0)}のdict
result=dict()  # {故障id:{status:('failure'または'overload'),ip:(ipアドレス),start:(故障開始時間), end:(故障復旧時間)}}のdict
counter=10001

for log in logs:
    matches=pattern.match(log).groups()
    ip,resp_time=matches[6:]
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
            result[overload_ids[ip]]={'ip':ip,'status':'overload','start':timeover_start[ip],'end':None}
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
data.to_csv('./output3.tsv',sep='\t')

    

# %%
