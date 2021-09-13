from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroyparser.spiders.leroymerlin import LeroymerlinSpider
from leroyparser import settings

query = 'ламинат'
if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, query=query)
    process.start()