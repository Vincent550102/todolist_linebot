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
from env import CATPI
from UserDataBaseTemplate import create_DB_Template
app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

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
    mess = event.message.text
    uid = event.source.user_id
    db = json.load(open('DataBase.json', encoding='utf-8'))
    try:
        FUNC_push = db[uid]['user_status']['FUNC_push']
        FUNC_delete = db[uid]['user_status']['FUNC_delete']
    except:
        db[uid] = create_DB_Template(uid)
        FUNC_push = db[uid]['user_status']['FUNC_push']
        FUNC_delete = db[uid]['user_status']['FUNC_delete']
    print(FUNC_push,FUNC_delete)
    if mess == 'debug':
        reply_mess(event, '''
    uid : {}
    FUNC_push : {}
    FUNC_delete : {}
'''.format(uid,FUNC_push,FUNC_delete))

    elif mess == "加入" or FUNC_push:
        if FUNC_push:
            if mess == "取消":
                reply_mess(event, "已取消加入動作")
            else:
                db[uid]['todolist'].append(mess)
                print(db[uid]['todolist'])
                line_bot_api.push_message(uid,TextMessage(text='test'))
                reply_mess(event, '已加入 : {} 在 {}'.format(mess,str(len(db[uid]['todolist']))))
            FUNC_push = False
        else:
            reply_mess(event, '請輸入您要加入的事項~ 若想放棄請輸入"取消"')
            FUNC_push = True

    elif mess == "檢視":
        result = '_ToDoList_\n'
        db = json.load(open('DataBase.json', encoding='utf-8'))
        print(db)
        for idx,item in enumerate(db[uid]['todolist']):
            result += '{}. {}\n'.format(str(idx+1),item)
        print(db)
        reply_mess(event, result+'[uid : {}]'.format(uid))

    elif mess == '刪除' or FUNC_delete:
        if FUNC_delete:
            if mess == "取消":
                reply_mess(event, "已取消刪除動作")
            else:
                db = json.load(open('DataBase.json', encoding='utf-8'))
                del db[uid]['todolist'][int(mess)-1]
                print(db)
                reply_mess(event, '已刪除 {}'.format(str(mess)))
            FUNC_delete = False
        else:
            reply_mess(event, '請輸入您要刪除的待辦事項~ 若想放棄請輸入"取消"')
            FUNC_delete = True

    elif mess == 'todolist_menu':
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

    elif mess == "我要貓咪圖片":
        img = get_catimg()
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=img,
                preview_image_url=img
            )
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text='我不知道你在說甚麼@@ : "'+event.message.text+'"')
        )
    print(FUNC_push, FUNC_delete)
    db[uid]['user_status']['FUNC_push'] = FUNC_push
    db[uid]['user_status']['FUNC_delete'] = FUNC_delete

    with open('DataBase.json','w',encoding='utf-8') as f:
        json.dump(db,f,indent=2,sort_keys=True,ensure_ascii=False)


if __name__ == "__main__":
    app.run()