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
from random import randint
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

def push_mess(uid, mess):
    line_bot_api.push_message(
        uid,
        TextMessage(text=mess)
    )

def start_random(uid,randrange,spacial):
    num = randint(int(randrange[0]),int(randrange[1]))
    if spacial:
        pass
    push_mess(uid,'恭喜抽到的是 {} 號~'.format(str(num)))


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
        TODO_FUNC_push = db[uid]['ToDoList']['user_status']['FUNC_push']
        TODO_FUNC_delete = db[uid]['ToDoList']['user_status']['FUNC_delete']
        RAND_FUNC_push = db[uid]['RanDom']['user_status']['FUNC_push']
        RAND_FUNC_delete = db[uid]['RanDom']['user_status']['FUNC_delete']
        RAND_FUNC_chose = db[uid]['RanDom']['user_status']['FUNC_chose']
    except:
        db[uid] = create_DB_Template(uid)
        TODO_FUNC_push = db[uid]['ToDoList']['user_status']['FUNC_push']
        TODO_FUNC_delete = db[uid]['ToDoList']['user_status']['FUNC_delete']
        RAND_FUNC_push = db[uid]['RanDom']['user_status']['FUNC_push']
        RAND_FUNC_delete = db[uid]['RanDom']['user_status']['FUNC_delete']
        RAND_FUNC_chose = db[uid]['RanDom']['user_status']['FUNC_chose']

    if mess == 'debug':
        reply_mess(event, '''
    uid : {}
    FUNC_push : {}
    FUNC_delete : {}
'''.format(uid,TODO_FUNC_push,TODO_FUNC_delete))
        print(db)

    elif mess == "TODO_加入" or TODO_FUNC_push:
        if TODO_FUNC_push:
            if mess == "取消":
                reply_mess(event, "已取消加入動作")
            else:
                try:
                    db[uid]['ToDoList']['todolist'].append(mess)
                    reply_mess(event, '已加入 : {} 在 {}'.format(mess,str(len(db[uid]['ToDoList']['todolist']))))
                except:
                    reply_mess(event, '沒有此待辦事項，已取消加入動作')
            TODO_FUNC_push = False
        else:
            reply_mess(event, '請輸入您要加入的事項~ 若想放棄請輸入"取消"')
            TODO_FUNC_push = True

    elif mess == "TODO_檢視":
        result = '_ToDoList_\n'
        for idx,item in enumerate(db[uid]['ToDoList']['todolist']):
            result += '{}. {}\n'.format(str(idx+1),item)
        reply_mess(event, result+'[uid : {}]'.format(uid))

    elif mess == 'TODO_刪除' or TODO_FUNC_delete:
        if TODO_FUNC_delete:
            if mess == "取消":
                reply_mess(event, "已取消刪除動作")
            else:
                try:
                    del db[uid]['ToDoList']['todolist'][int(mess)-1]
                    reply_mess(event, '已刪除 {}'.format(str(mess)))
                except:
                    reply_mess(event, '沒有此待辦事項，已取消刪除動作')
            TODO_FUNC_delete = False
        else:
            reply_mess(event, '請輸入您要刪除的待辦事項~ 若想放棄請輸入"取消"')
            TODO_FUNC_delete = True

    elif RAND_FUNC_push or RAND_FUNC_delete:
        if RAND_FUNC_push:
            if mess == "取消":
                reply_mess(event, "已取消新增動作")
            else:
                key = mess.split(':')[0]
                rang = mess.split(':')[1]
                try:
                    db[uid]['RanDom']['setlist'][key] = rang
                    reply_mess(event, '已新增 {} 在 {}'.format(key,rang))
                except:
                    reply_mess(event, '發生問題，有可能是你的設定名稱輸錯了，已取消新增動作')
            RAND_FUNC_push = False

        elif RAND_FUNC_delete:
            if mess == "取消":
                reply_mess(event, "已取消刪除動作")
            else:
                try:
                    del db[uid]['RanDom']['setlist'][mess]
                    reply_mess(event, '已刪除 : {}'.format(mess))
                except:
                    reply_mess(event, '發生問題，有可能是你的設定名稱輸錯了，已取消刪除動作')
            RAND_FUNC_delete = False

    elif mess == 'RAND_設定' or mess == 'RAND_新增' or mess == 'RAND_刪除':
        if mess == 'RAND_新增':
            reply_mess(event, '請輸入您要新增的設定~ \n[設定檔名]:[numer]~[number] \nex. 310:1~18 \n若想放棄請輸入"取消"')
            RAND_FUNC_push = True
        elif mess == 'RAND_刪除':
            reply_mess(event, '請輸入您要刪除的設定~ 若想放棄請輸入"取消"')
            RAND_FUNC_delete = True
        else:
            curlist = 'curlist\n'
            for idx,key in enumerate(db[uid]['RanDom']['setlist']):
                curlist += '{} : {}\n'.format(key,db[uid]['RanDom']['setlist'][key])
            line_bot_api.reply_message(
                event.reply_token,
                TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        title='目前已有設定檔',
                        text=curlist,
                        actions=[
                            MessageTemplateAction(
                                label='新增(push)',
                                text='RAND_新增'
                            ),
                            MessageTemplateAction(
                                label='刪除(delete)',
                                text='RAND_刪除'
                            )
                        ]
                    )
                )
            )

    elif mess == 'RAND_選設定' or RAND_FUNC_chose:
        if RAND_FUNC_chose:
            if mess == "取消":
                reply_mess(event, "已取消選擇動作")
            else:
                if mess in db[uid]['RanDom']['setlist']:
                    db[uid]['RanDom']['now_set'] = mess
                    reply_mess(event, '已選擇 {}'.format(mess))
                else:
                    reply_mess(event, '發生問題，沒有這個設定檔，已取消選擇動作')
            RAND_FUNC_chose = False
        else:
            curlist = '目前有的設定檔\n'
            for idx,key in enumerate(db[uid]['RanDom']['setlist']):
                curlist += '{} : {}\n'.format(key,db[uid]['RanDom']['setlist'][key])
            curlist += '\n目前選擇的設定檔 : {}\n請輸入您要選擇的設定檔~ 若想放棄請輸入"取消"'.format(db[uid]['RanDom']['now_set'] if db[uid]['RanDom']['now_set'] != '-1' else "null")
            reply_mess(event, curlist)
            RAND_FUNC_chose = True

    elif mess == 'RAND_開始抽':
        if db[uid]['RanDom']['now_set'] == '-1':
            reply_mess(event, '您尚未選擇設定檔，請點選第一個按鈕新增設定檔或第二個按鈕選擇設定檔')
        else:
            now_set = db[uid]['RanDom']['now_set']
            now_range = db[uid]['RanDom']['setlist'][now_set]
            reply_mess(event, '使用設定檔 {} 範圍為 {} 開始抽號~'.format(now_set,now_range))
            start_random(uid,now_range.split('~'),db[uid]['RanDom']['user_status']['FUNC_special'])
    
    elif mess == 'RAND_特殊模式':
        if db[uid]['RanDom']['user_status']['FUNC_special']:
            db[uid]['RanDom']['user_status']['FUNC_special'] = False
            reply_mess(event, '已取消特殊模式')
        else:
            db[uid]['RanDom']['user_status']['FUNC_special'] = True
            reply_mess(event, '已開啟特殊模式')

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
                            text='TODO_檢視'
                        ),
                        MessageTemplateAction(
                            label='加入(push)',
                            text='TODO_加入'
                        ),
                        MessageTemplateAction(
                            label='刪除(delete)',
                            text='TODO_刪除'
                        )
                    ]
                )
            )
        )

    elif mess == 'rand_menu':
        line_bot_api.reply_message(  # 回復傳入的訊息文字
            event.reply_token,
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='Random Menu',
                    text='請選擇動作',
                    actions=[
                        MessageTemplateAction(
                            label='設定(set)',
                            text='RAND_設定'
                        ),
                        MessageTemplateAction(
                            label='選擇設定(chose set)',
                            text='RAND_選設定'
                        ),
                        MessageTemplateAction(
                            label='開始抽號(random)',
                            text='RAND_開始抽'
                        ),
                        MessageTemplateAction(
                            label='特殊模式(special)',
                            text='RAND_特殊模式'
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
    db[uid]['ToDoList']['user_status']['FUNC_push'] = TODO_FUNC_push
    db[uid]['ToDoList']['user_status']['FUNC_delete'] = TODO_FUNC_delete
    db[uid]['RanDom']['user_status']['FUNC_push'] = RAND_FUNC_push
    db[uid]['RanDom']['user_status']['FUNC_delete'] = RAND_FUNC_delete
    db[uid]['RanDom']['user_status']['FUNC_chose'] = RAND_FUNC_chose

    with open('DataBase.json','w',encoding='utf-8') as f:
        json.dump(db,f,indent=2,sort_keys=True,ensure_ascii=False)


if __name__ == "__main__":
    app.run()