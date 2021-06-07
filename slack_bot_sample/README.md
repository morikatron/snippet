# slack bot sample

GeneralTalkerを使ったSlack botのサンプルプログラムです。  

GeneralTalkerは、モリカトロンの「AI会話ジェネレーター」をWebAPI経由で呼び出すサービスです。  
https://api.rakuten.net/morikatroninc-morikatroninc-default/api/generaltalker  

詳しい解説は Morikatron Engineer Blog の記事 「[GeneralTalker APIを使ったSlack botの作り方](https://tech.morikatron.ai/entry/2021/06/07/190000)」をご覧ください。




## ファイルの説明
- slack_bot.py  
GeneralTalkerを使ったSlack botのサンプルコード

## 依存ライブラリ
- slack_bolt
- requests
```
pip install slack_bolt
pip install requests
```

- ngrok   
※Slack APIではホストするサーバーが必要です。  
今回はテスト用のためngrokを使用して説明をさせていただきますが、 本格的に運用する際にはAWSやGoogle Cloudなどのサービスをご活用ください。   
こちらが参考になるかと思います。  
/docs/hosting

## slack apiの設定
1. https://api.slack.com/apps/ の右上「Your Apps」をクリックし、「Create a New App」でbotを作成  
「From scratch」と「From an app manifest」の選択ダイアログが出ますので、「From scratch」を選んで、「App Name」（ボットの名前=自由）と、ボットを動かすワークスペースを指定してください。

2. 左メニューの「OAuth & Permissions」タブの「Bot Token Scopes」で下記を追加  
※「User Token Scopes」ではないのでご注意ください。

    - channels:history
    - im:history
    - chat:write
    - im:write  


3. 「OAuth & Permissions」タブの上方の「Install to Workspace」ボタンをクリックし、SlackのワークスペースにbotのAppを追加

4. 「Basic Information」タブより「Signing Secret」、「OAuth & Permissions」より「Bot User OAuth Token」をそれぞれコピー  
※2021年５月現在、「User OAuth Token」と「Bot User OAuth Token」の両方が表示される場合がありますが、使用するのは「Bot User OAuth Token」ですので、取り間違えないようご注意ください。

5. 「App Home」タブ下方の「Show Tabs」で「Message Tab」をOnにし、その下の「Allow users to send Slash commands and messages from the messages tab」にチェックを入れる。

6. Slackのワークスペースにアクセス。メニューのAppより「アプリを追加する」をクリックし、1で作成したbotを追加  

## 動かし方
slack_bot.pyに上記でコピーした変数を入力してください。
- x-rapidapi-key: Your RAPID API KEY
- SLACK_SIGNING_SECRET: 5でコピーしたSigning Secret
- SLACK_BOT_TOKEN: 5でコピーしたBot User OAuth Token
- MY_SLACK_BOT_NAME: 1で設定したボットの名前

```
ngrok http 3000
python slack_bot.py
```

 https://api.slack.com/ の「Event Subscriptions」タブにて以下の手順を行ってください。


1. 「Enable Events」をOnにし「Request URL」にhttp://xxxxxxngrok.io/slack/eventsを入力。  
※/slack/eventsを入力し忘れないようご注意ください。  
これで「Verified」と表示されたらOKです。

2. 「Subscribe to bot events」で下記を追加。
    - message.channels
    - message.im  
追加後「Save Changes」をクリックしてください。  
※「Save Changes」をクリックしないと設定が消えてしまうのでご注意ください。
  
3. 「Reinstall app to workspace」と表示されたら、クリックしてbotの変更を反映させてあげてください。
