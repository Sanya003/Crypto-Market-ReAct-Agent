import os
import requests
import json
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv()

FREECRYPTO_TOKEN = os.getenv("FREECRYPTO_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

headers = {
    "Authorization": f"Bearer {FREECRYPTO_TOKEN}"
}

get_crypto_list_url = "https://api.freecryptoapi.com/v1/getCryptoList"
response = requests.get(get_crypto_list_url, headers=headers)
data = response.json()
print(json.dumps(data, indent=2))

get_data_url = "https://api.freecryptoapi.com/v1/getData"
params = {'symbol': 'BTC'}
response = requests.get(get_data_url, headers=headers, params=params)
data = response.json()
print(json.dumps(data, indent=2))

news_api = NewsApiClient(api_key=NEWSAPI_KEY)

articles = news_api.get_everything(
    q="bitcoin",
    language="en",
    sort_by="relevancy",
    page=1
)
print(json.dumps(articles, indent=2))
