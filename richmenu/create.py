import requests
import json

headers = {"Authorization":"Bearer ArxxWJmB8uU+jiIb/NCsEWdF3sVsIQOxHewSpJbuOft8OJYXKbpr7P6TdjKyrLOjQTS46EgdFzf3FRpF1Q18iw3oXLOTsCb0rMMM+R3LKEB6ebEiGg8zJjOZ6A7Co5VHP4kRWIjeOrdBGJoFrk+Y7AdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1386},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "Controller",
    "areas":[
        {
          "bounds": {"x": 0, "y": 385, "width": 1250, "height": 1000},
          "action": {"type": "message", "text": "todolist_menu"}
        },
        {
          "bounds": {"x": 1250, "y": 392, "width": 1250, "height": 1000},
          "action": {"type": "message", "text": "rand_menu"}
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)
#"richMenuId":"richmenu-36a4f857e0bf5f7c127bece8b73668cf"
