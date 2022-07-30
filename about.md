# コード全体
## 使用環境
- OS: Ubuntu-20.04 on Windows11 wsl2
- エディタ: Visual Studio Code 1.69.2
- 言語: python 3.10.4

## 説明中の用語
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

- 現在  
入力ファイルを先頭から処理していくにあたって、現在読み込んでいる行に書かれた時刻を指す


# 設問1
## 概要
入力ファイルを先頭から順に読み込み、応答時間が"-"のログを検知し次第時刻を`result`に記録、応答が戻り次第再び時刻を`result`に記録する。

## 主な変数
- failure  
ipアドレスをkeyに、現在故障中の場合は故障IDをvalueに、そうでない場合は0を持つDict型変数 

- result  
故障IDをkeyに、ipアドレス／故障開始時間／故障復旧時間を記録したDict型変数をvalueにもつDict型変数
```
{故障id:{
    ip:ipアドレス,
    start:故障開始時間,
    end:故障復旧時間
    },
...
}
```
## 出力
tsvの形式で`./output1.tsv`に保存

# 設問2
## 概要
設問1と異なりtimeoutを検知した際にはまず`status`に回数を、`timeout_start`に時刻を記録し、連続N回timeoutを検知した時に`timeout_start`から`result`に時刻を転記する。

## 主な変数
- N  
故障とみなす連続timeout回数

- status  
ipアドレスをkeyに、連続timeout回数をvalueにもつdict型変数

- timeout_start
ipアドレスをkeyに、現在timeout中の場合は最初のtimeout時刻をvalueに、そうでない場合は0をvalueに持つdict型変数  
timeoutがN回に達したときに呼び出す

- failure_ids  
ipアドレスをkeyに、現在故障中の場合は故障IDをvalueに、そうでない場合は0を持つDict型変数 

- result
設問1と同じ

## 出力
tsvの形式で'./output2.tsv'に保存

# 設問3
## 概要
設問2でtimeoutについて行った処理をtimeoverについても行うように変更した。



## 主な変数
- status  
ipアドレスをkeyに、連続timeout回数と連続timeover回数をvalueにもつdict型変数
```
{IPアドレス:{
    timeout:(連続timeout回数),
    timeover:(連続timeover回数)
    },
...
}
```

- timeout_start
設問2と同じ

- timeover_start
ipアドレスをkeyに、現在timeover中の場合は最初のtimeout時刻をvalueに、そうでない場合は0をvalueに持つdict型変数  
timeoverがm回に達したときに呼び出す

- failure_ids  
設問2と同じ

- overload_ids
ipアドレスをkeyに、現在過負荷の場合は過負荷IDをvalueに、そうでない場合は0を持つDict型変数

# 設問4
## 概要
設問3をベースに作成した。  
最初に一度入力ファイルを探索してネットワークの構成を調べて`network_ip_dict`に記録してから本処理に入った。
あるIPアドレスに対して故障が確認された場合に同一ネットワークの故障状態も調べ、全てのIPが故障していた場合に`result_nw`に時刻を記録する(ここまでの設問と異なりN回目のtimeoutを検知した時刻を故障開始時刻とする)
故障中のネットワークのいずれかのIPアドレスから応答を検知した時刻を故障終了時刻として`result_nw`に記録する

## 主な変数
- network_ip_dict  
ネットワークアドレスをkeyに、そのネットワークに属するすべてのIPアドレスのsetをvalueにもつdefault-dict型変数

- nwfailure_ids
ネットワークアドレスをkeyに、現在ネットワーク故障中の場合は最後に開始した故障の故障IDをvalueに、そうでない場合は0を持つDict型変数

- result_nw
ネットワーク故障の一覧
故障IDをkeyに、ipアドレス／故障開始時間／故障復旧時間を記録したDict型変数をvalueにもつDict型変数