# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class XdwspiderPipeline(object):
    def process_item(self, item, spider):
        return item


import hashlib
from scrapy.utils.python import to_bytes
import logging
from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline



class ImagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        if results[0][0]:
            print(results)
            path = results[0][1]["path"]
            print(path)
            item["movie_img"] = path
        else:
            item["movie_img"] = ""
        item.save()
        return item

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        # print(save_path)
        return 'movie/%s.jpg' % (image_guid)

    def get_media_requests(self, item, info):
        return [Request(x) for x in item.get(self.images_urls_field, [])]

