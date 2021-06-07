from flask import Flask, request, abort
from flask.wrappers import Response
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from typing import Dict, Literal
import requests
import json

# GeneralTalker APIのURLとapi-key（Rakuten Rapid APIサイトから入手してください）
generaltalker_url: str = "https://generaltalker.p.rapidapi.com/on_line/"
generaltalker_headers: Dict[str, str] = {
    'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    'x-rapidapi-host': "generaltalker.p.rapidapi.com"
}

# LINE Messaging API のChannel access token と Channel secret
line_bot_api: LineBotApi = LineBotApi('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
handler: WebhookHandler = WebhookHandler('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

# 送受信用のFlask
app = Flask(__name__)

# ボットのuserIdを取得
bot_name: str = line_bot_api.get_bot_info().user_id


# メッセージ（Webhook）を受信する
@app.route("/callback", methods=['POST'])
def callback() -> Literal['OK']:
    # 署名を取得
    signature: str = request.headers['X-Line-Signature']
    # request body を取得
    body: str = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # webhookの処理
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 署名の検証でエラー
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


# メッセージイベントのハンドラ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event) -> None:
    # 送信元のuserIdを取得
    user_name: str = event.source.user_id
    # GeneralTalker API での channel_tokenを取得
    channel_token: str
    if event.source.type == 'user':
        # 一対一のトークの場合
        channel_token = user_name
    elif event.source.type == 'group':
        # グループトークの場合
        channel_token = event.source.group_id
    elif event.source.type == 'room':
        # トークルームの場合
        channel_token = event.source.room_id

    # GeneralTalker API で返答を取得する
    querystring: Dict[str, str] = {
        "bot_name": bot_name,
        "user_name": user_name,
        "channel_token": channel_token,
        "user_msg_text": event.message.text
    }
    response: Response = requests.request("GET", generaltalker_url, headers=generaltalker_headers, params=querystring)
    # レスポンスのJSONをdictに変換
    dic: Dict = json.loads(response.text)
    # 返答のテキストを取り出す
    if "response" in dic:
        if "res" in dic["response"]:
            # 返答のテキスト
            reply: str = dic["response"]["res"]
    # 返答をLINEに投稿
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


if __name__ == "__main__":
    app.run(port=3000)  # 受信するポートを環境に合わせて設定してください
