# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def get_price(value):
    try:
        value = float(value)
    except Exception:
        value = None
    return value

class LeroyparserItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(get_price), output_processor=TakeFirst())
    specifications = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    spec_name = scrapy.Field()
    spec_description = scrapy.Field()
