# twitter bot sample

GeneralTalkerを使ったTwitter botのサンプルプログラムです。  

GeneralTalkerは、モリカトロンの「AI会話ジェネレーター」をWebAPI経由で呼び出すサービスです。  
https://api.rakuten.net/morikatroninc-morikatroninc-default/api/generaltalker  

詳しい解説は Morikatron Engineer Blog の記事 「[GeneralTalker APIを使ったTwitter botの作り方](https://tech.morikatron.ai/entry/2021/06/07/100000)」をご覧ください。


## ファイルの説明

 - twi_bot.py
    GeneralTalkerを使ったTwitter botのサンプルコード  
 - twi_bot.service
    twi_bot.pyをUbuntuで常駐起動する際の設定ファイル

## 


## 依存ライブラリ

```
pip insatll tweepy
pip insatll requests
```

## 動かし方

#### ターミナルで起動

```
python twi_bot.py
```

#### ubuntuで常駐動作させる場合

ubuntuで常駐動作させたい場合は、SystemDが便利です。  
SystemDの設定ファイル twi_bot.service を、systemdのディレクトリへコピーしていろいろし、起動するまでのコマンドの例を以下に記します。参考にしてください。
```
sudo cp twi_bot.service /etc/systemd/system
sudo chown root:root /etc/systemd/system/twi_bot.service
sudo chmod 644 /etc/systemd/system/twi_bot.service
sudo systemctl start twi_bot.service
```

```
# サービスステータス確認
sudo systemctl status twi_bot.service
# サービス停止
sudo systemctl stop twi_bot.service
# サービスリスタート
sudo systemctl restart twi_bot.service
```
