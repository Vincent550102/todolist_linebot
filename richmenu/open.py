import requests

headers = {"Authorization":"Bearer ArxxWJmB8uU+jiIb/NCsEWdF3sVsIQOxHewSpJbuOft8OJYXKbpr7P6TdjKyrLOjQTS46EgdFzf3FRpF1Q18iw3oXLOTsCb0rMMM+R3LKEB6ebEiGg8zJjOZ6A7Co5VHP4kRWIjeOrdBGJoFrk+Y7AdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-207420da779e3f9e7a212591c20590a4', 
                       headers=headers)

print(req.text)