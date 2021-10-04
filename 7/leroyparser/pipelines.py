# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from pprint import pprint
from scrapy.pipelines.images import ImagesPipeline
import os
from urllib.parse import urlparse


class LeroyparserPipeline:
    def process_item(self, item, spider):
        if not item['price']:
            item['price'] = None
        return item

class LeroyPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['title']}/{os.path.basename(urlparse(request.url).path)}"

class LeroySpecParserPipeline:
    def process_item(self, item, spider):
        spec_names = item['spec_name']
        spec_desc = item['spec_description']
        for i in range(len(spec_names)):
            spec_desc[i] = spec_desc[i].replace('\n', '').replace(' ', '')
            try:
                spec_desc[i] = float(spec_desc[i])
            except TypeError and ValueError:
                pass
            item['specifications'][spec_names[i]] = spec_desc[i]
        return item