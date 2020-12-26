from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('ArxxWJmB8uU+jiIb/NCsEWdF3sVsIQOxHewSpJbuOft8OJYXKbpr7P6TdjKyrLOjQTS46EgdFzf3FRpF1Q18iw3oXLOTsCb0rMMM+R3LKEB6ebEiGg8zJjOZ6A7Co5VHP4kRWIjeOrdBGJoFrk+Y7AdB04t89/1O/w1cDnyilFU=')

with open("./richmenu/control.png", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-f0f39f6bcdb5a94f8277589312447104", "image/jpeg", f)