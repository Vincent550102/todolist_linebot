from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    TemplateSendMessage
)

from time import sleep
import configparser,requests,json
app = Flask(__name__)

CATPI = "https://api.thecatapi.com/v1/images/search"
# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
FUNC_push = False
FUNC_delete = False


# line_bot_api = LineBotApi("10cfe0b9-052c-47ea-95d4-e99fa8761c99")
# handler = WebhookHandler("2bb08b3eefd3898727ae8ab11436a05f")

def get_catimg():
    return requests.get(CATPI).json()[-1]['url']

def reply_mess(event, mess):
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=mess)
    )

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    print(event)
    mess = event.message.text.split(' ')
    uid = event.source.user_id
    if mess[0] == "我要貓咪圖片":
        img = get_catimg()
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=img,
                preview_image_url=img
            )
        )
    elif mess == "加入" or FUNC_push:
        if FUNC_push:
            if mess == "取消":
                reply_mess(event, "已取消加入動作")
            else:
                db = json.load(open('DataBase.json', encoding='utf-8'))
                if uid in db:
                    db[uid]['todolist'].append(result)
                else:
                    db[uid] = {
                        "uid" : uid,
                        "todolist" : [result],
                        "nickname" : "nickname"
                    }
                print(db[uid]['todolist'])
                reply_mess(event, '已加入 : {} 在 {}'.format(mess,str(len(db[uid]['todolist']))))
                with open('DataBase.json','w',encoding='utf-8') as f:
                    json.dump(db,f,indent=2,sort_keys=True,ensure_ascii=False)
            FUNC_push = False
        else:
            reply_mess(event, '請輸入您要加入的待辦事項~')
            FUNC_push = True

    elif mess[0] == "檢視":
        result = '_ToDoList_\n'
        db = json.load(open('DataBase.json', encoding='utf-8'))
        print(db)
        for idx,item in enumerate(db[uid]['todolist']):
            result += '{}. {}\n'.format(str(idx+1),item)
        print(db)
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=result)
        )
    elif mess[0] == '刪除':
        db = json.load(open('DataBase.json', encoding='utf-8'))
        del db[uid]['todolist'][int(mess[1])-1]
        print(db)
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="已刪除 "+str(mess[1]))
        )
        with open('DataBase.json','w',encoding='utf-8') as f:
            json.dump(db,f,indent=2,sort_keys=True,ensure_ascii=False)
    elif mess[0] == 'test':
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='ToDoList Menu',
                    text='請選擇動作',
                    actions=[
                        MessageTemplateAction(
                            label='檢視(check)',
                            text='檢視'
                        ),
                        MessageTemplateAction(
                            label='加入(push)',
                            text='加入'
                        ),
                        MessageTemplateAction(
                            label='刪除(delete)',
                            text='刪除'
                        )
                    ]
                )
            )
    )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='我不知道你在說甚麼@@ : "'+event.message.text+'"')
        )

if __name__ == "__main__":
    app.run()