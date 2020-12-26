from linebot import (
    LineBotApi, WebhookHandler
)

line_bot_api = LineBotApi('ArxxWJmB8uU+jiIb/NCsEWdF3sVsIQOxHewSpJbuOft8OJYXKbpr7P6TdjKyrLOjQTS46EgdFzf3FRpF1Q18iw3oXLOTsCb0rMMM+R3LKEB6ebEiGg8zJjOZ6A7Co5VHP4kRWIjeOrdBGJoFrk+Y7AdB04t89/1O/w1cDnyilFU=')

with open("./richmenu/control.png", 'rb') as f:
    line_bot_api.set_rich_menu_image("richmenu-207420da779e3f9e7a212591c20590a4", "image/jpeg", f)