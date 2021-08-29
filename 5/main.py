from m_client import MClient
from mvideo_parser import MVideo
from yahoo_mail_parser import YahooMail
from file_client import FileClient

mClientNewItems = MClient('127.0.0.1', 27017, 'mvideo', 'new_items')
mClientYahoo = MClient('127.0.0.1', 27017, 'yahoo', 'inbox')
mVideo = MVideo()
fileClient = FileClient()

new_items = mVideo.get_goods_by_category_title('Новинки')
fileClient.save('new_products.json', new_items)
mClientNewItems.insert_many(new_items)

yahoo_cred = fileClient.load('yahoo_email_credentials.json')
if yahoo_cred:
    yahooClient = YahooMail(yahoo_cred['login'], yahoo_cred['password'])
    emails = yahooClient.get_emails()
    mClientYahoo.insert_many(emails)

