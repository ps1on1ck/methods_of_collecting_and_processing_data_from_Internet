# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline

class InstaparserPipeline:
    def process_item(self, item, spider):
        return item

class InstagramPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['picture']:
            try:
                yield scrapy.Request(item['picture'])
            except Exception as e:
                print(e)

    def item_completed(self, results, item, info):
        if results:
            item['picture'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{item["category"]}/{item["parent_name"]}/' + os.path.basename(urlparse(request.url).path)