"""
Created by matsubara@morikatron.co.jp
Copyright (c) 2021 Morikatron Inc. All rights reserved.

GeneralTalker（雑談専用会話API）を使ったTwitter botのサンプルプログラム
"""

import json
import queue
from typing import Callable, Dict, List, Tuple, Union
import tweepy
import requests
import threading

# GeneralTalkerのURLとapi-key（api-keyはRakuten Rapid APIサイトから入手してXXXX部分を差し替えてください）
GeneralTalker_url: str = "https://generaltalker.p.rapidapi.com/on_twitter/"
GeneralTalker_headers: Dict[str, str] = {
    'x-rapidapi-key': "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    'x-rapidapi-host': "generaltalker.p.rapidapi.com"
}

# APIキーとトークン（twitterの開発者サイトから入手してXXXX部分を差し替えてください）
api_key: str = "XXXXXXXXXXXXXXXXXXXXXXXXX"
api_secret_key: str = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token: str = "XXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret: str = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# メッセージのキューを作成しておきます（多数のリクエストを順次処理するため）
msg_queue: queue.Queue = queue.Queue()

# Twitterのメッセージid(status id)とGeneralTalkerのメッセージidを変換するための辞書
msg_id_dict: Dict[int, int] = {}


# statusから整形された text を返す関数（ツイートから不要な要素（メンション）を削除、改行をスペースに）
def status_to_tweet_text(status: tweepy.models.Status) -> str:
    t: str
    if status.truncated:
        # 長いツィートの文章はextended_tweetの'full_text'に格納されている
        t = status.extended_tweet['full_text']
    else:
        # 普通の長さのツィート
        t = status.text
    # メンションがあったら削除
    if len(status.entities['user_mentions']) > 0:
        # メンションに位置は entities の user_mentions に開始・終了位置が格納されている
        indices_list: List[List[int]] = [m['indices'] for m in status.entities['user_mentions']]  # リストの中身は、開始・終了位置  例）[3, 16]
        # 降順にソート（末尾の方から順に処理するため）
        indices_list = sorted(indices_list, key=lambda x: -x[0])
        # テキストから不要な部分をカット
        indices: List[int]
        for indices in indices_list:
            t = t[:indices[0]] + t[indices[1]:]
    t = t.strip()  # 余白削除
    t = t.replace("\n", " ")  # 改行をスペースに
    return t


# 実行用のクラス
class TwitterEngine(object):

    def __init__(self, user_message_handler: Callable[[str, str, int, int], None]) -> None:
        # tweepyのインスタンス作成
        auth: tweepy.OAuthHandler = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        self.api: tweepy.API = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)
        self.bot_name: str = str(self.api.me().id)
        self.user_message_handler = user_message_handler

    def start_listener(self):
        # StreamListner生成
        listener: TwitterEngine.StreamListener = self.StreamListener(self.api, self.user_message_handler)
        self.stream: tweepy.Stream = tweepy.Stream(auth=self.api.auth, listener=listener)
        self.stream.filter(follow=[self.bot_name], is_async=False)

    class StreamListener(tweepy.StreamListener):
        def __init__(self, api: tweepy.API, user_message_handler: Callable[[str, str, int, int], None]) -> None:
            super().__init__()
            # self.on_user_message に　コールバックを設定
            self.on_user_message: Callable[[str, str, int, int], None] = user_message_handler
            self.api: tweepy.API = api

        # リプライやメンションがあった際に呼ばれる関数
        def on_status(self, status: tweepy.models.Status) -> None:
            tweet_id: int = status.id
            t: str = status_to_tweet_text(status)
            if status.user.id != self.api.me().id:  # ユーザーからのリプライ or メンション
                try:
                    # コールバック(on_message())を呼ぶ
                    screen_name: str = status.user.screen_name
                    self.on_user_message(t, screen_name, tweet_id, status.in_reply_to_status_id)
                except Exception as e:
                    print(e)

        # エラー発生時に呼ばれる関数
        def on_error(self, status_code: int) -> bool:
            print('on_error:', status_code)
            if status_code == 420:  # apiの制限に達すると420が返る
                print(self.api.rate_limit_status())
                return True  # 再接続試みる
            return True  # 420以外の場合もとりあえず再接続試みる

    # Twitterに投稿する関数
    def post_msg(self, to_screen_name: str, text: str, reply_to_status_id: int = None) -> int:
        res_text: str = '@' + to_screen_name + ' ' + text
        try:
            status: tweepy.models.Status = self.api.update_status(res_text, in_reply_to_status_id=reply_to_status_id)
            return status.id
        except Exception as e:
            print('Error at post_msg:', e)
            return -1


# メッセージキューに取得したツィートのデータを格納する関数
def on_message(user_msg_text: str, screen_name: str, tweet_id: int, in_reply_to_status_id: int) -> None:
    global msg_queue
    msg_queue.put((user_msg_text, screen_name, tweet_id, in_reply_to_status_id))


# GeneralTalker で発話を取得 -> Twitterに投稿する関数
def reply_message(twitter_engine: TwitterEngine, user_msg_text: str, screen_name: str, tweet_id: int, in_reply_to_status_id: int) -> None:
    # 返信先のid（Twitterメッセージのid）をGeneralTalkerのメッセージのidに変換する
    reply_to_id: int
    if in_reply_to_status_id in msg_id_dict:
        reply_to_id = msg_id_dict[in_reply_to_status_id]
    else:
        reply_to_id = 0
    # GeneralTalker で返答を取得する
    GeneralTalker_querystring: Dict[str, Union[str, int]] = {
        "bot_name": twitter_engine.bot_name,
        "user_name": screen_name,
        "reply_to_id": reply_to_id,
        "user_msg_text": user_msg_text
    }
    response: requests.Request = requests.request("GET", GeneralTalker_url, headers=GeneralTalker_headers, params=GeneralTalker_querystring)
    # レスポンスのJSONをdictに変換
    dic: Dict = json.loads(response.text)
    # 返答のテキストを取り出す
    reply: str = "……"
    if "response" in dic:
        if "res" in dic["response"]:
            # 返答のテキスト
            reply = dic["response"]["res"]
        if "user_utt_id" in dic["response"]:
            # user_msg_text の GeneralTalkerでのidを記録しておく
            msg_id_dict[tweet_id] = dic["response"]["user_utt_id"]
    # 返答をTwitterに投稿し、投稿したメッセージのidを取得
    reply_id: int = twitter_engine.post_msg(screen_name, reply, tweet_id)
    print(screen_name, ' -> ', user_msg_text)
    print(screen_name, ' <- ', reply)
    if "response" in dic:
        if reply_id > 0 and "bot_utt_id" in dic["response"]:
            # 投稿したメッセージの GeneralTalkerでのidを記録しておく
            msg_id_dict[reply_id] = dic["response"]["bot_utt_id"]


def watch_que(twitter_engine: TwitterEngine) -> None:
    while True:
        # キューから取得したツィートのデータを取り出す
        item: Tuple[str, str, int, int] = msg_queue.get()
        # 返答を生成してTwitterに投稿
        try:
            reply_message(twitter_engine, *item)
        except:
            pass
        msg_queue.task_done()


def main() -> None:
    global msg_queue
    # TwitterEngine のインスタンス作成
    twitter_engine: TwitterEngine = TwitterEngine(on_message)
    # キュー監視スレッドを開始
    t1 = threading.Thread(target=watch_que, args=(twitter_engine,))
    t1.start()
    # ストリームリスナーの開始（リスナーがエラーで落ちてもexceptで拾って復帰できるようにしてみる）
    while True:
        try:
            twitter_engine.start_listener()
        except:
            pass
        print("StreamListener restarted.")


if __name__ == '__main__':
    main()
