from lxml import html
import requests


def get_bbc_news_data():
    news = []
    url = 'https://www.bbc.com'
    section = '/news'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 Safari/537.36 '
    }

    response = requests.get(url + section, headers=headers)
    dom = html.fromstring(response.text)

    items = dom.xpath("//div[contains(@class, 'nw-c-top-stories__secondary-item')]")
    top_items = dom.xpath("//div[contains(@class, 'nw-c-top-stories__tertiary-items')]")
    for item in [*items, *top_items]:
        new_date = item.xpath(".//time[contains(@class, 'date')]/@datetime")
        info = {
            'title': item.xpath(".//h3[contains(@class, 'gs-c-promo-heading__title')]/text()")[0],
            'link': url + item.xpath(".//a[contains(@class, 'gs-c-promo-heading')]/@href")[0],
            'date': (new_date and new_date[0]) or None,
            'source_name': url,
        }

        news.append(info)

    return news
