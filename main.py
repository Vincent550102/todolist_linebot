from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from time import sleep
import configparser

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# line_bot_api = LineBotApi("10cfe0b9-052c-47ea-95d4-e99fa8761c99")
# handler = WebhookHandler("2bb08b3eefd3898727ae8ab11436a05f")


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    print("ok")
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    mess = event.message.text.split(" ")
    cnt = int()
    for me in mess:
        print(me)
        if(me.isdigit()):
            cnt = int(me)
    resul_mess = ""
    for i in range(cnt):
        resul_mess+='★'

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=resul_mess)
    # )
    for i in range(50):
        sleep(1)
        line_bot_api.push_message(
            event.source.userId,
            text="ww"
            )
    
    print("sent ok")

if __name__ == "__main__":
    app.run()