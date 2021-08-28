from m_client import MClient
from pprint import pprint
from bbc_news_parser import get_bbc_news_data
import json

# mClient = MClient('127.0.0.1', 27017, 'news', 'bbc')

google_news = get_bbc_news_data()
pprint(google_news)

# return_many = mClient.insert_many(google_news)
# pprint(return_many)

with open('bbc_news_data.json', 'w', encoding='utf-8') as a:
    json.dump(google_news, a, ensure_ascii=False)
