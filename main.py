from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from time import sleep
import configparser
import requests,json
app = Flask(__name__)

CATPI = "https://api.thecatapi.com/v1/images/search"

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

ToDoList = []

# line_bot_api = LineBotApi("10cfe0b9-052c-47ea-95d4-e99fa8761c99")
# handler = WebhookHandler("2bb08b3eefd3898727ae8ab11436a05f")

def get_catimg():
    return requests.get(CATPI).json()[-1]['url']

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
    mess = event.message.text.split(' ')
    if mess[0] == "我要貓咪圖片":
        img = get_catimg()
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=img,
                preview_image_url=img
            )
        )
    elif mess[0] == "加入":
        result = str()
        for part in mess:
            result += part if part != mess[0] else ''
        ToDoList.append(result)
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='已加入 : "'+result+'"'+" 在 " +len(ToDoList))
        )
    elif mess[0] == "檢視":
        result = "_ToDoList_\n"
        for idx,item in enumerate(ToDoList):
            result+= idx+'. '+item+'\n'
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=result)
        )
    elif mess[0] == '刪除':
        del ToDoList[mess[1]]
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="已刪除 "+mess[1])
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='我不知道你在說甚麼@@ : "'+event.message.text+'"')
        )

if __name__ == "__main__":
    app.run()