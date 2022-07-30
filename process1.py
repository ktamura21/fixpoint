# %%
# 設問１
# 監視ログファイルを読み込み、故障状態のサーバアドレスとそのサーバの故障期間を出力するプログラムを作成せよ。
# 出力フォーマットは任意でよい。
# なお、pingがタイムアウトした場合を故障とみなし、最初にタイムアウトしたときから、次にpingの応答が返るまでを故障期間とする。

import re
from datetime import datetime
import pandas as pd
import os

os.chdir(os.path.dirname(__file__))

with open('./sample.txt') as f:
    logs=f.readlines()


pattern=re.compile('(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2}),(.+/\d+),(.+)')
failure=dict()  # {(故障中のipアドレス):(故障idまたは0)}のdict
result=dict()  # {故障id:{ip:ipアドレス, start:故障開始時間, end:故障復旧時間}}のdict
counter=10001

for log in logs:
    matches=pattern.match(log).groups()
    ip,resp_time=matches[6:]
    year,month,day,hour,min,sec=[int(s) for s in matches[:6]]
    time=datetime(year,month,day,hour,min,sec)

    # 故障の場合
    if resp_time=='-': 
        # 新たに故障した場合
        if failure.get(ip,0)==0:
            failure[ip]=counter
            result[failure[ip]]={'ip':ip,'start':time,'end':None}
            counter+=1

    # 故障していない場合
    elif int(resp_time)>=0:
        # 故障から復旧した場合
        if failure.get(ip,0)!=0:
            result[failure[ip]]['end']=time
            failure[ip]=0

    else:
         raise ValueError()

data=pd.DataFrame.from_dict(result,orient='index')
data.to_csv('./output.tsv',sep='\t')

    

# %%
