import json,requests,html5lib
from bs4 import BeautifulSoup

API = "https://api.thecatapi.com/v1/images/search"
cat_url = requests.get(API).json()
print(cat_url[-1]['url'])