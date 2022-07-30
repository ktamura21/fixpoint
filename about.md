# コード全体
## 使用環境
- OS: Ubuntu-20.04 on Windows11 wsl2
- エディタ: Visual Studio Code 1.69.2
- 言語: python 3.10.4

## 用語
- timeout  
pingの応答時間が"-"で表される状態のこと

- 故障(failure)  
timeoutが同一のipアドレスで所定の回数(設問2以降ではN回)連続すること  
一回目のtimeoutの時刻を故障の開始とし、pingの応答が復活した時刻を故障の復旧とする

- timeover  
pingの応答時間が所定の時間(設問3ではtミリ秒)を超えること  
ただしtimeoutはこれに含まれないものとする

- 過負荷(overload)  
timeoverが所定の回数(設問3ではm回)連続すること
一回目のtimeoutの時刻を故障の開始とし、pingの応答が復活した時刻を故障の復旧とする

- 故障ID／過負荷ID  
故障および過負荷に対して一意に付与される数値、10001から順に付与する


# 設問1
## 主な変数
- failure  
ipアドレスをkeyに、故障の有無をvalueに持つDict型変数  
valueにはログの現在読み込んでいる行の時点で故障しているものは故障IDを、そうでないものは0をもつ

- result  
故障IDをkeyに、ipアドレス／故障開始時間／故障復旧時間を記録したDictionaryをvalueにもつDictionary
```
    {故障id:{
        ip:ipアドレス,
        start:故障開始時間,
        end:故障復旧時間
        }
    }
```
## 出力
tsvの形式で'./output1.tsv'に保存

# 設問2
## 主な変数(変更点)




