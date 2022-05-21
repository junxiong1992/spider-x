# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class XiurenPipeline:
    def process_item(self, item, spider):
        return item

class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):

        group = request.meta['group']
        name = request.meta['name']
        file_name = f'{group}/{name}.jpg'
        # print(f'下载路径为{file_name}')
        return file_name

    # def item_completed(self, results, item, info):
    #     image_paths = [x['path'] for ok, x in results if ok]
    #     if not image_paths:
    #         raise DropItem('Image Downloaded Failed')
    #     return item

    def get_media_requests(self, item, info):
        yield Request(item['url'], meta={
            'name': item['name'],
            'group': item['group'],
            'url': item['url'],
        })