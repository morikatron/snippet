"""
Created by Hikaru Yamada
Copyright(c) 2021 Morikatron Inc. All rights reserved.

GeneralTalker（雑談専用会話API）を使ったSlack botのサンプルプログラム
"""

import json
import requests
from slack_bolt import App, Say


# GeneralTalkerのURLとapi-key（Rakuten Rapid APIサイトから入手してください）
generaltalker_url = "https://morikatron-generaltalker.p.rapidapi.com/on_slack/"
generaltalker_headers = {
    'x-rapidapi-key': "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    'x-rapidapi-host': "generaltalker.p.rapidapi.com"
}

# SlackのSIGNING_SECRET と Bot User OAuth Token  （slackの開発者サイトから入手してください）
SLACK_SIGNING_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxx"
SLACK_BOT_TOKEN = "xxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Botの名前(App Nameを推奨)
MY_SLACK_BOT_NAME = "SampleBot"

# slack appを作成
app = App(signing_secret=SLACK_SIGNING_SECRET, token=SLACK_BOT_TOKEN)


@app.event({"type": "message", "subtype": None})
def reply_message(body: dict, say: Say):
    event = body["event"]

    # ユーザのidや発言内容などを取得
    channel_token = event.get('channel')  # 'XXXXXXXXXX'など
    user_name = event.get('user')  # 'XXXXXXXXXX'など
    user_msg_text = event.get('text')  # slackに入力された文字列
    channel_type = event.get('channel_type')  # ダイレクトメッセージの場合'im',チャンネルの場合'channel'となります

    querystring = {
        "bot_name": MY_SLACK_BOT_NAME,
        "user_name": user_name,
        "channel_token": channel_token,
        "user_msg_text": user_msg_text
    }

    response = requests.request(
        "GET", generaltalker_url, headers=generaltalker_headers, params=querystring)

    dic = json.loads(response.text)
    res = dic["response"]["res"]

    # チャンネルでの発言の場合@を付ける
    if channel_type == 'channel':
        res = '<@' + user_name + '>: ' + res
    say(res, channel=channel_token)


# その他のメッセージイベントを受けます（下記がない場合slackからの送信が404になり、イベントが延々再送されます）
@app.event({"type": "message"})
def on_else(body: dict):
    event = body["event"]
    print('その他のメッセージイベント:', event)


if __name__ == "__main__":
    app.start(port=3000)
