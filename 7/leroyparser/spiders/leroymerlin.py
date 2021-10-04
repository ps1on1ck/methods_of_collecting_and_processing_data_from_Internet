import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroyparser.items import LeroyparserItem

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search?q={query}']

    def parse(self, response: HtmlResponse):
        products = response.xpath("//div[@data-qa-product]/a")
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for product in products:
            yield response.follow(product, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('photos', "//uc-pdp-media-carousel/picture/source[@media='only screen and (min-width: 768px)']/@data-origin")
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_value('specifications', {})
        loader.add_xpath('spec_name', "//dl[@class='def-list']/div[@class='def-list__group']/dt/text()")
        loader.add_xpath('spec_description', "//dl[@class='def-list']/div[@class='def-list__group']/dd/text()")
        loader.add_value('url', response.url)
        yield loader.load_item()
